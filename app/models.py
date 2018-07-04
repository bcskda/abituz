from datetime import datetime
from app import db

class Application(db.Model):
	"""Represents an application made by student

	Atributes:
		student(:obj:`Student`)
		faculty(:obj:`Faculty`)
		program(:obj:`Program`)
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
	"""Represents a student

	Attributes:
		name (str): Full name
		applications (:obj:`list` of :obj:`Application`): Applications made by
		the student

	The `applicaions.append()` method will register a new application, however
	`db.session.commit()` is required for changes to be saved.
	"""

	__tablename__ = 'student'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False, index=True)
	applications = db.relationship("Application", back_populates="student", lazy='dynamic')

class University(db.Model):
	__tablename__ = 'university'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	faculties = db.relationship("Faculty", back_populates="university", lazy='dynamic')

class Faculty(db.Model):
	__tablename__ = 'faculty'
	id = db.Column(db.Integer, primary_key=True)
	university_id = db.Column(db.Integer, db.ForeignKey('university.id'))
	name = db.Column(db.String(100), nullable=False)
	university = db.relationship("University", back_populates="faculties", lazy='dynamic')
	applications = db.relationship("Application", back_populates="faculty", lazy='dynamic')

class Program(db.Model):
	__tablename__ = 'program'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(11), nullable=False, index=True)
	name = db.Column(db.String(20), nullable=False)
	applications = db.relationship("Application", back_populates="program", lazy='dynamic')