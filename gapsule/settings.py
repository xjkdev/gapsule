import os
import warnings
import configparser

settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
)


def read_config():
    config = configparser.ConfigParser()
    if os.path.exists('config/gapsule.ini'):
        config.read('config/gapsule.ini')
    else:
        config.read('config/default.ini')
    settings['dbuser'] = config.get('database', 'user', fallback=None)
    settings['dbname'] = config.get('database', 'dbname', fallback=None)
    settings['cookie_secret'] = config.get(
        'app', 'cookie_secret', fallback='secret_string')
    if settings['cookie_secret'] == 'secret_string':
        warnings.warn("WARNING: it's dangerous")  # TODO


read_config()
