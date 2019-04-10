from datetime import datetime
from gapsule.utils.log_call import log_call
from gapsule.models.connection import _connection, fetchrow, execute, fetch
from gapsule.utils.check_validity import check_username_validity, check_reponame_validity


class RepoNotFoundException(FileNotFoundError):
    pass


@log_call()
async def creat_new_repo(owner, reponame, introduction='', star_num=0, fork_num=0, visibility=False):
    # 创建一个新repo，必须提供owner名和repo名
    if(check_reponame_validity(reponame) == False):
        raise NameError('Invalid reponame')
    flag = await check_repo_existing(owner, reponame)
    if(flag == False):
        await execute(
            '''
                INSERT INTO repos(username,reponame,introduction,create_time,star_num,fork_num,visibility)
                VALUES($1,$2,$3,$4,$5,$6,$7)
            ''', owner, reponame, introduction, datetime.now(), star_num, fork_num, visibility
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
