import os
import shutil
import functools
import asyncio
from concurrent.futures import ProcessPoolExecutor
import chardet
from typing import Union, Tuple, List, Dict

from gapsule.settings import settings
from gapsule.utils.log_call import log_call
from gapsule.utils.subprocess import run, PIPE, DEVNULL
from gapsule.utils.check_validity import check_username_validity, check_reponame_validity


@functools.lru_cache(maxsize=32)
def _check_exists(root: str):
    if not os.path.exists(root):
        raise FileNotFoundError("Repo Not Found")


@functools.lru_cache(maxsize=32)
def get_repo_dirpath(owner: str, reponame: str) -> str:
    if not check_reponame_validity(reponame) or not check_username_validity(
            owner):
        raise ValueError('invalid reponame or username')
    dirpath = os.path.join(settings['repository_path'],
                           '{}/{}'.format(owner, reponame))
    return dirpath


def delete_repo(owner: str, reponame: str):
    path = get_repo_dirpath(owner, reponame)
    try:
        _check_exists(path)
        print('path', path)
        shutil.rmtree(path)
    except FileNotFoundError:
        pass


async def init_git_repo(owner: str, reponame: str) -> None:
    root = get_repo_dirpath(owner, reponame)
    if os.path.exists(root):
        raise FileExistsError("Repo Already Existed")
    os.makedirs(root)
    code1, _out, _err = await run(['git', 'init', '--bare'],
                                  cwd=root,
                                  stdout=DEVNULL,
                                  stderr=DEVNULL,
                                  timeout=2)
    if code1 != 0:
        raise RuntimeError("Repo Init failed")
    try:
        await git_config(root, 'http.receivepack', 'true')
    except Exception as e:
        raise RuntimeError("Repo Init failed") from e


async def git_config(workingdir: str, key: str, value: str):
    returncode, _out, _err = await run(['git', 'config', '--add', key, value], cwd=workingdir,
                                       stdout=DEVNULL, stderr=DEVNULL, timeout=2)
    if returncode != 0:
        raise RuntimeError("Repo Config failed")


async def git_ls_files(
        owner: str,
        reponame: str,
        branch: str,
        *,
        path: str = None,
        show_tree=False,
        recursive=True
) -> Union[List[Tuple[str, str]], List[Tuple[str, str, bool]]]:
    root = get_repo_dirpath(owner, reponame)
    _check_exists(root)
    cmd = ['git', 'ls-tree']
    if recursive:
        cmd += ['-r']
    if show_tree:
        cmd += ['-t']
    cmd += [branch]
    if path is not None:
        cmd.append(path)
    returncode, out, err = await run(cmd,
                                     cwd=root,
                                     stdout=PIPE,
                                     stderr=PIPE,
                                     timeout=2)
    if returncode != 0:
        err = err.decode()
        if 'fatal: Not a valid object name master' in err:
            return []
        raise RuntimeError("git ls-tree error")
    filelines = map(lambda line: line.split(maxsplit=3),
                    out.decode().split('\n'))
    if not show_tree:
        result = [(info[3], info[2]) for info in filelines if len(info) != 0]
    else:
        result = [(info[3], info[2], info[1] == 'tree') for info in filelines
                  if len(info) != 0]
    return result


ONELINE = 0
MEDIUM = 1
HASH_DATE_AND_MESSAGE = 2

PRETTY_OPTION = {
    ONELINE: "--pretty=oneline",
    MEDIUM: "--pretty=medium",
    HASH_DATE_AND_MESSAGE: "--pretty=format:%H\t%cI\t%s"
}


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
                if i + 1 == len(lines) or lines[i + 1].startswith('commit'):
                    result.append(tmp)
                    tmp = {}
                    state = 0
                else:
                    tmp['message'] += '\n'
    if len(tmp) > 0:
        result.append(tmp)
    return result


async def git_log(root: str,  branch: str, pretty=ONELINE,
                  path=None, maxsize: int = None, *, base: str = None) \
        -> Union[List[Tuple[str, str]], List[Dict[str, str]], List[Tuple[str, str, str]]]:
    cmd = ['git', 'log', '--date=iso8601-strict']
    if isinstance(maxsize, int):
        cmd += ['-n', str(maxsize)]
    cmd += [PRETTY_OPTION[pretty]]
    if base is None:
        cmd += [branch]
    else:
        cmd += ['{}..{}'.format(base, branch)]
    if path is not None:
        cmd += ['--', path]
    returncode, out, err = await run(cmd,
                                     cwd=root,
                                     stdout=PIPE,
                                     stderr=PIPE,
                                     timeout=2)
    if returncode != 0:
        err = err.decode()
        if ('does not have any commits yet' in err or
                "fatal: ambiguous argument 'master': unknown revision" in err):
            return []
        raise RuntimeError("git log error " + str(returncode), repr(err))
    out = out.decode()
    if pretty == ONELINE:
        result = [line.split(' ', 1) for line in out.split('\n')[:-1]]
    elif pretty == MEDIUM:
        result = _read_medium_log(out)
    elif pretty == HASH_DATE_AND_MESSAGE:
        result = [line.split('\t', 2) for line in out.split('\n')]
    return result


async def git_commit_logs(owner: str, reponame: str, branch: str, pretty=ONELINE,
                          path=None, maxsize: int = None, *, base: str = None) \
        -> Union[List[Tuple[str, str]], List[Dict[str, str]], List[Tuple[str, str, str]]]:
    root = get_repo_dirpath(owner, reponame)
    _check_exists(root)
    return await git_log(root, branch, pretty, path, maxsize, base=base)


async def git_branches(owner: str, reponame: str) -> Tuple[str, List[str]]:
    root = get_repo_dirpath(owner, reponame)
    _check_exists(root)
    cmd = ['git', 'branch']
    returncode, out, _err = await run(cmd,
                                      cwd=root,
                                      stdout=PIPE,
                                      stderr=DEVNULL,
                                      timeout=2)
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


async def get_all_files_latest_commit(owner: str,
                                      reponame: str,
                                      branch: str,
                                      files: List[str] = None) -> List[str]:
    if files is None:
        files = [
            x[0] for x in await git_ls_files(
                owner, reponame, branch, recursive=False)
        ]

    async def _task(f):
        r = await git_commit_logs(owner,
                                  reponame,
                                  branch,
                                  path=f,
                                  pretty=HASH_DATE_AND_MESSAGE,
                                  maxsize=1)
        return [f] + r[0]

    tasklist = (_task(f) for f in files)
    done = await asyncio.gather(*tasklist, return_exceptions=True)
    if len(done) < len(files):
        print("get_all_files_lastest_commit, not all tasks done.")
    return done


async def git_cat_file(owner: str, reponame: str, branch: str,
                       path: str) -> bytes:
    root = get_repo_dirpath(owner, reponame)
    _check_exists(root)
    print('244 line')
    files = await git_ls_files(owner,
                               reponame,
                               branch,
                               path=path,
                               show_tree=True,
                               recursive=False)
    for f in files:
        name, objhash, isdir = f
        if name == path:
            break
    else:
        raise FileNotFoundError(path)

    if isdir:
        raise OSError("trying to read content of directory")
    proc = await asyncio.create_subprocess_exec('git',
                                                'cat-file',
                                                'blob',
                                                objhash,
                                                cwd=root,
                                                stdout=PIPE,
                                                stderr=PIPE)
    out, err = await asyncio.wait_for(proc.communicate(), 5)
    if await asyncio.wait_for(proc.wait(), 1) != 0:
        print('a', out, err.decode())
        raise OSError("git cat file error")
    return out


@log_call()
async def git_fetch(dstroot: str, dstrefs: str, srcroot: str, srcrefs: str, *, fetch_head=False):
    cmd = ['git', 'fetch', 'file://'+srcroot]
    if not fetch_head:
        cmd += ['{}:{}'.format(srcrefs, dstrefs)]
    else:
        cmd += [srcrefs]
    returncode, _out, err = await run(cmd, cwd=dstroot, stdout=DEVNULL, stderr=PIPE,
                                      timeout=10)
    if returncode != 0:
        print(err)
        raise RuntimeError("git fetch error")


async def git_create_branch(root: str, newbranch: str, frombranch: str):
    cmd = ['git', 'branch', newbranch, frombranch]
    returncode, _out, _err = await run(cmd,
                                       cwd=root,
                                       stdout=DEVNULL,
                                       stderr=DEVNULL,
                                       timeout=2)
    if returncode != 0:
        raise RuntimeError("git branch error")


async def git_rm_branch(root: str, branch, *, force=False):
    cmd = ['git', 'branch']
    if force:
        cmd += ['-D']
    else:
        cmd += ['-d']
    cmd += [branch]
    returncode, _out, _err = await run(cmd,
                                       cwd=root,
                                       stdout=DEVNULL,
                                       stderr=PIPE,
                                       timeout=2)
    if returncode != 0:
        print(_err)
        raise RuntimeError("git rm branch error")


async def git_clone(workingdir: str,
                    owner: str,
                    reponame: str,
                    branch: str = None, *, bare=False):
    root = get_repo_dirpath(owner, reponame)
    cmd = ['git', 'clone']
    if bare:
        cmd += ['--bare']
    if branch is not None:
        cmd += ['-b', branch]
    cmd += ['file://' + root]
    returncode, _out, _err = await run(cmd,
                                       cwd=workingdir,
                                       stdout=DEVNULL,
                                       stderr=DEVNULL,
                                       timeout=10)
    if returncode != 0:
        raise RuntimeError("git branch error")


async def git_checkout(workingdir: str, branch: str):
    cmd = ['git', 'checkout', branch]
    returncode, _out, _err = await run(cmd,
                                       cwd=workingdir,
                                       stdout=DEVNULL,
                                       stderr=DEVNULL,
                                       timeout=5)
    if returncode != 0:
        raise RuntimeError("git checkout error")


async def git_merge_action(workingdir: str, action: str):
    if action not in ('abort', 'continue'):
        raise ValueError('action must be abort or continue')
    cmd = ['git', 'merge', '--' + action]
    returncode, _out, _err = await run(cmd,
                                       cwd=workingdir,
                                       stdout=DEVNULL,
                                       stderr=DEVNULL,
                                       timeout=5)
    if returncode != 0:
        raise RuntimeError("git merge error")


class CanNotAutoMerge(RuntimeError):
    pass


async def git_merge(workingdir: str, dstbranch: str, srcbranch: str):
    await git_checkout(workingdir, dstbranch)
    cmd = ['git', 'merge', '--no-commit', '--no-ff', srcbranch]
    returncode, out, err = await run(cmd, cwd=workingdir, stdout=PIPE, stderr=PIPE,
                                     timeout=5)
    out = out.decode().split('\n')
    conflicts = [line for line in out if line.startswith('CONFLICT')]
    if len(conflicts) > 0:
        raise CanNotAutoMerge('\n'.join(conflicts))
    if returncode != 0:
        print(out, err)
        raise RuntimeError("git merge error")


async def git_push(workingdir: str, dstbranch: str, dstremote: str = None):
    if dstremote is None:
        dstremote = 'origin'
    cmd = ['git', 'push', dstremote, dstbranch]
    returncode, _out, _err = await run(cmd,
                                       cwd=workingdir,
                                       stdout=DEVNULL,
                                       stderr=DEVNULL,
                                       timeout=5)
    if returncode != 0:
        raise RuntimeError("git push error")


async def git_pull(workingdir: str, dstremote: str = None):
    if dstremote is None:
        dstremote = 'origin'
    cmd = ['git', 'pull', dstremote]
    returncode, _out, _err = await run(cmd,
                                       cwd=workingdir,
                                       stdout=DEVNULL,
                                       stderr=DEVNULL,
                                       timeout=5)
    if returncode != 0:
        raise RuntimeError("git pull error")


async def git_commit(workingdir: str, message: str):
    message = message.encode()
    cmd = ['git', 'commit', '--file=-']
    returncode, _out, _err = await run(cmd, cwd=workingdir, input=message,
                                       stdout=DEVNULL, stderr=DEVNULL,
                                       timeout=5)
    if returncode != 0:
        raise RuntimeError("git commit error")


def git_diff_parsing(data):
    result = []
    i = 0
    head = b'\ndiff --git '
    len_head = len(head)-1
    len_data = len(data)
    while i < len_data:
        next_lineend = data.find(b'\n', i)
        nexti = data.find(head, next_lineend)
        if nexti == -1:
            nexti = len_data
        else:
            nexti = nexti + 1
        title = data[i + len_head: next_lineend].decode()
        body = data[next_lineend+1: nexti]
        det = chardet.detect(body[:1024])
        if det['encoding'] == 'ascii':
            result.append((title, body.decode()))
        else:
            result.append((title, body.decode(det['encoding'])))
        i = nexti
    return result


async def git_diff(workingdir: str, base_branch: str, compare_to: str) -> List[Tuple[str, str]]:
    """ Return a List which items are tuples, containing title and body.
        title are 'path_to_a_file path_to_b_file'
        body are diff format
    """
    cmd = ['git', 'diff', base_branch, compare_to]
    returncode, out, _err = await run(cmd, cwd=workingdir, stdout=PIPE, stderr=DEVNULL,
                                      timeout=5)
    if returncode != 0:
        raise RuntimeError("git diff error")

    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, git_diff_parsing, out)
    return result
