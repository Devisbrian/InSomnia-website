from flask import render_template, redirect, url_for, request, current_app, flash
from flask.json import dumps
from app.common.mail import send_email
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from itsdangerous import SignatureExpired

from app import login_manager, urltimed
from . import auth_bp
from .forms import SignupForm, LoginForm
from .models import User
from app.models import Members
import logging

logger = logging.getLogger(__name__)

@auth_bp.route("/email-confirm/<token>", methods=["GET", "POST"])
def email_confirm(token):
    try:
        email = urltimed.loads(token, salt='email-confirm', max_age=180)
    except SignatureExpired:
        email = None
    
    if email is not None:
        user = User.get_by_email(email=email)
        user.confirm = True
        user.save()
        logger.info(f'El Email {email} ha sido verificado')
    return render_template("auth/confirm.html", email=email)


@auth_bp.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    form = SignupForm()
    form.bias.choices = [(member.name, member.name) for member in Members.get_all()]
    form.bias.choices.insert(0, ("", "Seleccione una o más"))
    error = None
    #if request.method == 'POST': # PARA MODAL SIGNUP
        #username = request.form.get('uname')
        #name = request.form.get('name')
        #lastname = request.form.get('lastname')
        #city = request.form.get('city')
        #phone = request.form.get('phone')
        #birthday = request.form.get('birthday')
        #bias = request.form.get('bias')
        #email = request.form.get('email')
        #password = request.form.get('psw')
        #password_confirm = request.form.get('psw_c')
    if form.validate_on_submit():
        username = form.username.data
        name = form.name.data
        lastname = form.lastname.data
        city = form.city.data
        phone = form.phone.data
        birthday = form.birthday.data
        bias = form.bias.data
        email = form.email.data
        password = form.password.data
        password_confirm = form.password_confirm.data

        # Comprobamos que no hay ya un usuario con ese email
        user = User.get_by_email(email)
        user2 = User.get_by_username(username)
        
        
        if user is not None:
            flash('El email digitado ya está siendo utilizado por otra persona')
        elif user2 is not None:
            flash('El nombre de usuario digitado ya está siendo utilizado por otra persona')
        else:
            # Creamos el usuario y lo guardamos
            user = User(username=username, name=name, lastname=lastname, email=email, city=city, phone=phone, birthday=birthday)
            user.set_password(password)
            # Busqueda de bias
            for biases in bias:
                bias_for_user = Members.get_by_name(biases)
                user.bias.append(bias_for_user)
            user.save()
            # Crear token de verificación de correo
            token = urltimed.dumps(email, salt='email-confirm')
            link = url_for('auth.email_confirm', token=token, _external=True)
            # Enviamos un email de bienvenida
            send_email(subject='Welcome to the dreamworld',
                       sender=current_app.config['DONT_REPLY_FROM_EMAIL'],
                       recipients=[email, ],
                       text_body=f'Hola {username}, ahora eres parte de InSomnia Colombia.',
                       html_body=f'<p>Hola <strong>{username}</strong>, ahora eres parte de InSomnia Colombia</p><br>Confirma tu Email a través del siguiente link: {link}')
            # Dejamos al usuario logueado
            login_user(user, remember=True)
            next_page = request.args.get('next', None)
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('public.index')
            return redirect(next_page)
    return render_template('auth/signup_form.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    #form = LoginForm()
    if request.method == 'POST':
        user = request.form.get('uname')
        user = User.get_by_username(user)
        psw = request.form.get('psw')
        remember_me = request.form.get('remember')
    #if form.validate_on_submit():
        #user = User.get_by_username(form.username.data)
        #if user is not None and user.check_password(form.password.data):
        if user is not None and user.check_password(psw):
            login_user(user, remember=remember_me)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('public.index')
            return redirect(next_page)
        else:
            flash('Ooops! El usuario o la contraseña es incorrecta')
    return redirect(url_for('public.index'))


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.index'))


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))