import re


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
