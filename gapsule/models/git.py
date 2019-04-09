import os
import functools
import subprocess
import asyncio
from subprocess import PIPE, DEVNULL
from typing import Union, Tuple, List, Dict

from gapsule.settings import settings
from gapsule.utils.async_proc import async_communicate
from gapsule.utils.check_validity import check_username_validity, check_reponame_validty


@functools.lru_cache(maxsize=32)
def _check_exists(root: str):
    if not os.path.exists(root):
        raise FileNotFoundError("Repo Not Found")


@functools.lru_cache(maxsize=32)
def get_repo_dirpath(owner: str, reponame: str) -> str:
    if not check_reponame_validty(reponame) or not check_username_validity(owner):
        raise ValueError('invalid reponame or username')
    dirpath = os.path.join(
        settings['repository_path'], '{}/{}'.format(owner, reponame))
    return dirpath


async def init_git_repo(owner: str, reponame: str) -> None:
    root = get_repo_dirpath(owner, reponame)
    if os.path.exists(root):
        raise FileExistsError("Repo Already Existed")
    os.makedirs(root)
    proc = subprocess.Popen(['git', 'init', '--bare'],
                            cwd=root, stdout=DEVNULL, stderr=DEVNULL)
    if proc.wait(timeout=2) != 0:
        raise RuntimeError("Repo Init failed")


async def git_ls_files(owner: str, reponame: str, branch: str, *, path: str = None, show_tree=False) \
        -> Union[List[Tuple[str, str]], List[Tuple[str, str, bool]]]:
    root = get_repo_dirpath(owner, reponame)
    _check_exists(root)
    if show_tree:
        cmd = ['git', 'ls-tree', '-r', '-t', branch]
    else:
        cmd = ['git', 'ls-tree', '-r', branch]
    if path is not None:
        cmd.append(path)
    proc = subprocess.Popen(cmd, cwd=root, stdout=PIPE, stderr=PIPE)
    out, err = await async_communicate(proc, timeout=2)
    if len(err) > 0:
        raise RuntimeError("git ls-tree error")
    filelines = map(lambda line: line.split(), out.decode().split('\n'))
    if not show_tree:
        result = [(info[3], info[2]) for info in filelines if len(info) != 0]
    else:
        result = [(info[3], info[2], info[1] == 'tree')
                  for info in filelines if len(info) != 0]
    return result

ONELINE = 0
MEDIUM = 1
DATE_AND_MESSAGE = 2

PRETTY_OPTION = {ONELINE: "--pretty=oneline", MEDIUM: "--pretty=medium",
                 DATE_AND_MESSAGE: "--pretty=format:%cI %s"}


def _read_medium_log(log: str) -> List[Dict[str, str]]:
    lines = log.split('\n')
    result = []
    tmp = {}
    state = 0
    for i, line in enumerate(lines):
        if state == 0:
            if line.startswith('commit'):
                s = line.split()
                tmp[s[0]] = s[1]
            state = 1
        elif state == 1:
            if line == '':
                state = 2
                continue
            k, v = line.split(': ', 1)
            tmp[k] = v.strip()
        elif state == 2:
            if line.startswith('    '):
                if 'message' not in tmp:
                    tmp['message'] = line[4:]
                else:
                    tmp['message'] += '\n' + line[4:]
            elif line == '':
                if i+1 == len(lines) or lines[i+1].startswith('commit'):
                    result.append(tmp)
                    tmp = {}
                    state = 0
                else:
                    tmp['message'] += '\n'
    if len(tmp) > 0:
        result.append(tmp)
    return result


async def git_commit_logs(owner: str, reponame: str, branch: str, pretty=ONELINE,
                          path=None, maxsize: int = None) \
        -> Union[List[Tuple[str, str]], List[Dict[str, str]]]:
    root = get_repo_dirpath(owner, reponame)
    _check_exists(root)
    cmd = ['git', 'log', '--date=iso8601-strict']
    if isinstance(maxsize, int):
        cmd += ['-n', str(maxsize)]
    cmd += [PRETTY_OPTION[pretty], branch]
    if path is not None:
        cmd += ['--', path]
    proc = subprocess.Popen(cmd, cwd=root, stdout=PIPE, stderr=PIPE)
    out, err = await async_communicate(proc, timeout=2)
    if len(err) > 0:
        raise RuntimeError("git log error")
    out = out.decode()
    if pretty == ONELINE:
        result = [line.split(' ', 1)
                  for line in out.split('\n')[:-1]]
    elif pretty == MEDIUM:
        result = _read_medium_log(out)
    elif pretty == DATE_AND_MESSAGE:
        result = [line.split(' ', 1)
                  for line in out.split('\n')]
    return result


async def get_all_files_latest_commit(owner: str, reponame: str, branch: str,
                                      files: List[str] = None) -> List[str]:
    if files is None:
        files = map(lambda x: x[0], await git_ls_files(owner, reponame, branch))

    async def _task(f):
        r = await git_commit_logs(owner, reponame, branch, path=f,
                                  pretty=DATE_AND_MESSAGE, maxsize=1)
        return r[0]
    done, pending = asyncio.wait((_task(f) for f in files), timeout=5)
    if len(pending) > 0:
        print("get_all_files_lastest_commit, not all tasks done.")
    return [f.result() for f in done]
