import os
#from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
#load_dotenv(os.path.join(basedir, 'config.env'))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    os.environ.get('DATABASE_URL_CONFIG') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
