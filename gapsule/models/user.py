import crypt
import re
import asyncpg
import asyncio
import functools
from gapsule import models


def log_call(f, log_func=None):
    if log_func is None:
        log_func = print

    @functools.wraps(f)
    def _wrapper(*args, **kwargs):
        nonlocal log_func
        name = f.__name__ if hasattr(f, '__name__') else '<Anonymous Function>'
        sarg = ', '.join(str(a) for a in args)
        skarg = ', '.join('%s=%s' % (k, v) for k, v in kwargs.items())
        if len(skarg) > 0:
            tmp = ', '.join((sarg, skarg))
        else:
            tmp = sarg
        result = f(*args, **kwargs)
        log_func('Function Called {}({}) -> {}'.format(
            name, tmp, str(result)))
        return result
    return _wrapper


def check_username_validity(username):
    if(len(username) == 0 | len(username) > 20):
        return False
    if not (re.match('([a-z]|[A-Z]|[0-9]|_)+', username)):
        return False
    return True


def check_mail_validity(mail_address):
    if(len(mail_address) == 0 | len(mail_address) > 40):
        return False
    if not (re.match('([a-z]|[A-Z]|[0-9]|_|\.)*?@.+', mail_address)):
        return False
    return True


def check_password_validity(password):
    if(len(password) < 8 | len(password) == 0 | len(password) > 40):
        return False
    if not (re.search('[A-Z]+', password)):
        return False
    if not (re.search('[0-9]+', password)):
        return False
    if not (re.match('([a-z]|[A-Z]|[0-9]|_)+', password)):
        return False
    return True


@log_call
async def create_new_user(username, mail_address, password):
    if (check_username_validity(username) == False):
        return False
    if (check_mail_validity(mail_address) == False):
        return False
    if(check_password_validity(password) != False):
        temp = await models.connection.fetchrow(
            '''
        SELECT username FROM users_info
        WHERE username =$1''', username
        )
        if(temp != None):
            raise NameError()
        else:
            salt = crypt.mksalt()
            encrypted_password = crypt.crypt(password, salt)
            await models.connection.execute(
                '''
            INSERT INTO users_info(username, mail_address, password, salt) VALUES($1, $2, $3, $4)''', username, mail_address, encrypted_password, salt
            )
            return True
    else:
        return False


@log_call
async def verify_user(username, password):
    if (check_username_validity(username) == False):
        return False
    if(check_password_validity(password) != False):
        temp_name = await models.connection.fetchrow(
            '''
            SELECT username FROM users_info
            WHERE username =$1
            ''',
            username
        )
        if(temp_name == None):
            raise NameError()
        else:
            temp_salt = await models.connection.fetchrow(
                '''
                SELECT salt FROM users_info
                WHERE username =$1
                ''',
                username
            )
            temp_encrypted_pw = crypt.crypt(password, salt=temp_salt['salt'])
            print(temp_encrypted_pw)
            temp_password = await models.connection.fetchrow(
                '''
                SELECT password FROM users_info
                WHERE username =$1
                ''',
                username
            )
            if(temp_encrypted_pw == temp_password['password']):
                print('ok')
                return True
            else:
                print('no')
                return False


@log_call
async def set_profile(username, icon_url, introduction):
    if (check_username_validity(username) == False):
        return False
    else:
        temp_name = await models.connection.fetchrow(
            '''
        SELECT username FROM users_info
        WHERE username =$1
            ''',
            username
        )
        if(temp_name == None):
            raise NameError()
        else:
            temp_name = await models.connection.fetchrow(
                '''
            SELECT username FROM profiles
            WHERE username =$1
            ''',
                username
            )
            if(temp_name == None):
                await models.connection.execute(
                    '''
                    INSERT INTO profiles(username, icon_url, introduction) VALUES($1, $2, $3)
                    ''', username, icon_url, introduction
                )
            else:
                await models.connection.execute(
                    '''
                    UPDATE profiles
                    SET icon_url = $1, introduction = $2
                    ''', icon_url, introduction
                )  # update
            return True


@log_call
async def get_icon_url(username):
    url = await models.connection.fetchrow(
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


@log_call
async def get_introduction(username):
    url = await models.connection.fetchrow(
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
