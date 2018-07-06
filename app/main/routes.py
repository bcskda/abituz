from flask import redirect, url_for, request, render_template
from sqlalchemy.orm.exc import NoResultFound
from app import db
from app.models import Student, Application
from app.main import bp

@bp.route('/')
def redirect_to_index():
	return redirect(url_for('main.index'))

@bp.route('/index')
def index():
	return render_template('index.html', title='Home')

@bp.route('/count')
def count():
	total = len(Application.query.all())
	return render_template('count.html', count=total)

@bp.route('/count/<name>')
def count_by_name(name):
	try:
		student = Student.query.filter_by(name=name).one()
		count = len(student.applications)
	except NoResultFound:
		count = None
	return render_template('count_by_name.html', title='Count', name=name, count=count)

@bp.route('/students')
def students():
	students = Student.query.all()
	return render_template('students.html', title='All students', students=students)

@bp.route('/students/<name>')
def student_by_name(name):
	student = Student.query.filter_by(name=name).first_or_404()
	return render_template('student_by_name.html', student=student)