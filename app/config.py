import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'app.db')

	SQLALCHEMY_TRACK_MODIFICATIONS = False

	APP_UPDATE_TIMER = (os.environ.get('APP_UPDATE_TIMER') not in [None, '0']) or \
		False

	APP_UPDATE_SECS = int(os.environ.get('APP_UPDATE_SECS') or \
		1800) # 30 min
