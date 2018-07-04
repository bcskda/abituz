from app import create_app, db
from app.models import *

app = create_app()

@app.shell_context_processor
def make_shell_context():
	return {
		'db': db, 'Application': Application,
		'Student': Student, 'University': University,
		'Faculty': Faculty, 'Program': Program
	}