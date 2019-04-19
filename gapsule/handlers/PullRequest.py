import asyncio
import tornado.web

from gapsule.models import git, pullrequest, repo
from gapsule.utils.decorators import ajaxquery
from gapsule.handlers.Base import BaseHandler


class CreatePullRequestHandler(BaseHandler):
    @ajaxquery
    async def get(self, owner, reponame, restpath):
        compare_info = await self.judgeBranch(owner, reponame, restpath)

        preview = await pullrequest.pull_request_preview(
            compare_info['base_owner'], reponame, compare_info['base_branch'],
            compare_info['compare_owner'], reponame, compare_info['compare_branch'])

        preview['state'] = 'ok'
        self.write(preview)

    async def judgeBranch(self, owner, reponame, statepath):
        compare_dict = {
            'base_owner': owner,
            'compare_owner': owner,
        }
        state = 0
        tmp = ''
        for ch in statepath:
            if ch == ':' and state == 0:
                compare_dict["base_owner"] = owner
                tmp, state = '', 1
            elif ch == '.' and state == 0:
                compare_dict["base_owner"] = owner
                compare_dict["base_branch"] = tmp
                tmp, state = '', 2
            elif ch == '.' and state == 1:
                compare_dict["base_branch"] = tmp
                tmp, state = '', 2
            elif tmp == '...' and state == 2:
                tmp, state = '', 3
            elif ch == ':' and state == 3:
                compare_dict["compare_owner"] = tmp
                tmp, state = '', 4
            tmp += ch
        if state == 4:
            compare_dict["compare_branch"] = tmp
        else:
            compare_dict["compare_owner"] = owner
            compare_dict["base_branch"] = tmp
        if 'base_branch' not in compare_dict:
            compare_dict['base_branch'] = await asyncio.gather(
                repo.get_default_branch(compare_dict["base_owner"], reponame)
            )
        if 'compare_branch' not in compare_dict:
            compare_dict['compare_branch'] = await asyncio.gather(
                repo.get_default_branch(
                    compare_dict["compare_owner"], reponame)
            )
        return compare_dict


class PullCommitsHandler(BaseHandler):
    @ajaxquery
    async def get(self, owner, reponame, postid):
        pull_commits_dict = {
            "state": "ok",
            "log": await pullrequest.pull_request_log(owner, reponame, postid)
        }
        self.write(pull_commits_dict)


class PullChecksHandler(BaseHandler):
    @ajaxquery
    async def get(self, owner, reponame, postid):
        pull_checks_dict = {
            "status": "ok",
            # TODO: 需要数据库提供接口
            # 参数 owner, reponame, postid（关键码数字）,name
            "checks": {
                "number": "number",
                "content": "content",
            }
        }
        self.write(pull_checks_dict)


class PullFilesHandler(BaseHandler):
    @ajaxquery
    async def get(self, owner, reponame, postid):
        pull_files_dict = {
            "status": "ok",
            "diff": await pullrequest.pull_request_diff(owner, reponame, postid)
        }
        self.write(pull_files_dict)
