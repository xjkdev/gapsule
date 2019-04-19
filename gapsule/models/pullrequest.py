import tempfile
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


async def create_pull_request(dstowner: str, dstrepo: str, dstbranch: str,
                              srcowner: str, srcrepo: str, srcbranch: str,
                              title: str, status: str, visibility: bool):

    dst_repo_id = await get_repo_id(dstowner, dstrepo)
    src_repo_id = await get_repo_id(srcowner, srcrepo)

    this_id = await create_new_attached_post(dst_repo_id, srcowner, title,
                                             status, visibility, False)

    branches = (await git_branches(dstowner, dstrepo))[1]
    if not dstbranch in branches:
        raise BranchNotFoundException()
    branches2 = (await git_branches(srcowner, srcrepo))[1]
    if not srcbranch in branches2:
        raise BranchNotFoundException()

    flag_auto_merged = await create_pull_request_git(dstowner, dstrepo,
                                                     dstbranch, this_id,
                                                     srcowner, srcrepo,
                                                     srcbranch)
    await execute(
        '''
        INSERT INTO pull_requests(dest_repo_id,dest_branch,pull_id,src_repo_id,src_branch,created_time,status,auto_merge_status)
        VALUES($1,$2,$3,$4,$5,$6,$7,$8)
        ''', dst_repo_id, dstbranch, this_id, src_repo_id, srcbranch,
        datetime_now(), status, flag_auto_merged)


async def get_pull_request_info(dstowner: str, dstrepo: str, pull_id: int):
    result = await fetchrow(
        '''
        SELECT * FROM pull_requests
        WHERE pull_id=$1 and dest_repo_id=$2
        ''', pull_id, await get_repo_id(dstowner, dstrepo))
    return dict(result)


async def merge_pull_request(dstowner: str, dstrepo: str, dstbranch: str,
                             pullid: int):
    try:
        merge_pull_request_git(dstowner, dstrepo, dstbranch, pullid)
    except:
        await execute(
            '''
            UPDATE pull_requests
            SET auto_merge_status=$1
            WHERE dest_repo_id=$2 and pullid=$3
            ''', False, get_repo_id(dstowner, dstrepo), pullid)
    else:
        await execute(
            '''
            UPDATE pull_requests
            SET auto_merge_status=$1
            WHERE dest_repo_id=$2 and pullid=$3
            ''', True, get_repo_id(dstowner, dstrepo), pullid)


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
            WHERE dest_repo_id=$2 and pullid=$3
            ''', 'Closed', get_repo_id(dstowner, dstrepo), pullid)


_working_dirs = {}


async def get_working_dir(owner, reponame, pullid):
    if (owner, reponame, pullid) not in _working_dirs:
        tmpdir = tempfile.TemporaryDirectory()
        git.git_clone(tmpdir.name, owner, reponame)
        _working_dirs[(owner, reponame, pullid)] = tmpdir
    else:
        tmpdir = _working_dirs[(owner, reponame, pullid)]
    dstroot = '{}/{}'.format(tmpdir.name, reponame)
    return dstroot


async def finish_working_dir(owner, reponame, pullid):
    del _working_dirs[(owner, reponame, pullid)]


async def create_pull_request_git(dstowner: str, dstrepo: str, dstbranch: str,
                                  pullid: int, srcowner: str, srcrepo: str,
                                  srcbranch: str):
    dstroot = git.get_repo_dirpath(dstowner, dstrepo)
    srcroot = git.get_repo_dirpath(srcowner, srcrepo)
    pr_head_branch = 'pull/{}/head'.format(pullid)
    pr_merge_branch = 'pull/{}/merge'.format(pullid)
    await git.git_fetch(dstroot, pr_head_branch, srcroot, srcbranch)
    workingdir = get_working_dir(dstowner, dstrepo, pullid)
    await git.git_create_branch(workingdir, pr_merge_branch, dstbranch)
    await git.git_checkout(workingdir, pr_merge_branch)
    flag_auto_merged = True
    try:
        await git.git_merge(workingdir, dstbranch, pr_head_branch)
    except git.CanNotAutoMerge:
        await git.git_merge_action(workingdir, 'abort')
        flag_auto_merged = False
    except RuntimeError as e:
        raise e
    await git.git_push(workingdir, pr_merge_branch, 'origin')
    return flag_auto_merged


async def merge_pull_request_git(dstowner: str, dstrepo: str, dstbranch: str,
                                 pullid: int):
    if (dstowner, dstrepo, pullid) not in _working_dirs:
        raise RuntimeError('merge pull request before create')
    workingdir = get_working_dir(dstowner, dstrepo, pullid)
    # TODO: pull dstbranch, check if updated, and check if really merged
    pr_merge_branch = 'pull/{}/merge'.format(pullid)
    await git.git_checkout(workingdir, pr_merge_branch)
    await git.git_push(workingdir, dstbranch, 'origin')
    finish_working_dir(dstowner, dstrepo, pullid)
    return True


async def close_pull_request_git(dstowner: str, dstrepo: str, pullid: int):
    finish_working_dir(dstowner, dstrepo, pullid)
