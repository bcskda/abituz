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
@click.option('--interval', '-i', default=None)
@click.option('--timer/--no-timer', 'loop', default=None)
@click.option('--debug/--no-debug', default=False)
def ds_update(interval, loop, debug):
	"""Examples:
		(venv) $ flask ds_update --timer -i 1800
			Update every 1800 sec (30 min)
		(venv) $ APP_UPDATE_TIMER=1 flask ds_update
			The same
		(venv) $ flask ds_update --debug
			Update once with debug
	"""
	if interval == None:
		interval = app.config['APP_UPDATE_SECS']
	if loop == None:
		loop = app.config['APP_UPDATE_TIMER']

	if loop:
		print('Starting supervisor')
		from app.update import UpdateSupervisor
		supervisor = UpdateSupervisor(interval, debug=debug)
	else:
		print('Starting single update')
		from app.update import update_all
		update_all(debug=debug)
