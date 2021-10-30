from flask import Blueprint

fanclub_bp = Blueprint('fanclub', __name__, template_folder='templates')

from . import routes