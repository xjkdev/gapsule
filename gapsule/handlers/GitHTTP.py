import asyncio
from asyncio.subprocess import PIPE
import os
import re
import base64

from tornado.web import RequestHandler, HTTPError

from gapsule.models import repo, user, git
from gapsule.settings import settings

GIT_URL_PATTERNS = [
    ("GET", "/HEAD"),
    ("GET", "/info/refs"),
    ("GET", "/objects/info/alternates"),
    ("GET", "/objects/info/http-alternates"),
    ("GET", "/objects/info/packs"),
    ("GET", "/objects/[0-9a-f]{2}/[0-9a-f]{38}"),
    ("GET", "/objects/pack/pack-[0-9a-f]{40}\\.pack"),
    ("GET", "/objects/pack/pack-[0-9a-f]{40}\\.idx"),
    ("POST", "/git-upload-pack"),
    ("POST", "/git-receive-pack"),
]

GIT_URL_PATTERNS_REGEX = '|'.join(p[1] for p in GIT_URL_PATTERNS)


def spawn_git_http_backend(method, query_string, root, path_info, content_type=None,
                           remote_user=None, remote_addr=None):
    env = dict(
        REQUEST_METHOD=method,
        GIT_PROJECT_ROOT=root,
        GIT_HTTP_EXPORT_ALL='',
        QUERY_STRING=query_string,
        PATH_INFO=path_info,
    )
    if content_type is not None:
        env['CONTENT_TYPE'] = content_type
    proc = asyncio.create_subprocess_exec('git', 'http-backend', env=env,
                                          stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return proc


def parse_cgi_stdout(data):
    maxi = data.find(b'\r\n\r\n')
    if maxi < 0:
        body = ''
    else:
        body = data[maxi+4:]
        data = data[:maxi].split(b'\r\n')
    header = dict()
    for line in data:
        k, v = line.split(b': ', 1)
        header[k.decode()] = v.decode()
    return header, body


class GitHTTPHandler(RequestHandler):

    def request_auth(self, authname=None):
        if authname is None:
            authname = "Git Access"
        self.set_header('WWW-Authenticate',
                        'Basic realm="{}"'.format(authname))
        self.set_status(401)
        self.finish()

    async def prepare(self):
        auth = self.request.headers.get('Authorization')
        if auth is None:
            return None
        auth = base64.decodebytes(auth.lstrip('Basic ').encode())
        auth = auth.decode()
        username, password = auth.split(':', 2)
        if await user.verify_user(username, password):
            self.current_user = username

    async def handle_git_request(self, method, owner, reponame, path_info):
        for method, pattern in GIT_URL_PATTERNS:
            if re.match(pattern+'$', path_info):
                break
        else:
            self.write("Request not supported: {}/{}".format(owner, reponame))
            raise HTTPError(404)

        try:
            root = git.get_repo_dirpath(owner, reponame)
        except ValueError as e:
            raise HTTPError(404) from e

        if not os.path.exists(root):
            raise HTTPError(404)

        query_string = self.request.query
        if method == 'POST':
            content_type = self.request.headers.get(
                'Accept', '').replace('result', 'request')
        else:
            content_type = None
        proc = await spawn_git_http_backend(
            method, query_string, root, path_info, content_type)
        # print(self.request.body)
        out, err = await asyncio.wait_for(proc.communicate(self.request.body), 10)
        await asyncio.wait_for(proc.wait(), 1)
        # print(out, err)
        if len(err) > 0:
            raise HTTPError(500)
        header, body = parse_cgi_stdout(out)
        for k, v in header.items():
            self.set_header(k, v)
        self.write(body)

    def check_read(self, owner, reponame):
        per = repo.check_read_permission(
            owner, reponame, self.current_user)
        if per is False:
            if self.current_user is None:
                self.request("Private Git Access")
                return False
            if not repo.check_read_permission(owner, reponame, self.current_user):
                raise HTTPError(403)
        return True

    async def get(self, owner, reponame, path_info):
        try:
            if self.check_read(owner, reponame):
                await self.handle_git_request('GET', owner, reponame, path_info)
        except repo.RepoNotFoundException:
            raise HTTPError(404)
        except HTTPError as e:
            raise e

    async def post(self, owner, reponame, path_info):
        try:
            if re.match('/git-upload-pack$', path_info) is not None:
                if self.current_user is None:
                    self.request_auth()
                    return
                if not repo.check_write_permission(owner, reponame, self.current_user):
                    raise HTTPError(403)
            elif not self.check_read(owner, reponame):
                return
            await self.handle_git_request('POST', owner, reponame, path_info)
        except repo.RepoNotFoundException:
            raise HTTPError(404)
        except HTTPError as e:
            raise e
