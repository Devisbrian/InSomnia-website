from flask import Blueprint

dreamcatcher_bp = Blueprint('dreamcatcher', __name__, template_folder='templates')

from . import routes