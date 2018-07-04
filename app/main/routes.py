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
	return render_template('index.html')

@bp.route('/count/<name>')
def count(name):
	try:
		student = Student.query.filter_by(name=name).one()
		count = len(student.applications)
	except NoResultFound:
		count = None
	return render_template('count.html', name=name, count=count)

@bp.route('/list/by_student')
def list_all_by_student():
	students = Student.query.all()
	return render_template('list_by_student.html', students=students)