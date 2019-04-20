from gapsule.utils.cookie_session import datetime_now
from gapsule.models.connection import fetchrow, execute, fetch


async def create_new_notification(user_id: int, content: str):
    current_id = await fetchrow(
        '''
        SELECT max(notification_id) FROM notifications
        WHERE user_id=$1
        ''', user_id)
    this_id = 1
    if current_id['max'] != None:
        this_id = current_id['max'] + 1
    await execute(
        '''
            INSERT INTO notifications(user_id,notification_id,created_time,content)
            VALUES($1,$2,$3,$4)
        ''', user_id, this_id, datetime_now(), content)
    return this_id


async def get_all_notifications(user_id: int):
    temps = await fetch(
        '''
            SELECT * FROM notifications
            WHERE user_id=$1
        ''', user_id)
    results = []
    for temp in temps:
        result = {}
        result['user_id'] = temp['user_id']
        result['notification_id'] = temp['notification_id']
        result['created_time'] = temp['created_time']
        result['content'] = temp['content']
        results.append(result)
    return results


async def delete_notification(notification_id: int):
    await execute(
        '''
        DELETE FROM notifications
        WHERE notification_id=$1
        ''', notification_id)
