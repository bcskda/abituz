from app import create_app, db
from app.models import *
import click

app = create_app()

@app.shell_context_processor
def make_shell_context():
	return {
		'db': db, 'Application': Application,
		'Student': Student, 'University': University,
		'Faculty': Faculty, 'Program': Program
	}

@app.cli.command()
@click.option('--debug/--no-debug', default=False)
def ds_update(debug):
	from app.update import update_all
	update_all(debug=debug)
