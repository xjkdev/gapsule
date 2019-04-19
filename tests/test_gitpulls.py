from unittest import TestCase, mock
import tempfile
import os
from subprocess import Popen, PIPE, DEVNULL
import time
import asyncio

from gapsule.models import git, pullrequest
from gapsule.settings import settings
from gapsule.utils import async_test
from tests.test_gitmodel import clone, commit_file, create_branch


repopath = tempfile.TemporaryDirectory()
root = None
lock = asyncio.Lock()


class GitModelTestCase(TestCase):

    @async_test
    async def setUp(self):
        global root
        git.get_repo_dirpath.cache_clear()
        settings['repository_path'] = repopath.name
        print('repository_path:', repopath.name)
        if root is not None:
            return
        await git.init_git_repo('abcd', 'efgh')
        root = git.get_repo_dirpath('abcd', 'efgh')
        self.assertTrue(os.path.exists(root))
        print('testing repo', root)
        git._check_exists(root)
        with tempfile.TemporaryDirectory() as tmpdir:
            clone(self, tmpdir, root)
            commit_file(self, tmpdir, 'test1.txt', 'testing file1',
                        'init message')
        with tempfile.TemporaryDirectory() as tmpdir:
            clone(self, tmpdir, root)
            commit_file(self, tmpdir, 'test2.txt', 'testing file2',
                        'test commit')

        async def _mock(*args):
            return {'dest_branch': 'master'}

        pullrequest.get_pull_request_info = _mock

    @async_test
    async def test_create_pr1(self):
        async with lock:
            time.sleep(1)
            with tempfile.TemporaryDirectory() as tmpdir:
                clone(self, tmpdir, root)
                create_branch(self, tmpdir)
                commit_file(self, tmpdir, 'test1.txt', 'testing\npull request\n',
                            'add commit', set_branch=True)
            await pullrequest.create_pull_request_git('abcd', 'efgh', 'master',
                                                      1,
                                                      'abcd', 'efgh', 'test-branch',
                                                      'testuser', 'test@example.com')
            pull_head_log = await git.git_commit_logs('abcd', 'efgh', 'refs/pull/1/head')
            self.assertEqual(pull_head_log[0][1], 'add commit')
            pull_merge_log = await git.git_commit_logs('abcd', 'efgh', 'refs/pull/1/merge')
            merge_msg = pullrequest.get_merge_message(
                1, 'abcd', 'test-branch')
            self.assertEqual(pull_merge_log[0][1], merge_msg)
            before_merged_log = await git.git_commit_logs('abcd', 'efgh', 'master')
            self.assertEqual(before_merged_log[0][1], 'test commit')
            await pullrequest.merge_pull_request_git('abcd', 'efgh', 1)
            merged_log = await git.git_commit_logs('abcd', 'efgh', 'master')
            self.assertEqual(merged_log[0][1], merge_msg)
            self.assertEqual(merged_log[1][1], 'add commit')

    @async_test
    async def test_create_pr_conflict(self):
        async with lock:
            time.sleep(1)
            with tempfile.TemporaryDirectory() as tmpdir:
                clone(self, tmpdir, root)
                create_branch(self, tmpdir, 'test-branch-b')
                commit_file(self, tmpdir, 'test1.txt', 'testing\nconflict\npull request\n',
                            'add commit conflict', set_branch=True, branch='test-branch-b')
            with tempfile.TemporaryDirectory() as tmpdir:
                clone(self, tmpdir, root)

                commit_file(self, tmpdir, 'test1.txt', 'testing\nmaking flictcon\npush request\n',
                            'can not auto commit')
            flag, out = await pullrequest.create_pull_request_git('abcd', 'efgh', 'master',
                                                                  2,
                                                                  'abcd', 'efgh', 'test-branch-b',
                                                                  'testuser', 'test@example.com')
            self.assertFalse(flag)
            self.assertEqual(out,
                             'CONFLICT (content): Merge conflict in test1.txt')
