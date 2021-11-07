from functools import wraps
from flask import abort, flash
from flask.helpers import url_for
from flask_login import current_user
from werkzeug.utils import redirect


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        is_admin = getattr(current_user, 'is_admin', False)
        if not is_admin:
            abort(401)
        return f(*args, **kws)
    return decorated_function

def staff_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        is_staff = getattr(current_user, 'is_staff', False)
        if not is_staff:
            abort(401)
        return f(*args, **kws)
    return decorated_function

def email_confirm_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        confirm = getattr(current_user, 'confirm', False)
        if not confirm:
            flash('¡Oops, para esto debes haber confirmado tu correo electrónico!')
            return redirect(url_for('public.index'))
        return f(*args, **kws)
    return decorated_function