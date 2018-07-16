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

@app.cli.group()
def ds():
	pass

@ds.command()
@click.option('--timer/--no-timer', 'loop', default=None, help='toggle periodical update checks')
@click.option('--interval', '-i', default=None, type=int, help='interval between updates')
@click.option('--debug/--no-debug', default=False, help='toggle debug output from update functions')
def update(interval, loop, debug):
	"""Get updates from datasources"""
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

@ds.command()
@click.argument('name')
def test(name):
	"""Test update from datasource"""
	from app.update import enabled_sources
	enabled_sources[name](debug=True)
