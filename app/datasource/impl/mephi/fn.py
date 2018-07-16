import re, requests, itertools
from sqlalchemy.orm.exc import NoResultFound
from app.models import *
from .regex import *
from .const import *

def get_page(text) -> (str, str, int):
	"""Extract info from program entry"""
	header = re.search(pat_program_header, text)
	name, payment = header.group(1), header.group(2)
	num = int(re.search(pat_program_entity_num, text).group(1))

	return name, payment, num

def get_pages() -> [(str, str, int)]:
	"""Find program entries in HTML document"""
	text = requests.get(url_pages).text
	table = re.search(pat_program_table, text).group(1)
	pages = re.findall(pat_program_entry, table)[2:] # First 2 - table headers
	return [get_page(x) for x in pages]

def setup() -> (Datasource, University, Faculty, [(str, str, int)]):
	pages = get_pages()

	try:
		datasource = Datasource.query.filter_by(name=dsname).one()
	except NoResultFound:
		datasource = Datasource(name=dsname)
		db.session.add(datasource)
		db.session.commit()

	if not datasource.is_init:
		university = University(name=uniname)
		db.session.add(university)
		faculty = Faculty(name=facname, university=university)
		db.session.add(faculty)
		
		for name,payment,num in pages:
			code = codes[name]
			if not Program.query.filter_by(code=code).one_or_none():
				db.session.add(Program(code=code, name=name))
		datasource.is_init = True
		db.session.commit()
	else:
		university = University.query.filter_by(name=uniname).one()
		faculty = university.faculties.all()[0]

	return datasource, university, faculty, pages

def get_group(text) -> str:
	return re.search(pat_student_group_name, text).group(1)

def get_score(text) -> int:
	match = re.search(pat_student_score, text).group(1)
	return int(match)

def application_dict(fields) -> dict:
	return {
		'name': fields[3],
		'score_sum': get_score(fields[5]),
		'score_extra': int(fields[6]) - get_score(fields[5])
	}

def handle_application(a, fac, prog, ds):
	student = Student.query.filter_by(name=a['name']).one_or_none()
	if not student:
		student = Student(name=a['name'])
		db.session.add(student)
	application = Application.query.get((student.id, fac.id, prog.id, ds.id))
	if not application:
		application = Application(student=student, faculty=fac, program=prog,
			datasource=ds)
	application.from_dict(a)

def update(debug=False):
	ds_ok = True
	datasource, university, faculty, pages = setup()
	for page_name, page_pay, page_num in pages:
		program = Program.query.filter_by(code=codes[page_name]).one()
		text = requests.get(url_base.format(page_num)).text
		if text == str_no_applications:
			if debug:
				print(program.name, program.code, 'no applications')
			continue
		table = re.search(pat_student_table, text).group(1)
		applications_count = 0
		student_or_group_iter = re.finditer(pat_student_or_group, table)
		for match in itertools.islice(student_or_group_iter, 2, None):
			try:
				if match.group(1) in class_group: # Group starts
					group_name = get_group(match.group(2))
					if debug:
						print('Group', group_name)
				elif match.group(1) in class_entry: # Student entry
					fields = re.findall(pat_student_fields, match.group(2))
					a = application_dict(fields)
					a['budget'] = page_pay == str_budget
					a['without_exam'] = group_name == str_without_exam
					handle_application(a, faculty, program, datasource)
					applications_count += 1
				else:
					raise Exception('pat_student_or_group matched unknown class')
			except Exception as e:
				print(__name__, 'Unhandled exception:', e)
				db.session.rollback()
				datasource.is_failing = True
				ds_ok = False
		db.session.commit()
		if debug:
			print(program.name, program.code,
				'with {} applications'.format(applications_count))
	datasource.last_update = datetime.utcnow()
	datasource.is_failing = ds_ok
	db.session.commit()
