import tempfile
import os
import multiprocessing
import asyncio
from asyncio.subprocess import PIPE, DEVNULL
from unittest.mock import Mock, MagicMock

from tornado.testing import AsyncHTTPTestCase, gen_test
from gapsule.utils import async_test
from gapsule.models import git, repo, user
from gapsule.settings import settings
from gapsule import app
from gapsule.handlers.GitHTTP import GitHTTPHandler
from tests.test_gitmodel import clone, commit_file

repopath = tempfile.TemporaryDirectory()
root = None

GitHTTPHandler.current_user = MagicMock(spec=property,
                                        __get__=lambda *args: 'abcd')


class GitServiceTestCase(AsyncHTTPTestCase):
    def get_app(self):
        return app.make_app()

    @async_test
    async def _before_setUp(self):
        global root
        git.get_repo_dirpath.cache_clear()
        settings['repository_path'] = repopath.name
        print('repository_path:', repopath.name)
        if root is not None:
            return
        await git.init_git_repo('abcd', 'efgh')
        root = git.get_repo_dirpath('abcd', 'efgh')
        self.assertTrue(os.path.exists(root))
        git._check_exists(root)
        # print('s test', root)
        with tempfile.TemporaryDirectory() as tmpdir:
            clone(self, tmpdir, root)
            commit_file(self, tmpdir, 'test1.txt', 'testing file1',
                        'init message')
        with tempfile.TemporaryDirectory() as tmpdir:
            clone(self, tmpdir, root)
            commit_file(self, tmpdir, 'test2.txt', 'testing file2',
                        'test commit')

    def setUp(self):
        self._before_setUp()
        super().setUp()

    @gen_test
    async def test_git_service(self):
        chk_read = Mock(return_value=True)
        repo.check_read_permission = asyncio.coroutine(chk_read)
        chk_write = Mock(return_value=True)
        repo.check_write_permission = asyncio.coroutine(chk_write)

        url = 'http://127.0.0.1:{}/abcd/efgh'.format(self.get_http_port())
        with tempfile.TemporaryDirectory() as tmpdir:
            p1 = await asyncio.create_subprocess_exec('git',
                                                      'clone',
                                                      url,
                                                      cwd=tmpdir,
                                                      stdout=DEVNULL,
                                                      stderr=DEVNULL)
            self.assertEqual(await p1.wait(), 0)
            newrepo = os.path.join(tmpdir, 'efgh')
            self.assertTrue(os.path.exists(newrepo))
            self.assertTrue(os.path.exists(os.path.join(newrepo, 'test1.txt')))
            self.assertTrue(os.path.exists(os.path.join(newrepo, 'test2.txt')))
            filename = 'test3.txt'
            content = msg = 'test pushing'

            with open(os.path.join(newrepo, filename), 'w') as f:
                f.write(content)
                f.close()
            p2 = await asyncio.create_subprocess_exec('git',
                                                      'add',
                                                      filename,
                                                      cwd=newrepo,
                                                      stdout=DEVNULL,
                                                      stderr=DEVNULL)
            self.assertEqual(await p2.wait(), 0)
            p3 = await asyncio.create_subprocess_exec('git',
                                                      'commit',
                                                      '-m',
                                                      msg,
                                                      cwd=newrepo,
                                                      stdout=DEVNULL,
                                                      stderr=DEVNULL)
            self.assertEqual(await p3.wait(), 0)
            p4 = await asyncio.create_subprocess_exec('git',
                                                      'push',
                                                      cwd=newrepo,
                                                      stdout=DEVNULL,
                                                      stderr=DEVNULL)
            self.assertEqual(await p4.wait(), 0)
