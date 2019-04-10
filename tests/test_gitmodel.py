from unittest import TestCase
import tempfile
import asyncio
import os
from subprocess import Popen, PIPE, DEVNULL
import re

from gapsule.models import git
from gapsule.settings import settings
from gapsule.utils import async_test


def ishash(s):
    return re.match('[0-9a-f]{40}', s) is not None


repopath = tempfile.TemporaryDirectory()
settings['repository_path'] = repopath.name
print('repository_path:', repopath.name)
root = None


def clone(testCase, tmpdir):
    p1 = Popen(['git', 'clone', root], cwd=tmpdir,
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
        if root is not None:
            return
        await git.init_git_repo('abcd', 'efgh')
        root = git.get_repo_dirpath('abcd', 'efgh')
        self.assertTrue(os.path.exists(root))
        print('testing repo', root)
        git._check_exists(root)
        with tempfile.TemporaryDirectory() as tmpdir:
            clone(self, tmpdir)
            commit_file(self, tmpdir, 'test1.txt', 'testing file1',
                        'init message')
        with tempfile.TemporaryDirectory() as tmpdir:
            clone(self, tmpdir)
            commit_file(self, tmpdir, 'test2.txt', 'testing file2',
                        'test commit')

    @async_test
    async def test_ls_files(self):
        files = await git.git_ls_files('abcd', 'efgh', 'master')
        for name, h in files:
            self.assertTrue(name in ['test1.txt', 'test2.txt'])
            self.assertIsNot(re.match('[0-9a-f]{40}', h), None)
        files = await git.git_ls_files('abcd', 'efgh', 'master', show_tree=True)
        for name, h, isdir in files:
            self.assertTrue(name in ['test1.txt', 'test2.txt'])
            self.assertTrue(ishash(h))
            self.assertFalse(isdir)

    @async_test
    async def test_log1(self):
        logs = await git.git_commit_logs('abcd', 'efgh', 'master')
        for h, _ in logs:
            self.assertTrue(ishash(h))
        self.assertEqual(logs[0][1], 'test commit')
        self.assertEqual(logs[1][1], 'init message')

    @async_test
    async def test_log2(self):
        logs = await git.git_commit_logs('abcd', 'efgh', 'master', pretty=git.HASH_DATE_AND_MESSAGE)
        for h, t, _ in logs:
            self.assertTrue(ishash(h))
            self.assertIsNot(
                re.match(r"\d{4}(-\d{2}){2}T(\d{2}:){2}\d{2}[+-]\d{2}:\d{2}", t), None)
        self.assertEqual(logs[0][2], 'test commit')
        self.assertEqual(logs[1][2], 'init message')

    @async_test
    async def test_log3(self):
        logs = await git.git_commit_logs('abcd', 'efgh', 'master', pretty=git.MEDIUM)
        self.assertEqual(logs[0]['message'], 'test commit')
        self.assertEqual(logs[1]['message'], 'init message')

    @async_test
    async def test_branch(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            clone(self, tmpdir)
            create_branch(self, tmpdir)
            commit_file(self, tmpdir, 'test3.txt', 'testing branch',
                        'test commit', set_branch=True)
        current, branches = await git.git_branches('abcd', 'efgh')
        self.assertEqual(current, 'master')
        self.assertEqual(len(branches), 2)
        self.assertIn('master', branches)
        self.assertIn('test-branch', branches)
