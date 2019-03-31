'''import configparser
from gapsule.app import app'''
from gapsule.models.repo import get_branches_name

'''def read_config(app):
    config=configparser.ConfigParser()
    config.read('gapsule.ini')
    app.settings['dbuser'] = config['user']
    app.settings['dbname'] = config['gapsule']

read_config(app)'''

get_branches_name()