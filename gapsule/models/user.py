import crypt
import re
import secrets
import asyncpg
import asyncio
import functools
from gapsule import models
from gapsule.utils.cookie_session import datetime_now
from gapsule.utils.log_call import log_call
from gapsule.models.connection import _connection, fetchrow, execute, fetch
from gapsule.utils.check_validity import check_mail_validity, check_password_validity, check_username_validity, check_reponame_validity


@log_call()
def add_user_pending_verifying(username, mail_address, password):
    # 返回一个随机的token，并将验证信息加入pending_info
    if(check_username_validity(username) == True and check_mail_validity(mail_address) == True):
        pending_info = {}
        pending_info['username'] = username
        pending_info['mail_address'] = mail_address
        pending_info['password'] = password
        pending_info['token'] = secrets.token_urlsafe(16)
        models.signup_token.append_token(pending_info)
        return pending_info['token']


@log_call()
async def check_user_existing(username):
    # user是否存在
    temp = await fetchrow(
        '''
        SELECT username FROM users_info
        WHERE username = $1
        ''', username
    )
    if(temp != None):
        return True
    else:
        return False


@log_call()
async def check_profile_existing(username):
    temp = await fetchrow(
        '''
        SELECT username FROM profiles
        WHERE username =$1''', username
    )
    if(temp != None):
        return True
    else:
        return False


@log_call()
async def create_new_user(username, mail_address, password):
    if (check_username_validity(username) == False):
        return False
    if (check_mail_validity(mail_address) == False):
        return False
    if(check_password_validity(password) != False):
        flag = await check_user_existing(username)
        if(flag == True):
            raise NameError('Username already existing')
        else:
            salt = crypt.mksalt()
            encrypted_password = crypt.crypt(password, salt)
            await execute(
                '''
            INSERT INTO users_info(username, mail_address, password, salt) VALUES($1, $2, $3, $4)''', username, mail_address, encrypted_password, salt
            )
            return True
    else:
        return False


@log_call()
async def verify_user(username, password):
    if (check_username_validity(username) == False):
        return False
    if(check_password_validity(password) != False):
        flag = check_user_existing(username)
        if(flag == False):
            raise NameError('User does not exist')
        else:
            temp_salt = await fetchrow(
                '''
                SELECT salt FROM users_info
                WHERE username =$1
                ''',
                username
            )
            temp_encrypted_pw = crypt.crypt(password, salt=temp_salt['salt'])
            temp_password = await fetchrow(
                '''
                SELECT password FROM users_info
                WHERE username =$1
                ''',
                username
            )
            if(temp_encrypted_pw == temp_password['password']):
                return True
            else:
                return False


@log_call()
async def set_profile(username, icon_url=None, introduction=None, company=None, location=None, website=None):
    if (check_username_validity(username) == False):
        return False
    else:
        flag = check_user_existing(username)
        if(flag == False):
            raise NameError('User does not exist')
        else:
            flag = check_profile_existing(username)
            if(flag == False):
                await execute(
                    '''
                    INSERT INTO profiles(username, icon_url, introduction, company, location, website) VALUES($1, $2, $3, $4, $5, $6)
                    ''', username, icon_url, introduction, company, location, website
                )
            else:
                await execute(
                    '''
                    UPDATE profiles
                    SET icon_url = $1, introduction = $2
                    WHERE username = $3
                    ''', icon_url, introduction, username
                )
            return True


@log_call()
async def get_uid(username):
    uid = await fetchrow(
        '''
                SELECT uid FROM users_info
                WHERE username =$1
                ''',
        username
    )
    if (uid == None):
        raise NameError()
    else:
        return uid['uid']


@log_call()
async def get_icon_url(username):
    url = await fetchrow(
        '''
                SELECT icon_url FROM profiles
                WHERE username =$1
                ''',
        username
    )
    if (url == None):
        raise NameError()
    else:
        return url['icon_url']


@log_call()
async def get_introduction(username):
    url = await fetchrow(
        '''
                SELECT introduction FROM profiles
                WHERE username =$1
                ''',
        username
    )
    if (url == None):
        raise NameError()
    else:
        return url['introduction']


async def alter_username(old_username, new_username):
    if(check_username_validity(new_username) == False or check_username_validity(old_username) == False):
        raise NameError()
    else:
        flag = check_user_existing(old_username)
        if(flag == False):
            raise NameError('User not existing')
        else:
            await execute(
                '''
                    UPDATE users_info
                    SET username = $1
                    WHERE username = $2
                ''', new_username, old_username
            )
            await execute(
                '''
                    UPDATE profiles
                    SET username = $1
                    WHERE username = $2
                ''', new_username, old_username
            )
            await execute(
                '''
                    UPDATE log_info
                    SET username = $1
                    WHERE username = $2
                ''', new_username, old_username
            )
            await execute(
                '''
                    UPDATE repos
                    SET username = $1
                    WHERE username = $2
                ''', new_username, old_username
            )
            return True


@log_call()
async def alter_icon(username, new_url):
    await execute(
        '''
            UPDATE  profiles
            SET icon_url = $1
            WHERE username = $2
        ''', new_url, username
    )
    return True


@log_call()
async def alter_introduction(username, new_intro):
    await execute(
        '''
            UPDATE  profiles
            SET introduction = $1
            WHERE username = $2
        ''', new_intro, username
    )
    return True


async def user_login(username, password):
    flag = await verify_user(username, password)
    if(flag == True):
        temp = await models.connection.fetchrow(
            '''
        SELECT username FROM log_info
        WHERE username =$1''', username
        )
        if(temp != None):
            await models.connection.execute(
                '''
            DELETE FROM log_info WHERE username=$1
            ''', username)
        session = secrets.token_urlsafe()
        await models.connection.execute(
            '''
                INSERT INTO log_info(username,session,login_time) VALUES($1,$2,$3)
            ''', username, session, datetime_now()
        )
        return session
    else:
        return False


@log_call()
async def user_logout(username):
    await models.connection.execute(
        '''
            DELETE FROM log_info WHERE username=$1
            ''', username)


@log_call()
async def check_session_status(username, session):
    temp = await models.connection.fetchrow(
        '''
        SELECT username, session FROM log_info
        WHERE username =$1
        ''', username
    )
    if(temp == None):
        return False
    else:
        if(temp['username'] == username and temp['session'] == session):
            return True
        else:
            return False
