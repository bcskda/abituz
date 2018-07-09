from threading import Thread
from datetime import datetime
from app.models import Datasource
from app.serialize import jenc
from app.api import bp

@bp.route('/update', methods=['POST'])
def do_update():
	result = {'error': 0, 'error_explain': 'ok'}
	from app.update import update_all, is_updating
	start_time = datetime.utcnow()
	if is_updating():
		result['error'] = -1
		result['error_explain'] = 'update in progress'
		return jenc(result)
	update_all()
	now = datetime.utcnow()
	delta = now - start_time
	result['finished_at'] = now.isoformat()
	result['took_seconds'] = delta.seconds
	return jenc(result)

@bp.route('/update', methods=['GET'])
def is_updating():
	result = {'error': 0, 'error_explain': 'ok'}
	from app.update import is_updating
	result['updating'] = is_updating()
	return jenc(result)
