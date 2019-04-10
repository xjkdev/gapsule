from gapsule.utils.cookie_session import datetime_now
from gapsule.utils.log_call import log_call
from gapsule.models.repo import get_repo_id, check_repo_existing
from gapsule.models.connection import fetch, fetchrow, execute

# post分为attached_post 和 nonattached_post，前者依附于一个repo，由repo_id和post_id标识。后者由0 (repo_id=0)+post_id标识


class PostNotFoundException(FileNotFoundError):
    pass


@log_call()
async def creat_new_attached_post(repo_id, postername, title, status, visibility):
    current_id = await fetchrow(
        '''
        SELECT max(post_id) FROM posts
        WHERE repo_id=$1
        ''', repo_id
    )
    this_id = 1
    if current_id['max'] != None:
        this_id = current_id['max']+1

    await execute(
        '''
        INSERT INTO posts(post_id,repo_id,postername,title,status,visibility,post_time)
        VALUES($1,$2,$3,$4,$5,$6,$7)
        ''', this_id, repo_id, postername, title, status, visibility, datetime_now()
    )
    return this_id


@log_call()
async def creat_new_nonattached_post(postername, title, status, visibility):
    this_id = await creat_new_attached_post(0, postername, title, status, visibility)
    return this_id


@log_call()
async def check_post_existing(repo_id, post_id):
    temp = await fetchrow(
        '''
        SELECT * FROM posts
        WHERE repo_id=$1 and post_id=$2
        ''', repo_id, post_id
    )
    if temp:
        return True
    else:
        return False


@log_call()
async def get_all_posts(postername):
    # 查一个用户发过的所有posts
    results = []
    temps = await fetch(
        '''
        SELECT * FROM posts
        WHERE postername=$1
        ''', postername
    )
    for temp in temps:
        result = {}
        result['repo_id'] = temp['repo_id']
        result['post_id'] = temp['post_id']
        result['postername'] = temp['postername']
        result['title'] = temp['title']
        result['status'] = temp['status']
        result['visibility'] = temp['visibility']
        result['post_time'] = temp['post_time']
        results.append(result)
    print(results)


@log_call()
async def get_postername(repo_id, post_id):
    result = await fetchrow(
        '''
        SELECT postername FROM posts
        WHERE repo_id=$1 and post_id=$2
        ''', repo_id, post_id
    )
    return result['postername']


@log_call()
async def get_title(repo_id, post_id):
    result = await fetchrow(
        '''
        SELECT title FROM posts
        WHERE repo_id=$1 and post_id=$2
        ''', repo_id, post_id
    )
    return result['title']


@log_call()
async def get_status(repo_id, post_id):
    result = await fetchrow(
        '''
        SELECT status FROM posts
        WHERE repo_id=$1 and post_id=$2
        ''', repo_id, post_id
    )
    return result['status']


@log_call()
async def alter_status(repo_id, post_id, new_status):
    await execute(
        '''
        UPDATE posts
        SET status=$1
        WHERE repo_id=$2 and post_id=$3
        ''', new_status, repo_id, post_id
    )


@log_call()
async def get_visibility(repo_id, post_id):
    result = await fetchrow(
        '''
        SELECT visibility FROM posts
        WHERE repo_id=$1 and post_id=$2
        ''', repo_id, post_id
    )
    return result['visibility']
