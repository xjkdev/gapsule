from unittest import TestCase
import tempfile
import os
from subprocess import Popen, PIPE, DEVNULL
import re
import time

from gapsule.models import git, pullrequest
from gapsule.settings import settings
from gapsule.utils import async_test


def ishash(s):
    return re.match('[0-9a-f]{40}', s) is not None


repopath = tempfile.TemporaryDirectory()
root = None


def clone(testCase, tmpdir, path):
    p1 = Popen(['git', 'clone', path], cwd=tmpdir,
               stdout=DEVNULL, stderr=DEVNULL)
    testCase.assertEqual(p1.wait(), 0)


def commit_file(testCase, tmpdir, filename, content, msg, set_branch=False):
    newrepo = os.path.join(tmpdir, 'efgh')
    with open(os.path.join(newrepo, filename), 'w') as f:
        f.write(content)
        f.close()
    p2 = Popen(['git', 'add', filename], cwd=newrepo,
               stdout=DEVNULL, stderr=DEVNULL)
    testCase.assertEqual(p2.wait(), 0)
    p3 = Popen(['git', 'commit', '-m', msg], cwd=newrepo,
               stdout=DEVNULL, stderr=DEVNULL)
    testCase.assertEqual(p3.wait(), 0)
    if not set_branch:
        p4 = Popen(['git', 'push'], cwd=newrepo,
                   stdout=DEVNULL, stderr=DEVNULL)
    else:
        p4 = Popen(['git', 'push', '--set-upstream', 'origin', 'test-branch'], cwd=newrepo,
                   stdout=DEVNULL, stderr=DEVNULL)
    testCase.assertEqual(p4.wait(), 0)


def create_branch(testCase, tmpdir):
    newrepo = os.path.join(tmpdir, 'efgh')
    p2 = Popen(['git', 'checkout', '-btest-branch'], cwd=newrepo,
               stdout=DEVNULL, stderr=DEVNULL)
    testCase.assertEqual(p2.wait(), 0)


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
        print('testing recpo', root)
        git._check_exists(root)
        with tempfile.TemporaryDirectory() as tmpdir:
            clone(self, tmpdir, root)
            commit_file(self, tmpdir, 'test1.txt', 'testing file1',
                        'init message')
        with tempfile.TemporaryDirectory() as tmpdir:
            clone(self, tmpdir, root)
            commit_file(self, tmpdir, 'test2.txt', 'testing file2',
                        'test commit')

    @async_test
    async def test_create_pr1(self):
        time.sleep(1)
        with tempfile.TemporaryDirectory() as tmpdir:
            clone(self, tmpdir, root)
            create_branch(self, tmpdir)
            commit_file(self, tmpdir, 'test1.txt', 'testing pull request',
                        'add commit', set_branch=True)
        await pullrequest.create_pull_request_git(
            'abcd', 'efgh', 'master', 1, 'abcd', 'efgh', 'test-branch')
        pull_head_log = await git.git_commit_logs('abcd', 'efgh', 'refs/pull/1/head')
        self.assertEqual(pull_head_log[0][1], 'add commit')
        pull_merge_log = await git.git_commit_logs('abcd', 'efgh', 'refs/pull/1/merge')
        merge_msg = pullrequest.get_merge_message(
            1, 'abcd', 'test-branch')
        self.assertEqual(pull_merge_log[0][1], merge_msg)
        before_merged_log = await git.git_commit_logs('abcd', 'efgh', 'master')
        self.assertEqual(before_merged_log[0][1], 'test commit')
        await pullrequest.merge_pull_request_git('abcd', 'efgh', 'master', 1)
        merged_log = await git.git_commit_logs('abcd', 'efgh', 'master')
        self.assertEqual(merged_log[0][1], merge_msg)
        self.assertEqual(merged_log[1][1], 'add commit')
