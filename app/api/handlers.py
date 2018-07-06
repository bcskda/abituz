from app.api import bp

@bp.route('/update', methods=['POST'])
def do_update():
	print()
	from app.update import update_all
	update_all()
	return 'done'