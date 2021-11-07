from flask import render_template, redirect, url_for, abort, current_app, flash
from flask_login import login_required
import logging

from app.auth.models import User

from . import profile_bp

logger = logging.getLogger(__name__)


@profile_bp.route('/profile/<username>/')
@login_required
def index(username):
    user = User.get_by_username(username)
    return render_template('profile/index.html', user=user)