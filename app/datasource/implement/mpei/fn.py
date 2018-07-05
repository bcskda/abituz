import re, requests
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
from app.models import *
from .regex import *
from .const import *
from . import university, datasource

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

def update(debug=False):
	if debug:
		print(university.name, 'with total pages:', len(pages))
	for num, page in enumerate(pages):
		faculty = Faculty.query.filter_by(university=university, name=page[0]).one()
		program = Program.query.filter_by(code=page[1]).one()
		text = requests.get(url_base.format(num + 1)).text
		time = get_time(text) # TODO self.last_update
		exams = get_exams(text)
		applications_count = 0
		for table in re.finditer(pat_table, text):
			unsaved_count = 0
			for a in applications(text[table.start():table.end()], count=len(exams)):
				try:
					a['without_exam'] = table.group(1) == without_exam
					a['revoked'] = revoked in a['notes']
					a['last_seen'] = time
					for i,exam in enumerate(exams):
						a['exam_{}'.format(i + 1)] = exam
					try:
						student = Student.query.filter_by(name=a['name']).one()
					except NoResultFound:
						student = Student(name=a['name'])
						db.session.add(student)
					application = Application.query.get((student.id, faculty.id,
						program.id, datasource.id))
					if not application:
						application = Application(student=student, faculty=faculty,
							program=program, datasource=datasource)
					application.from_dict(a)
					application.last_update = time
					applications_count += 1
				except Exception as e:
					print(__name__, ' Unhandled exception:', e)
					db.session.rollback()
					datasource.is_failing = True
			datasource.last_update = datetime.utcnow()
			db.session.commit()
		if debug:
			print('Page #', num + 1, faculty.name, program.code, program.name,
				time, exams, 'with {} applications'.format(applications_count))
		datasource.is_failing = False
		db.session.commit()