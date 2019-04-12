import tempfile
from dataclasses import dataclass
from typing import Optional, Dict, Tuple, List
from gapsule.models import git, repo


async def create_pull_request(dstowner: str, dstrepo: str, dstbranch: str, pullid: int,
                              srcowner: str, srcrepo: str, srcbranch: str):
    flag_auto_merged = await create_pull_request_git(dstowner, dstrepo, dstbranch, pullid,
                                                     srcowner, srcrepo, srcbranch)
    # TODO: add to database dstowner,dstrepo,dstbranch,pullid,status, auto_merge_status
    #       ,srcowner,strrepo,srcbranch
    # status: open, close, merged
    # auto_merge_status: true/false, failing to auto merge implys having conflicts.


async def merge_pull_request(dstowner: str, dstrepo: str, pullid: int):
    # TODO: get desbranch to call merge_pull_request_git
    # TODO: call merge_pull_request_git
    # TODO: change state to merged if merged.
    pass


async def close_pull_request(dstowner: str, dstrepo: str, pullid: int):
    # TODO: call merge_pull_request_git
    # TODO: change state to closed.
    pass


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


async def create_pull_request_git(dstowner: str, dstrepo: str, dstbranch: str, pullid: int,
                                  srcowner: str, srcrepo: str, srcbranch: str):
    dstroot = git.get_repo_dirpath(dstowner, dstrepo)
    srcroot = git.get_repo_dirpath(srcowner, srcrepo)
    pr_head_branch = 'pull/{}/head'.format(pullid)
    pr_merge_branch = 'pull/{}/merge'.format(pullid)
    await git.git_fetch(dstroot, pr_head_branch,
                        srcroot, srcbranch)
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


async def merge_pull_request_git(dstowner: str, dstrepo: str, dstbranch: str, pullid: int):
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
