from threading import Lock
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
		def wrapper(*args, **kwargs):
			avail = self.lock.acquire(blocking=self.block)
			if not avail:
				raise LockAcquired
			try:
				return fn(*args, **kwargs)
			finally:
				self.lock.release()
		return wrapper