import functools
import crypt
import re
import asyncpg
import asyncio
from gapsule import models
from gapsule.utils.log_call import log_call


def check_username_validity(username):
    if(len(username) == 0 | len(username) > 20):
        return False
    if not (re.match('([a-z]|[A-Z]|[0-9]|_)+', username)):
        return False
    return True


def check_mail_validity(mail_address):
    if(len(mail_address) == 0 | len(mail_address) > 40):
        return False
    if not (re.match(r'([a-z]|[A-Z]|[0-9]|_|\.)*?@.+', mail_address)):
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
def check_session_status(username, session, logged_time):
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
