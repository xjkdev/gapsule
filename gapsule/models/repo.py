from typing import List, Tuple, Dict
import os
from logging import warning
from gapsule.utils.log_call import log_call
from gapsule.models import git
from gapsule.utils.cookie_session import datetime_now
from gapsule.models.connection import _connection, fetchrow, execute, fetch
from gapsule.utils.check_validity import check_username_validity, check_reponame_validity
from gapsule.models.user import get_uid


class RepoNotFoundException(FileNotFoundError):
    pass


@log_call()
async def creat_new_repo(owner, reponame, introduction='', star_num=0, fork_num=0, visibility=False, forked_from='', default_branch=''):
    # 创建一个新repo，必须提供owner名和repo名
    if(check_reponame_validity(reponame) == False):
        raise NameError('Invalid reponame')
    flag = await check_repo_existing(owner, reponame)
    if(flag == False):
        await execute(
            '''
                INSERT INTO repos(username,reponame,introduction,create_time,star_num,fork_num,visibility,default_branch)
                VALUES($1,$2,$3,$4,$5,$6,$7,$8,$9)
            ''', owner, reponame, introduction, datetime_now(), star_num, fork_num, visibility, forked_from, default_branch
        )
    else:
        raise NameError('Repo already exists')


@log_call()
async def check_repo_existing(owner, reponame):
    # 检查一个repo是否存在，返回bool
    temp = await fetchrow(
        '''
        SELECT username FROM repos
        WHERE username = $1 AND reponame = $2''', owner, reponame
    )
    if(temp != None):
        return True
    else:
        return False


@log_call()
async def endow_read_permission(owner, reponame, username_permitted):
    if(await check_repo_existing(owner, reponame) == True):
        await execute(
            '''
                INSERT INTO read_permission(repo_id,username)
                VALUES($1,$2)
            ''', await get_repo_id(owner, reponame), username_permitted
        )
    else:
        raise RepoNotFoundException()


@log_call()
async def remove_read_permission(owner, reponame, username_to_remove):
    if(await check_repo_existing(owner, reponame) == True):
        await execute(
            '''
                delete from read_permission
                where repo_id=$1 and username=$2
            ''', await get_repo_id(owner, reponame), username_to_remove
        )
    else:
        raise RepoNotFoundException()


@log_call()
async def endow_admin_permission(owner, reponame, username_permitted):
    if(await check_repo_existing(owner, reponame) == True):
        await execute(
            '''
                INSERT INTO admin_permission(repo_id,username)
                VALUES($1,$2)
            ''', await get_repo_id(owner, reponame), username_permitted
        )
    else:
        raise RepoNotFoundException()


@log_call()
async def remove_admin_permission(owner, reponame, username_to_remove):
    if(await check_repo_existing(owner, reponame) == True):
        await execute(
            '''
                delete from admin_permission
                where repo_id=$1 and username=$2
            ''', await get_repo_id(owner, reponame), username_to_remove
        )
    else:
        raise RepoNotFoundException()


@log_call()
async def check_read_permission(owner, reponame, username=None):
    if(await check_repo_existing(owner, reponame) == True):
        if await get_repo_visibility(owner, reponame) == True:
            return True
        else:
            temp = await fetchrow(
                '''
                    SELECT username FROM read_permission
                    WHERE repo_id=$1 and username=$2
                ''', await get_repo_id(owner, reponame), username
            )
            if temp != None:
                return True
            else:
                return False
    else:
        raise RepoNotFoundException()


def get_commits_num(owner, repo, branch):
    """ 查询 repo的提交次数commits """
    return len(git.git_commit_logs(owner, repo, branch, pretty=git.ONELINE))

# 修改 repo的提交次数commits
@log_call(warning)
def set_commits_num(new_num):
    print('commits_num set as'+str(new_num)+' successfully')
    return True


def get_branches_num(owner, repo):
    """ 查询  repo的分支数branch """
    return len(git.git_branches(owner, repo)[1])


@log_call()
async def check_write_permission(owner, reponame, username):
    if(await check_repo_existing(owner, reponame) == True):
        temp = await fetchrow(
            '''
        SELECT username FROM admin_permission
        WHERE repo_id=$1 and username=$2
        ''', await get_repo_id(owner, reponame), username
        )
        if temp != None:
            return True
        else:
            temp2 = await fetchrow(
                '''
                SELECT collaborator FROM collaborate
                WHERE repo_id=$1 and username=$2
                ''', await get_repo_id(owner, reponame), username
            )
            if temp2 != None:
                return True
            else:
                return False
    else:
        raise RepoNotFoundException()


@log_call()
async def check_admin_permission(owner, reponame, username):
    if(await check_repo_existing(owner, reponame) == True):
        temp = await fetchrow(
            '''
                    SELECT username FROM admin_permission
                    WHERE repo_id=$1 and username=$2
            ''', await get_repo_id(owner, reponame), username
        )
        if temp != None:
            return True
        else:
            return False
    else:
        raise RepoNotFoundException()


@log_call()
async def delete_repo(owner, reponame):
    # 删除一个repo
    if(await check_repo_existing(owner, reponame) == True):
        await execute(
            '''
                DELETE FROM repos
                WHERE username=$1 and reponame=$2
            ''', owner, reponame
        )
    else:
        raise RepoNotFoundException()


@log_call()
async def add_collaborator(owner, reponame, collaborator_name):
    # 为一个repo加入一位collaborator
    if(await check_repo_existing(owner, reponame) == True):
        await execute(
            '''
                INSERT INTO collaborate(repo_id,collaborator)
                VALUES($1,$2)
            ''', await get_repo_id(owner, reponame), collaborator_name
        )
    else:
        raise RepoNotFoundException()


@log_call()
async def remove_collaborator(owner, reponame, collaborator_name):
    # 从一个repo里删除一个collaborator
    if(await check_repo_existing(owner, reponame) == True):
        await execute(
            '''
                    delete from collaborate
                    where repo_id=$1 and collaborator=$2
                ''', await get_repo_id(owner, reponame), collaborator_name
        )
    else:
        raise RepoNotFoundException()


def get_releases_num():
    return 0


@log_call()
async def get_repo_names(owner):
    # 查询一个用户所有的repo名，返回repo名列表
    names = await fetch(
        '''
            SELECT reponame FROM repos
            WHERE username=$1
        ''', owner
    )
    results = []
    for name in names:
        print(name['reponame'])
        results.append(name['reponame'])
    return results


@log_call()
async def alter_repo_name(owner, old_reponame, new_reponame):
    # 改repo名
    if(await check_repo_existing(owner, old_reponame) == True):
        if(check_reponame_validity(new_reponame) == True):
            await execute(
                '''
                UPDATE repos
                SET reponame = $1
                WHERE reponame = $2 and username = $3;
                ''', new_reponame, old_reponame, owner
            )
            return True
        else:
            raise NameError('invalid new_reponame')
    else:
        raise RepoNotFoundException()


@log_call()
async def get_repo_id(owner, reponame):
    # 根据owner名和repo名查该repo的id
    if(await check_repo_existing(owner, reponame) == True):
        result = await fetchrow(
            '''
                SELECT repo_id FROM repos
                WHERE  username=$1 and reponame=$2
            ''', owner, reponame
        )
        print(result['repo_id'])
        return result['repo_id']
    else:
        raise RepoNotFoundException()


async def get_owner_id(repo_id):
    temp = await fetchrow(
        '''
            SELECT username FROM repos
            WHERE repo_id=$1
        ''', repo_id
    )
    result = get_uid(temp['username'])
    return result


async def set_default_branch(owner, reponame, new_default_branch):
    if(await check_repo_existing(owner, reponame) == True):
        await execute(
            '''
                UPDATE repos
                SET    default_branch=$1
            ''', new_default_branch
        )
    else:
        raise RepoNotFoundException()


async def get_default_branch(owner, reponame):
    if(await check_repo_existing(owner, reponame) == True):
        await fetchrow(
            '''
                SELECT default_branch FROM repos
                 WHERE  username=$1 and reponame=$2
            ''', owner, reponame
        )
    else:
        raise RepoNotFoundException()


async def get_forked_from(owner, reponame):
    if(await check_repo_existing(owner, reponame) == True):
        await fetchrow(
            '''
                SELECT forked_from FROM repos
                 WHERE  username=$1 and reponame=$2
            ''', owner, reponame
        )
    else:
        raise RepoNotFoundException()


@log_call()
async def get_repo_introduction(owner, reponame):
    # 根据owner名和repo名查该repo的introduction
    if(await check_repo_existing(owner, reponame) == True):
        result = await fetchrow(
            '''
                SELECT introduction FROM repos
                WHERE  username=$1 and reponame=$2
            ''', owner, reponame
        )
        return result['introduction']
    else:
        raise RepoNotFoundException()


@log_call()
async def set_repo_introduction(owner, reponame, new_introduction):
    if(await check_repo_existing(owner, reponame) == True):
        await execute(
            '''
                UPDATE  repos
                SET     introduction=$1
                WHERE   username=$2 and reponame=$3
            ''', new_introduction, owner, reponame
        )
    else:
        raise RepoNotFoundException()


def get_specified_path(owner, reponame, branch, path=None) -> List[Tuple[str, str, bool]]:
    """ 查询  对应版本对应路径下的某个文件夹包含的文件夹（名称）和文件（名称）
        返回三元组，分别为name, hash, is_dir
    """
    return git.git_ls_files(owner, reponame, branch, path=path, show_tree=True)


@log_call()
async def get_repo_star_num(owner, reponame):
    # 根据owner名和repo名查该repo的star数
    if(await check_repo_existing(owner, reponame) == True):
        result = await fetchrow(
            '''
                SELECT star_num FROM repos
                WHERE username=$1 and reponame=$2
            ''', owner, reponame
        )
        return result['star_num']
    else:
        raise RepoNotFoundException()


@log_call()
async def inc_repo_star_num(owner, reponame):
    if(await check_repo_existing(owner, reponame) == True):
        new_num = await get_repo_star_num(owner, reponame)+1
        await execute(
            '''
                UPDATE  repos
                SET     star_num=$1
                WHERE   username=$2 and reponame=$3
            ''', new_num, owner, reponame
        )
    else:
        raise RepoNotFoundException()


@log_call()
async def get_repo_fork_num(owner, reponame):
    # 根据owner名和repo名查该repo的fork数
    if(await check_repo_existing(owner, reponame) == True):
        result = await fetchrow(
            '''
                SELECT fork_num FROM repos
                WHERE username=$1 and reponame=$2
            ''', owner, reponame
        )
        return result['fork_num']
    else:
        raise RepoNotFoundException()


@log_call()
async def inc_repo_fork_num(owner, reponame):
    if(await check_repo_existing(owner, reponame) == True):
        new_num = await get_repo_fork_num(owner, reponame)+1
        await execute(
            '''
                UPDATE  repos
                SET     fork_num=$1
                WHERE   username=$2 and reponame=$3
            ''', new_num, owner, reponame
        )
    else:
        raise RepoNotFoundException()


@log_call()
async def get_repo_visibility(owner, reponame):
    # 根据owner名和repo名查该repo是public(True)的还是private(False)的
    if(await check_repo_existing(owner, reponame)):
        result = await fetchrow(
            '''
                SELECT visibility FROM repos
                WHERE username=$1 and reponame=$2
            ''', owner, reponame
        )
        return result['visibility']
    else:
        raise RepoNotFoundException()


def get_file_content(path, branch=None):
    return 'content:...'


def get_all_files(owner, reponame, branch) -> List[Tuple[str, str]]:
    """ 查询  所有仓库文件 """
    return git.git_ls_files(owner, reponame, branch)


def path_exists(owner, reponame, branch, path) -> bool:
    """ 查询  对应路径的文件（夹）是否存在 """
    files = git.git_ls_files(owner, reponame, branch, show_tree=True)
    files = [info[0] for info in files]
    path = path.rstrip('/')
    return path in files


def get_history(owner, reponame, branch) -> List[Dict[str, str]]:
    """ 查询 历史提交的版本与时间 """
    return git.git_commit_logs(owner, reponame, branch, pretty=git.MEDIUM)


def get_contributors_info():
    return 0
