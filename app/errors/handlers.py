from flask import render_template
from app import db
from app.errors import bp

@bp.errorhandler(500)
def error_500():
	db.session.rollback()
	return 'Sorry'