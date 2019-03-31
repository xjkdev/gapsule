import os
import configparser

template_path = os.path.join(os.path.dirname(__file__), "templates")
static_path = os.path.join(os.path.dirname(__file__), "static")

def read_config(app):
    config=configparser.ConfigParser()
    config.read('config/gapsule.ini')
    app.settings['dbuser'] = config.get('database','user',fallback=None)
    app.settings['dbname'] = config.get('database','dbname',fallback=None)