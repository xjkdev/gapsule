from gapsule.utils.cookie_session import datetime_now
from gapsule.utils.log_call import log_call
from gapsule.models.repo import get_repo_id, check_repo_existing
from gapsule.models.connection import fetch, fetchrow, execute
from gapsule.models.notification import create_new_notification
from gapsule.models.user import get_uid


class PostNotFoundException(FileNotFoundError):
    pass


class CommentNotFoundException(FileNotFoundError):
    pass


@log_call()
async def create_new_attached_post(repo_id: int,
                                   postername: str,
                                   title: str,
                                   status: str,
                                   visibility: bool,
                                   is_issue: bool = True):
    current_id = await fetchrow(
        '''
        SELECT max(post_id) FROM posts
        WHERE repo_id=$1
        ''', repo_id)
    this_id = 1
    if current_id['max'] is not None:
        this_id = current_id['max'] + 1

    await execute(
        '''
        INSERT INTO posts(post_id,repo_id,is_issue,postername,title,status,visibility,post_time)
        VALUES($1,$2,$3,$4,$5,$6,$7,$8)
        ''', this_id, repo_id, is_issue, postername, title, status, visibility,
        datetime_now())
    return this_id


@log_call()
async def create_new_nonattached_post(postername: str, title: str, status: str,
                                      visibility: bool):
    this_id = await create_new_attached_post(0, postername, title, status,
                                             visibility)
    return this_id


@log_call()
async def check_post_existing(repo_id: int, post_id: int):
    temp = await fetchrow(
        '''
        SELECT * FROM posts
        WHERE repo_id=$1 and post_id=$2
        ''', repo_id, post_id)
    if temp:
        return True
    else:
        return False


@log_call()
async def get_all_posts_of_poster(postername: str):
    temps = await fetch(
        '''
        SELECT * FROM posts
        WHERE postername=$1
        ''', postername)
    results = [dict(temp) for temp in temps]
    return results


@log_call()
async def get_postername(repo_id: int, post_id: int):
    result = await fetchrow(
        '''
        SELECT postername FROM posts
        WHERE repo_id=$1 and post_id=$2
        ''', repo_id, post_id)
    return result['postername']


@log_call()
async def get_title(repo_id: int, post_id: int):
    result = await fetchrow(
        '''
        SELECT title FROM posts
        WHERE repo_id=$1 and post_id=$2
        ''', repo_id, post_id)
    return result['title']


@log_call()
async def get_status(repo_id: int, post_id: int):
    result = await fetchrow(
        '''
        SELECT status FROM posts
        WHERE repo_id=$1 and post_id=$2
        ''', repo_id, post_id)
    return result['status']


@log_call()
async def alter_status(repo_id: int, post_id: int, new_status: str):
    await execute(
        '''
        UPDATE posts
        SET status=$1
        WHERE repo_id=$2 and post_id=$3
        ''', new_status, repo_id, post_id)


@log_call()
async def get_visibility(repo_id: int, post_id: int):
    result = await fetchrow(
        '''
        SELECT visibility FROM posts
        WHERE repo_id=$1 and post_id=$2
        ''', repo_id, post_id)
    return result['visibility']


@log_call()
async def create_new_comment(repo_id: int, post_id: int, type: str,
                             content: str, commenter_name: str):
    if await check_post_existing(repo_id, post_id):
        current_id = await fetchrow(
            '''
        SELECT max(comment_id) FROM comments
        WHERE repo_id=$1 and post_id=$2
        ''', repo_id, post_id)
        this_id = 1
        if current_id['max'] != None:
            this_id = current_id['max'] + 1
        await execute(
            '''
                INSERT INTO comments(post_id,repo_id,comment_id,is_reply,reply_to_id,address_time,type,content,commenter)
                VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)
                ''', post_id, repo_id, this_id, False, None, datetime_now(),
            type, content, commenter_name)

        notification = commenter_name+' commented your post (id: ' + \
            str(repo_id)+'_'+str(post_id)+')'
        poster = await get_postername(repo_id, post_id)
        poster_id = await get_uid(poster)
        await create_new_notification(poster_id, notification)

        return this_id
    else:
        raise PostNotFoundException()


@log_call()
async def create_new_reply(repo_id: int, post_id: int, reply_to_id: int,
                           type: str, content: str, replier_name: str):
    if await check_post_existing(repo_id, post_id):
        current_id = await fetchrow(
            '''
        SELECT max(comment_id) FROM comments
        WHERE repo_id=$1 and post_id=$2
        ''', repo_id, post_id)
        this_id = 1
        if current_id['max'] != None:
            this_id = current_id['max'] + 1
        await execute(
            '''
            INSERT INTO comments(post_id,repo_id,comment_id, is_reply,reply_to_id,address_time,type,content,commenter)
            VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)
            ''', post_id, repo_id, this_id, True, reply_to_id, datetime_now(),
            type, content, replier_name)

        notification = replier_name + ' replied to you'
        await create_new_notification(reply_to_id, notification)

        return this_id
    else:
        raise PostNotFoundException()


@log_call()
async def check_comment_existing(repo_id: int, post_id: int, comment_id: int):
    temp = await fetchrow(
        '''
        SELECT FROM comments
        WHERE repo_id=$1, post_id=$2, comment_id=$3
        ''', repo_id, post_id, comment_id)
    if temp:
        return True
    else:
        return False


@log_call()
async def delete_comment(repo_id: int, post_id: int, comment_id: int):
    if check_comment_existing(repo_id, post_id, comment_id):
        await execute(
            '''
            DELETE FROM comments
            WHERE repo_id=$1, post_id=$2, comment_id=$3
            ''', repo_id, post_id, comment_id)
    else:
        raise CommentNotFoundException()


async def get_all_attached_posts(repo_id: int):
    # 查询一个repo下所有的帖子id
    temps = await fetch(
        '''
            SELECT * FROM posts
            WHERE repo_id=$1
        ''', repo_id)
    results = [dict(temp) for temp in temps]
    return results


async def get_all_nonattached_posts():
    return await get_all_attached_posts(0)


async def get_all_issues(repo_id: int):
    temps = await fetch(
        '''
            SELECT * FROM posts
            WHERE repo_id=$1 and is_issue=$2
        ''', repo_id, True)
    results = [dict(temp) for temp in temps]
    return results


async def get_all_pull_requests(repo_id: int):
    temps = await fetch(
        '''
            SELECT * FROM posts
            WHERE repo_id=$1 and is_issue=$2
        ''', repo_id, False)
    results = [dict(temp) for temp in temps]
    return results


@log_call()
async def get_all_comments(repo_id: int, post_id: int):
    temps = await fetch(
        '''
            SELECT * FROM comments
            WHERE repo_id=$1 and post_id=$2
            ''', repo_id, post_id)
    results = [dict(temp) for temp in temps]
    return results
