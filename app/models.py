from datetime import datetime
from app import db

class Application(db.Model):
	"""Represents an application made by student.

	Implements the many-to-many relationship between Student, Faculty and
	Program.

	Atributes:
		is_revoked (:obj:`bool`): whether the application has been recalled.
		last_seen (:obj:`datetime.datetime`): last time the data source

	Relationships:
		student (:obj:`Student`): many-to-one
		faculty (:obj:`Faculty`): many-to-one
		program (:obj:`Program`): many-to-one

	"""

	__tablename__ = 'application'

	student_id = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)
	faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), primary_key=True)
	program_id = db.Column(db.Integer, db.ForeignKey('program.id'), primary_key=True)

	is_revoked = db.Column(db.Boolean, default=False)
	last_seen = db.Column(db.DateTime, default=datetime.utcnow)
	datasource = db.Column(db.String(20), nullable=True, index=True)

	student = db.relationship("Student", back_populates="applications")
	faculty = db.relationship("Faculty", back_populates="applications")
	program = db.relationship("Program", back_populates="applications")

class Student(db.Model):
	"""Represents a student.

	Attributes:
		name (str): Full name, not null, unique

	Relationships:
		applications (:obj:`list` of :obj:`Application`): applications made
			by this student

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
		faculties (:obj:`list` of :obj:`Faculty`): one-to-many

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
		university (:obj:`University`): many-to-one
		applications (:obj:`list` of :obj:`Application`): applications to this
			faculty

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
		applications (:obj:`list` of :obj:`Application`): applications to this
			study program

	Note: the `applications.append()` method will register a new application,
	however `db.session.commit()` is required for changes to be saved.

	"""

	__tablename__ = 'program'

	id = db.Column(db.Integer, primary_key=True)

	code = db.Column(db.String(11), nullable=False, index=True)
	name = db.Column(db.String(20), nullable=False)

	applications = db.relationship("Application", back_populates="program")