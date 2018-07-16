from app import db
from app.datasource import enabled_sources
from .const import *

from .fn import update
enabled_sources[dsname] = update
