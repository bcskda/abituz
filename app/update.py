from app import db
from datetime import datetime
from app.datasource import enabled_sources

def update_all(debug=False):
	"""requests updates from all data sources"""
	for key,fn in enabled_sources.items():
		if debug:
			print(__name__, datetime.utcnow(),
				'call update on {}...'.format(key))
		try:
			fn(debug=debug)
		except Exception as e:
			print(__name__, 'Unhandled exception in {}:'.format(key), e)
			db.session.rollback()
		print(__name__, datetime.utcnow(), 'finished', key)