from threading import Lock, Thread
from time import process_time, sleep
from functools import wraps

class LockAcquired(Exception):
	"""LockAcquired: subclass of Exception, raised when non-blocking attempt
		to acquire a resource fails.
	"""

class WithLock(object):
	"""Decorator class to wrap fn execution in a lock.

	Arguments:
		lock (:obj:`Lock`): lock to wrap fn call with. If None, a
			:obj:`Lock` object for fn will be created.
		block (:obj:`bool`): whether :func:`lock.acquire` should block.

	Raises:
		LockAcquired: when :func:`lock.acquire` returns False.

	Example: see (project)/app/update.py
	"""
	def __init__(self, lock=None, block=True):
		super(WithLock, self).__init__()
		self.lock = lock or Lock()
		self.block = block
	def __call__(self, fn, *args, **kwargs):
		@wraps(fn)
		def wrapper(*args, **kwargs):
			avail = self.lock.acquire(blocking=self.block)
			if not avail:
				raise LockAcquired
			try:
				return fn(*args, **kwargs)
			finally:
				self.lock.release()
		return wrapper

class TimerCaller(object):
	"""Class to execute a callable in a separate thread with a fixed time
	interval.

	Arguments:
		fn (callable): the callable to execute. The return value is discarded.
			TODO save return value in a queue (?).
		interval (:obj:`int`): interval between end of the previous call and
			start of the new one (in seconds). TODO make between calls.
		count (:obj:`int`): times fn will be called. If None, loop forever.
	"""
	def __init__(self, interval, fn, count, *args, **kwargs):
		print('TimerCaller.__init__()', args, kwargs)
		super(TimerCaller, self).__init__()
		self.interval = interval
		self.fn = fn
		self.count = count
		self.args = args
		self.kwargs = kwargs
		self._started = False

	def _run(self):
		print('TimerCaller.run()')
		while self.count != 0:
			self.fn(*self.args, **self.kwargs)
			sleep(self.interval)
			if self.count:
				self.count -= 1

	def start(self):
		"""Start the caller thread"""
		if not self._started:
			self._started = True
			print('TimerCaller.start()')
			Thread(target=self._run).start()

class ContextTimerCaller(TimerCaller):
	"""A subclass of TimerCaller to execute fn in app context.

	Arguments:
		app (:obj:`Flask`) - Flask application object providing the context.
	"""

	def __init__(self, app, *args, **kwargs):
		print('ContextTimerCaller.__init__()', args, kwargs)
		super(ContextTimerCaller, self).__init__(*args, **kwargs)
		self.app = app


	def _run(self):
		print('ContextTimerCaller.run()')
		with self.app.app_context():
			super(ContextTimerCaller, self)._run()

class ExecuteSupervisor(ContextTimerCaller):
	"""Class to supervise periodic calls to a callable in a separate thread.

	The interface is inspired by Flask extentions. Allows delayed initialization
	by a call to :meth:`init_app`.
	"""
	def init_app(self, app, *args, **kwargs):
		print('ExecuteSupervisor.init_app()', args, kwargs)
		super(ExecuteSupervisor, self).__init__(app, *args, **kwargs)
		self.start()

	def __init__(self, app=None, *args, **kwargs):
		"""Arguments:
			app (:obj:`Flask`) - Flask application object.

		Examples:
			>>> supervisor = ExecuteSupervisor(app, interval, notify, some_user,
				some_message, count=3)

				Initialized instantly.
				interval, notify, count will be passed to ContextTimerCaller.
				some_user, some_message will be passed to notify() at calls.

			>>> supervisor = ExecuteSupervisor()
			>>> app = create_app()
			>>> supervisor.init_app(app, interval, notify, some_user,
				some_message, count=3)

				Same but initialized by call to init_app().
		"""
		print('ExecuteSupervisor.__init__()', args, kwargs)
		if app:
			self.init_app(app, *args, **args)
