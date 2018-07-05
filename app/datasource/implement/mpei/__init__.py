from sqlalchemy.orm.exc import NoResultFound
from app import db
from app.models import Datasource, University, Faculty, Program
from app.datasource import enabled_sources
from app.datasource.implement.mpei.const import *

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

from app.datasource.implement.mpei.fn import update
enabled_sources[dsname] = update