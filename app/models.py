from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
from app import db

class Application(db.Model):
	"""Represents an application made by student.

	Implements the many-to-many relationship between Student, Faculty and
	Program.

	Atributes:
		is_revoked (:obj:`bool`): whether the application has been recalled.
		last_seen (:obj:`datetime.datetime`): last time the data source

	Relationships:
		student (:obj:`Student`): many-to-many
		faculty (:obj:`Faculty`): many-to-many
		program (:obj:`Program`): many-to-many
		datasource (:obj:`Datasource`): many-to-many

	"""

	__tablename__ = 'application'

	student_id    = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)
	faculty_id    = db.Column(db.Integer, db.ForeignKey('faculty.id'), primary_key=True)
	program_id    = db.Column(db.Integer, db.ForeignKey('program.id'), primary_key=True)
	datasource_id = db.Column(db.Integer, db.ForeignKey('datasource.id'), primary_key=True)

	exam_1 = db.Column(db.String(10))
	exam_2 = db.Column(db.String(10))
	exam_3 = db.Column(db.String(10))
	exam_4 = db.Column(db.String(10))
	exam_5 = db.Column(db.String(10))
	exam_6 = db.Column(db.String(10))

	score_1 = db.Column(db.Integer)
	score_2 = db.Column(db.Integer)
	score_3 = db.Column(db.Integer)
	score_4 = db.Column(db.Integer)
	score_5 = db.Column(db.Integer)
	score_6 = db.Column(db.Integer)
	score_extra = db.Column(db.Integer, default=0)
	without_exam = db.Column(db.Boolean, default=False)

	is_revoked = db.Column(db.Boolean, default=False)
	last_seen = db.Column(db.DateTime, default=datetime.utcnow)
	datasource = db.Column(db.String(20), nullable=True, index=True)

	student    = db.relationship("Student", back_populates="applications")
	faculty    = db.relationship("Faculty", back_populates="applications")
	program    = db.relationship("Program", back_populates="applications")
	datasource = db.relationship("Datasource", back_populates="applications")

	def from_dict(self, o):
		self.exam_1 = o['exam_1']
		if 'exam_2' in o: self.exam_2 = o['exam_2']
		if 'exam_3' in o: self.exam_3 = o['exam_3']
		if 'exam_4' in o: self.exam_4 = o['exam_4']
		if 'exam_5' in o: self.exam_5 = o['exam_5']
		if 'exam_6' in o: self.exam_6 = o['exam_6']
		self.score_1 = o['score_1']
		if 'score_2' in o: self.score_2 = o['score_2']
		if 'score_3' in o: self.score_3 = o['score_3']
		if 'score_4' in o: self.score_4 = o['score_4']
		if 'score_5' in o: self.score_5 = o['score_5']
		if 'score_6' in o: self.score_6 = o['score_6']
		if 'score_extra' in o: self.score_extra = o['score_extra']
		if o['without_exam']:
			self.without_exam = True
		if o['revoked']:
			self.is_revoked = True
		if o['last_seen']:
			self.last_seen = o['last_seen']

	def exam_results(self):
		result = '{} {}'.format(self.exam_1, self.score_1)
		if self.exam_2:
			result += ', {} {}'.format(self.exam_2, self.score_2)
		if self.exam_3:
			result += ', {} {}'.format(self.exam_3, self.score_3)
		if self.exam_4:
			result += ', {} {}'.format(self.exam_4, self.score_4)
		if self.exam_5:
			result += ', {} {}'.format(self.exam_5, self.score_5)
		if self.exam_6:
			result += ', {} {}'.format(self.exam_6, self.score_6)
		result += ', {} {}'.format('ИД', self.score_6)
		return result

class Student(db.Model):
	"""Represents a student.

	Attributes:
		name (str): Full name, not null, unique

	Relationships:
		applications (query -> :obj:`list` of :obj:`Application`): applications made
			by this student, many-to-many.

	Note: the `applications.append()` method will register a new application,
	however `db.session.commit()` is required for changes to be saved.

	"""

	__tablename__ = 'student'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False, index=True)

	applications = db.relationship("Application", back_populates="student")

class University(db.Model):
	"""Represents a university.

	Attributes:
		name (str): Name of the uni, not null

	Relationships:
		faculties (:obj:`list` of :obj:`Faculty`): one-to-many.

	"""

	__tablename__ = 'university'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)

	faculties = db.relationship("Faculty", back_populates="university", lazy='dynamic')

class Faculty(db.Model):
	"""Represents a university`s faculty.

	Attributes:
		name (str): Name of the faculty, not null

	Relationships:
		university (:obj:`University`): many-to-one.
		applications (query -> :obj:`list` of :obj:`Application`): applications to this
			faculty, many-to-many.

	Note: the `applications.append()` method will register a new application,
	however `db.session.commit()` is required for changes to be saved.

	"""

	__tablename__ = 'faculty'

	id = db.Column(db.Integer, primary_key=True)
	university_id = db.Column(db.Integer, db.ForeignKey('university.id'))

	name = db.Column(db.String(100), nullable=False)

	university = db.relationship("University", back_populates="faculties")
	applications = db.relationship("Application", back_populates="faculty", lazy='dynamic')

class Program(db.Model):
	"""Represents a study program.

	Attributes:
		code (str): e.g. '01.03.02'
		name (str): description, e.g. 'Software Engineering'

	Relationships:
		applications (query -> :obj:`list` of :obj:`Application`): applications to this
			study program, many-to-many.

	Note: the `applications.append()` method will register a new application,
	however `db.session.commit()` is required for changes to be saved.

	"""

	__tablename__ = 'program'

	id = db.Column(db.Integer, primary_key=True)

	code = db.Column(db.String(11), nullable=False, index=True)
	name = db.Column(db.String(100), nullable=False)

	applications = db.relationship("Application", back_populates="program")

class Datasource(db.Model):
	"""An interface for all data sources.

	Data sources provide the app with students` applications, which are then
	saved in the database.

	Attributes:
		name (str): frienly name of the data source, not null.
		last_update (:obj:`datetime.datetime`): last update check time.
		is_failing (:obj:`bool`): indicates whether last update failed.
			Must be None if method `update` was never called.
		is_init (:obj:`bool`): indicates whether a db record has been created
			for the data source.

	Relationships:
		applications (query -> :obj:`list` of :obj:`Application`): applications registered
			by this data source, many-to-many.

	To add a datasource you should:
	1. Inherit from this class
	2. Implement the `update` method so as to update the _applications
		attribute. See :module:`app.datasource.mpei` as an example.
	3. Add an instance of your class to app.datasource.config.datasources
		(see app.datasource.config.py for reference).

	"""

	__tablename__ = 'datasource'

	id = db.Column(db.Integer, primary_key=True)

	name = db.Column(db.String(20), nullable=False)
	last_update = db.Column(db.DateTime, default=datetime.utcnow)
	is_failing = db.Column(db.Boolean, nullable=True, default=None)
	is_init = db.Column(db.Boolean, default=False)

	applications = db.relationship("Application", back_populates="datasource", lazy='select')
