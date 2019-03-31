import functools
import crypt
import re
import asyncpg
import asyncio
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


def check_un_validity(username):
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


def check_pw_validity(password):
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
    if (check_un_validity(username) == False):
        return False
    if (check_mail_validity(mail_address) == False):
        return False
    if(check_pw_validity(password) != False):
        temp = await models.connection.fetchrow(
            '''
            SELECT username FROM users_info
            WHERE username=$1
            ''',
            username
        )
        if(temp != None):
            raise NameError()
        else:
            encrypted_password = crypt.crypt(password, crypt.mksalt())
            await models.connection.execute(
                '''
                INSERT INTO users_info(username,mail_address,password) VALUES($1,$2,$3)
                ''', username, mail_address, encrypted_password
            )
            return True
    else:
        return False


@log_call
def verify_user(username, password):
    return True


@log_call
def alter_username(old_username, new_username):
    return True


@log_call
def creat_new_repo(reponame, description, visibility):
    return True


@log_call
def sign_out():
    return True
