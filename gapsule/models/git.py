import os
import functools
import asyncio
from typing import Union, Tuple, List, Dict

from gapsule.settings import settings
from gapsule.utils.subprocess import run, PIPE, DEVNULL
from gapsule.utils.check_validity import check_username_validity, check_reponame_validity


@functools.lru_cache(maxsize=32)
def _check_exists(root: str):
    if not os.path.exists(root):
        raise FileNotFoundError("Repo Not Found")


@functools.lru_cache(maxsize=32)
def get_repo_dirpath(owner: str, reponame: str) -> str:
    if not check_reponame_validity(reponame) or not check_username_validity(owner):
        raise ValueError('invalid reponame or username')
    dirpath = os.path.join(
        settings['repository_path'], '{}/{}'.format(owner, reponame))
    return dirpath


async def init_git_repo(owner: str, reponame: str) -> None:
    root = get_repo_dirpath(owner, reponame)
    if os.path.exists(root):
        raise FileExistsError("Repo Already Existed")
    os.makedirs(root)
    code1, _out, _err = await run(['git', 'init', '--bare'], cwd=root,
                                  stdout=DEVNULL, stderr=DEVNULL, timeout=2)
    if code1 != 0:
        raise RuntimeError("Repo Init failed")
    code2, _out, _err = await run(['git', 'config', '--add', 'http.receivepack', 'true'], cwd=root,
                                  stdout=DEVNULL, stderr=DEVNULL, timeout=2)
    if code2 != 0:
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
    returncode, out, err = await run(cmd, cwd=root, stdout=PIPE, stderr=PIPE, timeout=2)
    if returncode != 0:
        err = err.decode()
        if 'fatal: Not a valid object name master' in err:
            return []
        raise RuntimeError("git ls-tree error")
    filelines = map(lambda line: line.split(
        maxsplit=3), out.decode().split('\n'))
    if not show_tree:
        result = [(info[3], info[2]) for info in filelines if len(info) != 0]
    else:
        result = [(info[3], info[2], info[1] == 'tree')
                  for info in filelines if len(info) != 0]
    return result

ONELINE = 0
MEDIUM = 1
HASH_DATE_AND_MESSAGE = 2

PRETTY_OPTION = {ONELINE: "--pretty=oneline", MEDIUM: "--pretty=medium",
                 HASH_DATE_AND_MESSAGE: "--pretty=format:%H\t%cI\t%s"}


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
        -> Union[List[Tuple[str, str]], List[Dict[str, str]], List[Tuple[str, str, str]]]:
    root = get_repo_dirpath(owner, reponame)
    _check_exists(root)
    cmd = ['git', 'log', '--date=iso8601-strict']
    if isinstance(maxsize, int):
        cmd += ['-n', str(maxsize)]
    cmd += [PRETTY_OPTION[pretty], branch]
    if path is not None:
        cmd += ['--', path]
    returncode, out, err = await run(cmd, cwd=root, stdout=PIPE, stderr=PIPE, timeout=2)
    if returncode != 0:
        err = err.decode()
        if ('does not have any commits yet' in err or
                "fatal: ambiguous argument 'master': unknown revision" in err):
            return []
        raise RuntimeError("git log error " + str(returncode))
    out = out.decode()
    if pretty == ONELINE:
        result = [line.split(' ', 1)
                  for line in out.split('\n')[:-1]]
    elif pretty == MEDIUM:
        result = _read_medium_log(out)
    elif pretty == HASH_DATE_AND_MESSAGE:
        result = [line.split('\t', 2)
                  for line in out.split('\n')]
    return result


async def git_branches(owner: str, reponame: str) -> Tuple[str, List[str]]:
    root = get_repo_dirpath(owner, reponame)
    _check_exists(root)
    cmd = ['git', 'branch']
    returncode, out, _err = await run(cmd, cwd=root, stdout=PIPE, stderr=DEVNULL, timeout=2)
    if returncode != 0:
        raise RuntimeError("git branch error")
    out = out.decode().split('\n')
    current = None
    branches = []
    for line in out[:-1]:
        if line.startswith('* '):
            current = line[2:]
        branches.append(line[2:])
    return (current, branches)


async def get_all_files_latest_commit(owner: str, reponame: str, branch: str,
                                      files: List[str] = None) -> List[str]:
    if files is None:
        files = map(lambda x: x[0], await git_ls_files(owner, reponame, branch))

    async def _task(f):
        r = await git_commit_logs(owner, reponame, branch, path=f,
                                  pretty=HASH_DATE_AND_MESSAGE, maxsize=1)
        return r[0]
    done, pending = asyncio.gather((_task(f) for f in files), 5)
    if len(pending) > 0:
        print("get_all_files_lastest_commit, not all tasks done.")
    return [f.result() for f in done]


async def git_fetch(dstroot: str, dstrefs: str, srcroot: str, srcrefs: str):
    cmd = ['git', 'fetch', 'file://'+srcroot]
    cmd += ['{}:{}'.format(srcrefs, dstrefs)]
    returncode, _out, _err = await run(cmd, cwd=dstroot, stdout=DEVNULL, stderr=DEVNULL,
                                       timeout=10)
    if returncode != 0:
        raise RuntimeError("git fetch error")


async def git_create_branch(root: str, newbranch: str, frombranch: str):
    cmd = ['git', 'branch', newbranch, frombranch]
    returncode, _out, _err = await run(cmd, cwd=root, stdout=DEVNULL, stderr=DEVNULL,
                                       timeout=2)
    if returncode != 0:
        raise RuntimeError("git branch error")


async def git_clone(workingdir: str, owner: str, reponame: str, branch: str = None):
    root = get_repo_dirpath(owner, reponame)
    cmd = ['git', 'clone']
    if branch is None:
        cmd += ['-b', branch]
    cmd += ['file://' + root]
    returncode, _out, _err = await run(cmd, cwd=workingdir, stdout=DEVNULL, stderr=DEVNULL,
                                       timeout=10)
    if returncode != 0:
        raise RuntimeError("git branch error")


async def git_checkout(workingdir: str, branch: str):
    cmd = ['git', 'checkout', branch]
    returncode, _out, _err = await run(cmd, cwd=workingdir, stdout=DEVNULL, stderr=DEVNULL,
                                       timeout=5)
    if returncode != 0:
        raise RuntimeError("git checkout error")


async def git_merge_action(workingdir: str, action: str):
    if action not in ('abort', 'continue'):
        raise ValueError('action must be abort or continue')
    cmd = ['git', 'merge', '--'+action]
    returncode, _out, _err = await run(cmd, cwd=workingdir, stdout=DEVNULL, stderr=DEVNULL,
                                       timeout=5)
    if returncode != 0:
        raise RuntimeError("git merge error")


class CanNotAutoMerge(RuntimeError):
    pass


async def git_merge(workingdir: str, dstbranch: str, srcbranch: str):
    await git_checkout(workingdir, dstbranch)
    cmd = ['git', 'merge', '--no-ff', srcbranch]
    returncode, _out, _err = await run(cmd, cwd=workingdir, stdout=DEVNULL, stderr=DEVNULL,
                                       timeout=5)
    if returncode == 1:
        raise CanNotAutoMerge('can not auto merge')
    elif returncode != 0:
        raise RuntimeError("git merge error")


async def git_push(workingdir: str, dstbranch: str, remote: str = None):
    if dstremote is None:
        dstremote = 'origin'
    cmd = ['git', 'push', remote, dstbranch]
    returncode, _out, _err = await run(cmd, cwd=workingdir, stdout=DEVNULL, stderr=DEVNULL,
                                       timeout=5)
    if returncode != 0:
        raise RuntimeError("git push error")


async def git_pull(workingdir: str, remote: str = None):
    if dstremote is None:
        dstremote = 'origin'
    cmd = ['git', 'pull', remote]
    returncode, _out, _err = await run(cmd, cwd=workingdir, stdout=DEVNULL, stderr=DEVNULL,
                                       timeout=5)
    if returncode != 0:
        raise RuntimeError("git pull error")
