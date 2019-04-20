from gapsule.utils.cookie_session import datetime_now, format_log_time
from gapsule.models import user
from gapsule.models.connection import fetchrow, execute, fetch


async def create_new_notification(username: str, content: str):
    current_id = await fetchrow(
        '''
        SELECT max(notification_id) FROM notifications
        WHERE username=$1
        ''', username)
    this_id = 1
    if current_id['max'] != None:
        this_id = current_id['max'] + 1
    await execute(
        '''
            INSERT INTO notifications(username,notification_id,created_time,content)
            VALUES($1,$2,$3,$4)
        ''', username, this_id, datetime_now(), content)
    return this_id


async def get_all_notifications(username: str):
    temps = await fetch(
        '''
            SELECT * FROM notifications
            WHERE username=$1 ORDER BY created_time DESC
        ''', username)
    results = []
    for temp in temps:
        result = {}
        result['user'] = temp['username']
        result['notification_id'] = temp['notification_id']
        result['created_time'] = format_log_time(temp['created_time'])
        result['content'] = temp['content']
        results.append(result)
    return results


async def delete_notification(notification_id: int):
    await execute(
        '''
        DELETE FROM notifications
        WHERE notification_id=$1
        ''', notification_id)
