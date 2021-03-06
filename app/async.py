"""Re-usable utils for asynchronous stuff."""


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
	"""Class to execute a callable with a fixed time interval.

	Arguments:
		fn (callable): the callable to execute. The return value is discarded.
			TODO save return value in a queue (?).
		interval (:obj:`int`): interval between end of the previous call and
			start of the new one (in seconds). TODO make between calls.
		count (:obj:`int`): times fn will be called. If None, loop forever.
	"""
	def __init__(self, interval, fn, count, *args, **kwargs):
		super(TimerCaller, self).__init__()
		self.interval = interval
		self.fn = fn
		self.count = count
		self.args = args
		self.kwargs = kwargs
		self._started = False

	def start(self):
		"""Start the call-in-loop thread."""
		while self.count != 0:
			self.fn(*self.args, **self.kwargs)
			sleep(self.interval)
			if self.count:
				self.count -= 1
