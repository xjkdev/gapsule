import re


def check_reponame_validity(reponame):
    if len(reponame) < 4 or len(reponame) > 20:
        return False
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]+$', reponame):
        return False
    return True


def check_username_validity(username):
    if len(username) < 4 or len(username) > 20:
        return False
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]+$', username):
        return False
    return True


def check_mail_validity(mail_address):
    if len(mail_address) == 0 or len(mail_address) > 40:
        return False
    if not re.match(r'^([A-Za-z0-9_\.-])+\@([A-Za-z0-9_\.-])+\.([A-Za-z]{2,8})$', mail_address):
        return False
    return True


def check_password_validity(password):
    if len(password) < 8 or len(password) == 0 or len(password) > 40:
        return False
    if not re.search('[A-Z]+', password):
        return False
    if not re.search('[0-9]+', password):
        return False
    if not re.match(r'^([a-zA-Z0-9_])+$', password):
        return False
    return True
