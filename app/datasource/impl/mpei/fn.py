import re, requests
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
from app.models import *
from .regex import *
from .const import *

def setup() -> (Datasource, University):
	try:
		datasource = Datasource.query.filter_by(name=dsname).one()
	except NoResultFound:
		datasource = Datasource(name=dsname)
		db.session.add(datasource)
		db.session.commit()

	if not datasource.is_init:
		university = University(name=uniname)
		db.session.add(university)
		fac_names = set(map(lambda x: x[0], pages[1:]))
		faculties = [Faculty(name=x, university=university) for x in fac_names]
		db.session.add_all(faculties)
		for x in pages:
			if not Program.query.filter_by(code=x[1]).one_or_none():
				db.session.add(Program(code=x[1], name=x[2]))
		datasource.is_init = True
		db.session.commit()
	else:
		university = University.query.filter_by(name=uniname).one()
	return datasource, university

def get_time(text):
	return re.search(pat_time, text).group(1)

def get_exams(text):
	exam_iter = re.finditer(pat_exam, text)
	return set([s.group(1) for s in exam_iter])

def parse_application(text, count):
	field_values = map(
		lambda x: x.group(1),
		re.finditer(pat_field, text))
	return dict(zip(student_fields[count], field_values))

def applications(text, count=3):
	for s in re.finditer(pat_student, text):
		yield parse_application(s.group(1), count)
	return None

def handle_application(a, fac, prog, ds):
	try:
		student = Student.query.filter_by(name=a['name']).one()
	except NoResultFound:
		student = Student(name=a['name'])
		db.session.add(student)
	application = Application.query.get((student.id, fac.id, prog.id, ds.id))
	if not application:
		application = Application(student=student, faculty=fac, program=prog,
			datasource=ds)
	application.from_dict(a)

def update(debug=False):
	datasource, university = setup()
	if debug:
		print(university.name, 'with total page groups:', len(pages))
	for page_group_num,page_group in enumerate(pages):
		faculty = Faculty.query.filter_by(university=university, name=page_group[0]).one()
		program = Program.query.filter_by(code=page_group[1]).one()
		applications_count = 0
		for page_num in page_group[3]:
			text = requests.get(url_base.format(page_num)).text
			time = get_time(text)
			exams = get_exams(text)
			for table in re.finditer(pat_table, text):
				for a in applications(table.group(0), count=len(exams)):
					try:
						a['without_exam'] = table.group(1) == str_without_exam
						a['last_seen'] = datetime.strptime(time, time_fmt)
						a['revoked'] = str_revoked in a['notes']
						for i,exam in enumerate(exams):
							a['exam_{}'.format(i + 1)] = exam
						ident = (faculty.id, program.id, datasource.id)
						handle_application(a, faculty, program, datasource)
						applications_count += 1
					except Exception as e:
						print(__name__, ' Unhandled exception:', e)
						db.session.rollback()
						datasource.is_failing = True
			datasource.last_update = datetime.utcnow()
			db.session.commit()
		if debug:
			print('#', page_group_num, faculty.name, program.code, program.name,
				time, exams, 'with {} applications'.format(applications_count))
	datasource.is_failing = False
	db.session.commit()
