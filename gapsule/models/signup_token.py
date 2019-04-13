_token_to_check = []


def append_token(item):
    _token_to_check.append(item)


def check_token(username, password, token):
    for info in _token_to_check:
        if (info['username'] == username and info['password'] == password
                and info['token'] == token):
            return True
    return False


def get_pending_email(username):
    for info in _token_to_check:
        if info['username'] == username:
            return info['email']
    return None


def remove_token(username):
    for info in _token_to_check:
        if info['username'] == username:
            _token_to_check.remove(info)
