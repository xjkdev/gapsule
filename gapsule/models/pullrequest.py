import tempfile
import asyncio

from dataclasses import dataclass
from typing import Optional, Dict, Tuple, List
from gapsule.models import git, repo
from gapsule.models.git import git_branches
from gapsule.models.repo import get_repo_id
from gapsule.models.connection import execute, fetchrow
from gapsule.utils.cookie_session import datetime_now
from gapsule.models.post import create_new_attached_post


class BranchNotFoundException(FileNotFoundError):
    pass


def get_merge_message(pullid: int, srcowner: str, srcbranch: str,
                      content: str = None):
    msg = 'Merge pull request #{} from {}/{}'.format(
        pullid, srcowner, srcbranch)
    if content is not None:
        msg += '\n\n' + content
    return msg


def is_merge_message(message: str, pullid: int):
    return message.startswith('Merge pull request #{} from'.format(pullid))


async def create_pull_request(dstowner: str, dstrepo: str, dstbranch: str,
                              srcowner: str, srcrepo: str, srcbranch: str,
                              title: str, status: str, visibility: bool):

    dst_repo_id = await get_repo_id(dstowner, dstrepo)
    src_repo_id = await get_repo_id(srcowner, srcrepo)

    branches = (await git_branches(dstowner, dstrepo))[1]
    if not dstbranch in branches:
        raise BranchNotFoundException()
    branches2 = (await git_branches(srcowner, srcrepo))[1]
    if not srcbranch in branches2:
        raise BranchNotFoundException()
    current_id = await fetchrow(
        '''
        SELECT max(pull_id) FROM pull_requests
        WHERE dest_repo_id=$1
        ''', dst_repo_id)
    this_id = 1
    if current_id['max'] != None:
        this_id = current_id['max'] + 1

    flag_auto_merged = await create_pull_request_git(dstowner, dstrepo,
                                                     dstbranch, this_id,
                                                     srcowner, srcrepo,
                                                     srcbranch, title)
    await execute(
        '''
        INSERT INTO pull_requests(dest_repo_id,dest_branch,pull_id,src_repo_id,src_branch,created_time,status,auto_merge_status)
        VALUES($1,$2,$3,$4,$5,$6,$7,$8)
        ''', dst_repo_id, dstbranch, this_id, src_repo_id, srcbranch,
        datetime_now(), status, flag_auto_merged)

    await create_new_attached_post(dst_repo_id, srcowner, title, status,
                                   visibility, False)


async def merge_pull_request(dstowner: str, dstrepo: str, dstbranch: str,
                             pullid: int):
    try:
        merge_pull_request_git(dstowner, dstrepo, dstbranch, pullid)
    except:
        await execute(
            '''
            UPDATE pull_requests
            SET auto_merge_status=$1
            ''', False)
    else:
        await execute(
            '''
            UPDATE pull_requests
            SET auto_merge_status=$1
            ''', True)


async def close_pull_request(dstowner: str, dstrepo: str, dstbranch: str,
                             pullid: int):
    try:
        merge_pull_request_git(dstowner, dstrepo, dstbranch, pullid)
    except:
        pass
    else:
        await execute(
            '''
            UPDATE pull_requests
            SET status=$1
            ''', 'Closed')


_working_dirs = {}


async def get_working_dir(owner, reponame, pullid):
    if (owner, reponame, pullid) not in _working_dirs:
        tmpdir = tempfile.TemporaryDirectory()
        await git.git_clone(tmpdir.name, owner, reponame)
        _working_dirs[(owner, reponame, pullid)] = tmpdir
    else:
        tmpdir = _working_dirs[(owner, reponame, pullid)]
    dstroot = '{}/{}'.format(tmpdir.name, reponame)
    return dstroot


def finish_working_dir(owner, reponame, pullid):
    _working_dirs[(owner, reponame, pullid)].cleanup()
    del _working_dirs[(owner, reponame, pullid)]


async def create_pull_request_git(dstowner: str, dstrepo: str, dstbranch: str,
                                  pullid: int, srcowner: str, srcrepo: str,
                                  srcbranch: str, content: str = None):
    dstroot = git.get_repo_dirpath(dstowner, dstrepo)
    srcroot = git.get_repo_dirpath(srcowner, srcrepo)
    pr_head_branch = 'refs/pull/{}/head'.format(pullid)
    pr_merge_branch = 'refs/pull/{}/merge'.format(pullid)
    await git.git_fetch(dstroot, pr_head_branch, srcroot, srcbranch)
    workingdir = await get_working_dir(dstowner, dstrepo, pullid)
    await git.git_fetch(workingdir, pr_head_branch, dstroot, pr_head_branch)
    flag_auto_merged = True
    try:
        # TODO: merge author
        await git.git_merge(workingdir, dstbranch, pr_head_branch)
        msg = get_merge_message(pullid, srcowner, srcbranch, content)
        await git.git_commit(workingdir, msg)
    except git.CanNotAutoMerge:
        await git.git_merge_action(workingdir, 'abort')
        flag_auto_merged = False
    except RuntimeError as e:
        raise e
    await git.git_fetch(dstroot, pr_merge_branch, workingdir, dstbranch)
    return flag_auto_merged


async def merge_pull_request_git(dstowner: str, dstrepo: str, dstbranch: str,
                                 pullid: int):
    if (dstowner, dstrepo, pullid) not in _working_dirs:
        raise RuntimeError('merge pull request before create')
    dstroot = git.get_repo_dirpath(dstowner, dstrepo)
    pr_merge_branch = 'refs/pull/{}/merge'.format(pullid)
    workingdir = await get_working_dir(dstowner, dstrepo, pullid)
    print(workingdir, pr_merge_branch, dstbranch)

    latest_commit_merge, latest_commit_dst = await asyncio.gather(
        git.git_log(dstroot, pr_merge_branch, maxsize=1),
        git.git_log(dstroot, dstbranch, maxsize=1)
    )
    if (not is_merge_message(latest_commit_merge[0][1], pullid)
            or latest_commit_dst[0][0] == latest_commit_merge[0][0]):
        raise RuntimeError('merge was not actually performed.')

    await git.git_fetch(workingdir, pr_merge_branch, dstroot, pr_merge_branch)
    await git.git_checkout(workingdir, pr_merge_branch)
    await git.git_push(workingdir, dstbranch, 'origin')
    finish_working_dir(dstowner, dstrepo, pullid)
    return True


async def close_pull_request_git(dstowner: str, dstrepo: str, pullid: int):
    finish_working_dir(dstowner, dstrepo, pullid)
