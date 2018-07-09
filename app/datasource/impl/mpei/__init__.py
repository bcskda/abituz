from sqlalchemy.orm.exc import NoResultFound
from app import db
from app.models import Datasource, University, Faculty, Program
from app.datasource import enabled_sources
from .const import *

from .fn import update
enabled_sources[dsname] = update
