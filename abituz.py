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
@click.option('--interval', '-i', default=1800)
@click.option('--loop', is_flag=True, default=False)
@click.option('--debug', is_flag=True, default=False)
def ds_update(loop, interval, debug):
	"""Examples:
		(venv) $ flask ds_update -l -i 900
			Update every 1800 sec (30 min)
		(venv) $ flask ds_update --debug
			Update once with debug
	"""
	if loop:
		from app.update import UpdateSupervisor
		supervisor = UpdateSupervisor(interval, debug=debug)
	else:
		from app.update import update_all
		update_all(debug=debug)
