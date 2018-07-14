"""Module `app.update`: update info stored in db.

Warning: Should not be imported outside app context.
"""

from datetime import datetime
from threading import Lock
from sqlalchemy.sql import func
from app import db, async
from app.models import Datasource
from app.datasource import enabled_sources

_update_lock = Lock()
try:
	_last_update = db.session.query(func.max(Datasource.last_update))
except RuntimeError as e:
	print('app.update imported out of context') # Maybe it`s wrong
	raise e

def is_updating():
	return _update_lock.locked()

def last_update():
	return _last_update.one()

@async.WithLock(lock=_update_lock, block=False)
def update_all(debug=False):
	"""Requests updates from all data sources

	It can be *very* slow, so you probably would like to execute this
		in a separate thread. If the db allows.
	"""
	print(__name__, datetime.utcnow().isoformat(),
		'Update started')
	for ds,fn in enabled_sources.items():
		print(__name__, datetime.utcnow().isoformat(),
			'started datasource', ds)
		try:
			fn(debug=debug)
		except Exception as e:
			print(__name__, 'Unhandled exception in datasource {}:'.format(ds), e)
			db.session.rollback()
		print(__name__, datetime.utcnow().isoformat(),
			'finished datasource', ds)
	last_update = datetime.utcnow()
	print(__name__, last_update.isoformat(),
		'Update finished')

class UpdateSupervisor(async.TimerCaller):
	"""Class to supervise data updates in a separate thread.
	TODO make singleton.
	"""
	def __init__(self, interval, *args, **kwargs):
		"""Overrides ExecuteSupervisor`s :meth:`__init__` to get configuration
			from the app object and pass it to ContextTimerCaller."""
		super(UpdateSupervisor, self).__init__(interval, update_all, None, *args, **kwargs)
		self.start()
