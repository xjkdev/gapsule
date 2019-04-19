import hashlib
import random
import re
import secrets
import asyncpg
import asyncio
import functools
from gapsule import settings
from gapsule.models import signup_token
from gapsule.utils.cookie_session import datetime_now
from gapsule.utils.log_call import log_call
from gapsule.models.connection import fetchrow, execute, fetch
from gapsule.utils.check_validity import (check_mail_validity,
                                          check_password_validity,
                                          check_username_validity,
                                          check_reponame_validity)


@log_call()
def add_user_pending_verifying(username: str, mail_address: str,
                               password: str):
    if (check_username_validity(username) and check_mail_validity(mail_address)
            and check_password_validity(password)):
        pending_info = {}
        pending_info['username'] = username
        pending_info['email'] = mail_address
        pending_info['password'] = password
        pending_info['token'] = secrets.token_urlsafe(16)
        signup_token.append_token(pending_info)
        if not settings.settings['enable_email']:
            return pending_info['token']
        else:
            return None
    else:
        raise NameError()


@log_call()
async def check_user_existing(username: str):
    temp = await fetchrow(
        '''
        SELECT username FROM users_info
        WHERE username = $1
        ''', username)
    return temp is not None


async def get_user_mail_address(username: str):
    if check_user_existing(username):
        result = await fetchrow(
            '''
            SELECT mail_address FROM users_info
            WHERE username = $1
            ''', username)
        return result['mail_address']
    else:
        raise NameError("user does not exist")


@log_call()
async def check_profile_existing(username: str):
    temp = await fetchrow(
        '''
        SELECT username FROM profiles
        WHERE username =$1''', username)
    return temp is not None


@log_call()
async def create_new_user(username: str, mail_address: str, password: str):
    if not check_username_validity(username):
        return False
    if not check_mail_validity(mail_address):
        return False
    if (check_password_validity(password) != False):
        flag = await check_user_existing(username)
        if (flag == True):
            raise NameError('Username already existing')
        else:
            salt = username[random.randint(
                0,
                len(username) - 1)] + username[random.randint(
                    0,
                    len(username) - 1)] + username[random.randint(
                        0,
                        len(username) - 1)]
            sha512 = hashlib.sha512()
            temp = password + salt
            temp = temp.encode('utf-8')
            sha512.update(temp)
            encrypted_password = sha512.hexdigest()
            await execute(
                '''
            INSERT INTO users_info(username, mail_address, password, salt) VALUES($1, $2, $3, $4)''',
                username, mail_address, encrypted_password, salt)
            return True
    else:
        return False


async def get_user_info(username: str):
    result = await fetchrow(
        '''
        SELECT * FROM users_info
        WHERE username=$1
        ''', username)
    return dict(result)


@log_call()
async def verify_user(username: str, password: str):
    if not check_username_validity(username):
        return False
    if not check_password_validity(password):
        return False
    if (check_password_validity(password) != False):
        flag = await check_user_existing(username)
        if (flag == False):
            raise NameError('User does not exist')
        else:
            temp_salt = await fetchrow(
                '''
                SELECT salt FROM users_info
                WHERE username =$1
                ''', username)
            sha5122 = hashlib.sha512()
            temp = (password + temp_salt['salt']).strip()
            temp = temp.encode('utf-8')
            sha5122.update(temp)
            temp_encrypted_pw = sha5122.hexdigest()
            temp_password = await fetchrow(
                '''
                SELECT password FROM users_info
                WHERE username =$1
                ''', username)
            if (temp_encrypted_pw == temp_password['password']):
                return True
            else:
                return False
    else:
        return False


@log_call()
async def set_profile(username: str,
                      firstname: str,
                      lastname: str,
                      icon_path: str = None,
                      introduction: str = None,
                      company: str = None,
                      location: str = None,
                      public_email: str = None,
                      website: str = None):
    if not check_username_validity(username):
        return False
    flag = await check_user_existing(username)
    if not flag:
        raise NameError('User does not exist')
    else:
        flag = await check_profile_existing(username)
        if not flag:
            await execute(
                '''
                INSERT INTO profiles(username, icon_url,firstname,lastname, introduction, company, location,public_email, website) VALUES($1, $2, $3, $4, $5, $6,$7,$8,$9)
                ''', username, icon_path, firstname, lastname, introduction,
                company, location, public_email, website)
        else:
            await execute(
                '''
                UPDATE profiles
                SET lastname=$1, firstname=$2
                WHERE usernmae=$3
                ''', lastname, firstname, username)
            if icon_path != None:
                await execute(
                    '''
                    UPDATE profiles
                    SET icon_url=$1
                    WHERE username=$2
                    ''', icon_path, username)
            if introduction != None:
                await execute(
                    '''
                    UPDATE profiles
                    SET introduction=$1
                    WHERE username=$2
                    ''', introduction, username)
            if company != None:
                await execute(
                    '''
                    UPDATE profiles
                    SET company=$1
                    WHERE username=$2
                    ''', company, username)
            if location != None:
                await execute(
                    '''
                    UPDATE profiles
                    SET location=$1
                    WHERE username=$2
                    ''', location, username)
            if public_email != None:
                await execute(
                    '''
                    UPDATE profiles
                    SET public_email=$1
                    WHERE username=$2
                    ''', public_email, username)
            if website != None:
                await execute(
                    '''
                    UPDATE profiles
                    SET website=$1
                    WHERE username=$2
                    ''', website, username)
        return True


@log_call()
async def get_uid(username: str):
    uid = await fetchrow(
        '''
                SELECT uid FROM users_info
                WHERE username =$1
                ''', username)
    if uid is None:
        raise NameError()
    else:
        return uid['uid']


async def get_profile_info(username: str):
    temp = await fetchrow(
        '''
            SELECT * FROM profiles
            WHERE username=$1
        ''', username)
    result = dict(temp)
    return result


async def alter_username(old_username: str, new_username: str):
    if (check_username_validity(new_username) == False
            or check_username_validity(old_username) == False):
        raise NameError()
    else:
        flag = check_user_existing(old_username)
        if not flag:
            raise NameError('User not existing')
        else:
            await execute(
                '''
                    UPDATE users_info
                    SET username = $1
                    WHERE username = $2
                ''', new_username, old_username)
            await execute(
                '''
                    UPDATE profiles
                    SET username = $1
                    WHERE username = $2
                ''', new_username, old_username)
            await execute(
                '''
                    UPDATE log_info
                    SET username = $1
                    WHERE username = $2
                ''', new_username, old_username)
            await execute(
                '''
                    UPDATE repos
                    SET username = $1
                    WHERE username = $2
                ''', new_username, old_username)
            await execute(
                '''
                    UPDATE read_permission
                    SET username = $1
                    WHERE username = $2
                ''', new_username, old_username)
            await execute(
                '''
                    UPDATE admin_permission
                    SET username = $1
                    WHERE username = $2
                ''', new_username, old_username)
            return True


async def user_login(username: str, password: str):
    flag = await verify_user(username, password)
    if not flag:
        return False
    temp = await fetchrow(
        '''
    SELECT username FROM log_info
    WHERE username =$1''', username)
    if temp is not None:
        await execute(
            '''
        DELETE FROM log_info WHERE username=$1
        ''', username)
    session = secrets.token_urlsafe()
    await execute(
        '''
            INSERT INTO log_info(username,session,login_time) VALUES($1,$2,$3)
        ''', username, session, datetime_now())
    return session


@log_call()
async def user_logout(username: str):
    await execute(
        '''
            DELETE FROM log_info WHERE username=$1
            ''', username)


@log_call()
async def check_session_status(username: str, session: str):
    temp = await fetchrow(
        '''
        SELECT username, session FROM log_info
        WHERE username =$1
        ''', username)
    if temp is None:
        return False
    return (temp['username'] == username and temp['session'] == session)


async def get_last_login_time(username: str):
    temp = await fetchrow(
        '''
        SELECT login_time FROM log_info
        WHERE username=$1
        ''', username)
    return temp['login_time']
