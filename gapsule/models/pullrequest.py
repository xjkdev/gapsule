import tempfile
import asyncio

from dataclasses import dataclass
from typing import Optional, Dict, Tuple, List
from gapsule.models import git, repo, user
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
                              title: str, authorname: str,
                              status: str, visibility: bool) -> Tuple[int, bool, str]:
    authoremail = await user.get_user_mail_address(authorname)
    dst_repo_id = await repo.get_repo_id(dstowner, dstrepo)
    src_repo_id = await repo.get_repo_id(srcowner, srcrepo)

    branches = (await git.git_branches(dstowner, dstrepo))[1]
    if not dstbranch in branches:
        raise BranchNotFoundException()
    branches2 = (await git.git_branches(srcowner, srcrepo))[1]
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

    flag_auto_merged, conflicts = await create_pull_request_git(dstowner, dstrepo, dstbranch,
                                                                this_id,
                                                                srcowner, srcrepo, srcbranch,
                                                                authorname, authoremail,
                                                                title)
    await execute(
        '''
        INSERT INTO pull_requests(dest_repo_id,dest_branch,pull_id,src_repo_id,src_branch,
                                  created_time,status,auto_merge_status)
        VALUES($1,$2,$3,$4,$5,$6,$7,$8)
        ''', dst_repo_id, dstbranch, this_id, src_repo_id, srcbranch,
        datetime_now(), status, flag_auto_merged)

    postid = await create_new_attached_post(dst_repo_id, srcowner, title, status,
                                            visibility, False)
    return postid, flag_auto_merged, conflicts


async def merge_pull_request(dstowner: str, dstrepo: str, pullid: int):
    merge_pull_request_git(dstowner, dstrepo, pullid)
    await execute(
        '''
        UPDATE pull_requests
        SET status=$1
        WHERE dest_repo_id=$2 and pullid=$3
        ''', 'Merged', repo.get_repo_id(dstowner, dstrepo), pullid)


async def close_pull_request(dstowner: str, dstrepo: str, pullid: int):
    finish_working_dir(dstowner, dstrepo, pullid)
    await execute(
        '''
        UPDATE pull_requests
        SET status=$1
        WHERE dest_repo_id=$2 and pullid=$3
        ''', 'Closed', repo.get_repo_id(dstowner, dstrepo), pullid)


async def get_pull_request_info(dstowner: str, dstrepo: str, pullid: int) -> Dict[str, ...]:
    dst_repo_id = await repo.get_repo_id(dstowner, dstrepo)
    result = await fetchrow(
        '''
        SELECT * FROM pull_requests WHERE dest_repo_id=$1 and pull_id=$2
        ''', dst_repo_id, pullid
    )
    if result is None:
        return None
    else:
        return dict(result)

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


def has_working_dir(owner, reponame, pullid):
    return (owner, reponame, pullid) in _working_dirs


def finish_working_dir(owner, reponame, pullid):
    _working_dirs[(owner, reponame, pullid)].cleanup()
    del _working_dirs[(owner, reponame, pullid)]


async def create_pull_request_git(dstowner: str, dstrepo: str, dstbranch: str, pullid: int,
                                  srcowner: str, srcrepo: str, srcbranch: str,
                                  authorname: str, authoremail: str,
                                  content: str = None):
    dstroot = git.get_repo_dirpath(dstowner, dstrepo)
    srcroot = git.get_repo_dirpath(srcowner, srcrepo)
    pr_head_branch = 'refs/pull/{}/head'.format(pullid)
    pr_merge_branch = 'refs/pull/{}/merge'.format(pullid)
    await git.git_fetch(dstroot, pr_head_branch, srcroot, srcbranch)
    workingdir = await get_working_dir(dstowner, dstrepo, pullid)
    await git.git_fetch(workingdir, pr_head_branch, dstroot, pr_head_branch)
    flag_auto_merged = True
    output = ''
    try:
        await git.git_config(workingdir, 'user.name', authorname)
        await git.git_config(workingdir, 'user.email', authoremail)
        await git.git_merge(workingdir, dstbranch, pr_head_branch)
        msg = get_merge_message(pullid, srcowner, srcbranch, content)
        await git.git_commit(workingdir, msg)
    except git.CanNotAutoMerge as e:
        await git.git_merge_action(workingdir, 'abort')
        flag_auto_merged = False
        output = e.args[0]
    except RuntimeError as e:
        raise e
    await git.git_fetch(dstroot, pr_merge_branch, workingdir, dstbranch)
    return flag_auto_merged, output


async def update_pull_request(dstowner: str, dstrepo: str, pullid: int):
    info = await get_pull_request_info(dstowner, dstrepo, pullid)
    dstbranch = info['dest_branch']
    src_repo_id = info['src_repo_id']
    src_owner_id = await repo.get_owner_id(src_repo_id)
    srcowner = info['']
    srcrepo = None
    srcbranch = info['src_branch']


async def merge_pull_request_git(dstowner: str, dstrepo: str, pullid: int):
    dstbranch = ""
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


async def pull_request_diff(dstowner: str, dstrepo: str,  pullid: int) -> List[Tuple[str, str]]:
    info = await get_pull_request_info(dstowner, dstrepo, pullid)
    if info is None:
        raise ValueError('PullRequest Not Found')
    dstbranch = info['dest_branch']
    workingdir = await get_working_dir(dstowner, dstrepo, pullid)
    pr_head_branch = 'refs/pull/{}/head'.format(pullid)
    result = await git.git_diff(workingdir, dstbranch, pr_head_branch)
    return result


async def pull_request_log(dstowner: str, dstrepo: str,  pullid: int) -> List[Dict[str, str]]:
    info = await get_pull_request_info(dstowner, dstrepo, pullid)
    if info is None:
        raise ValueError('PullRequest Not Found')
    dstbranch = info['dest_branch']
    pr_head_branch = 'refs/pull/{}/head'.format(pullid)
    result = await git.git_commit_logs(dstowner, dstrepo, pr_head_branch,
                                       pretty=git.MEDIUM, base=dstbranch)
    return result


async def pull_request_preview(dstowner: str, dstrepo: str, dstbranch: str,
                               srcowner: str, srcrepo: str, srcbranch: str) -> Dict[str, ...]:
    if dstowner != srcowner or dstrepo != srcrepo:
        dstroot = git.get_repo_dirpath(dstowner, dstrepo)
        srcroot = git.get_repo_dirpath(srcowner, srcrepo)
        await git.git_fetch(dstroot, 'FETCH_HEAD', srcroot, srcbranch, fetch_head=True)
        srcbranch = 'FETCH_HEAD'
    result = {}
    result['log'] = await git.git_commit_logs(dstowner, dstrepo, 'FETCH_HEAD',
                                              pretty=git.MEDIUM, base=dstbranch)
    result['diff'] = await git.git_diff(dstroot, dstbranch, srcbranch)
    return result
