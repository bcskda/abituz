from app import db
from app.models import *

class Datasource(db.Model):
	"""An interface for all data sources.

	Data sources provide the app with students` applications, which are then
	saved in the database.

	Attributes:
		name (str): name of the data source, not null
		_applications (:obj:`list` of :obj:`Applications`): applications known
			by the time of the last update, private.
		last_update (:obj:`datetime.datetime`): last update check time.
		is_failing (:obj:`bool`): indicates whether last update failed.
			Must be None if method `update` was never called.
			Should be set by the `update` method.

	To add a datasource you should:
	1. Inherit from this class:
	1.1. Provide a unique self.__mapper_args__['polymorphic_identity'].
		(see http://docs.sqlalchemy.org/en/latest/orm/inheritance.html).
	1.2. Implement the `update` method so as to update the _applications
		attribute.
	2. @TODO how to register?

	"""

	def __init__(self, applications):
		"""Args:
			applications (:obj:`list` of :obj:`Application`): applications known
				by the time __init__ is called. Should be used to avoid
				extra database write.
		"""
		super(Datasource, self).__init__()
		self._applications = applications

	id = db.Column(db.Integer, primary_key=True)
	
	name = db.Column(db.String(20), nullable=False)
	last_update = db.Column(db.DateTime, default=datetime.utcnow)
	is_failing = db.Column(db.Boolean, nullable=True, default=None)

	@property
	def applications(self):
		""":obj:`list` of :obj:`Application`: applications received
		from this datasource.
		"""
		return self._applications