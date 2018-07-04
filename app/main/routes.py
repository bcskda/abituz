from flask import redirect, url_for, request, render_template
from sqlalchemy.orm.exc import NoResultFound
from app import db
from app.models import Student
from app.main import bp

@bp.route('/')
def redirect_to_index():
	return redirect(url_for('main.index'))

@bp.route('/index')
def index():
	return render_template('index.html', title='Home')

@bp.route('/count/<name>')
def count(name):
	try:
		student = Student.query.filter_by(name=name).one()
		count = len(student.applications)
	except NoResultFound:
		count = None
	return render_template('count.html', title='Count', name=name, count=count)

@bp.route('/students')
def students_all():
	students = Student.query.all()
	return render_template('students.html', title='All students', students=students)