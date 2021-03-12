import configparser
import os

loaded_config = {}


def init():
    key_suffix = 'dev'
    if os.getenv('APP_ENV') == 'production':
        key_suffix = 'prod'
    elif os.getenv('APP_ENV') == 'dev-docker':
        # A different config is needed to access the localhost DB from within the Mac OS docker container.
        key_suffix = 'docker'

    config = configparser.ConfigParser()
    config.read( 'instance/app.cnf' )

    loaded_config['database'] = dict(config[f'database-{key_suffix}'])
    loaded_config['app_secret'] = dict(config[f'app-secret-{key_suffix}'])


def get_secret_key():
    return loaded_config['app_secret']['secret']


def get_db_config():
    return loaded_config['database']
    
