from datetime import datetime
from gapsule.utils.log_call import log_call
from gapsule.models.connection import fetch, fetchrow, execute
from gapsule.models.post import check_post_existing, PostNotFoundException

# 一个post（帖子）下的所有跟帖都是comment。reply是特殊的comment。


class CommentNotFoundException(FileNotFoundError):
    pass


@log_call()
async def create_new_comment(repo_id, post_id, type, content, commenter_name):
    if await check_post_existing(repo_id, post_id):
        current_id = await fetchrow(
            '''
        SELECT max(comment_id) FROM comments
        WHERE repo_id=$1
        ''', repo_id
        )
        this_id = 1
        if current_id['max'] != None:
            this_id = current_id['max']+1
        await execute(
            '''
                INSERT INTO comments(post_id,repo_id,comment_id,is_reply,reply_to,address_time,type,content,conmmenter)
                VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)
                ''', post_id, repo_id, this_id, False, None, datetime.now(), type, content, commenter_name
        )
        return this_id
    else:
        raise PostNotFoundException()


@log_call()
async def create_new_reply(repo_id, post_id, reply_to_name, type, content, replier_name):
    if await check_post_existing(repo_id, post_id):
        current_id = await fetchrow(
            '''
        SELECT max(comment_id) FROM comments
        WHERE repo_id=$1
        ''', repo_id
        )
        this_id = 1
        if current_id['max'] != None:
            this_id = current_id['max']+1
        await execute(
            '''
            INSERT INTO comments(post_id,repo_id,comment_id, is_reply,reply_to,address_time,type,content,conmmenter)
            VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)
            ''', post_id, repo_id, this_id, True, reply_to_name, datetime.now(), type, content, replier_name
        )
        return this_id
    else:
        raise PostNotFoundException()


@log_call()
async def check_comment_existing(repo_id, post_id, comment_id):
    temp = await fetchrow(
        '''
        SELECT FROM comments
        WHERE repo_id=$1, post_id=$2, comment_id=$3
        ''', repo_id, post_id, comment_id
    )
    if temp:
        return True
    else:
        return False


@log_call()
async def delete_comment(repo_id, post_id, comment_id):
    if check_comment_existing(repo_id, post_id, comment_id):
        await execute(
            '''
            DELETE FROM comments
            WHERE repo_id=$1, post_id=$2, comment_id=$3
            ''', repo_id, post_id, comment_id
        )
    else:
        raise CommentNotFoundException()


@log_call()
async def get_comment_info(repo_id, post_id, comment_id):
    # 根据三个id得到对应commnet的信息
    if check_comment_existing(repo_id, post_id, comment_id):
        temp = await fetchrow(
            '''
            SELECT * FROM comments
            WHERE repo_id=$1, post_id=$2, comment_id=$3
            ''', repo_id, post_id, comment_id
        )
        result = {}
        result['post_id'] = temp['post_id']
        result['repo_id'] = temp['repo_id']
        result['comment_id'] = temp['comment_id']
        result['is_reply'] = temp['is_reply']
        result['reply_to'] = temp['reply_to']
        result['address_time'] = temp['address_time']
        result['type'] = temp['type']
        result['content'] = temp['content']
        result['conmmenter'] = temp['conmmenter']
        return result
    else:
        raise CommentNotFoundException()
