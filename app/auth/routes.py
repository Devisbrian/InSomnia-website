from flask import redirect, url_for, request, flash, jsonify
from app.common.mail import mail_verification
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from itsdangerous import SignatureExpired

from app import login_manager, urltimed
from . import auth_bp
from .models import User, Cities
from app.dreamcatcher.models import Members
import logging

logger = logging.getLogger(__name__)

@auth_bp.route("/email-confirm/<token>", methods=["GET", "POST"])
def email_confirm(token):
    try:
        email = urltimed.loads(token, salt='email-confirm', max_age=86400)
    except SignatureExpired:
        email = None
    
    if email is not None:
        user = User.get_by_email(email=email)
        user.confirm = True
        user.save()
        logger.info(f'El Email {email} ha sido verificado')
        flash('Yujuuuu, ¡has verificado el email ' + email + '!')
    else:
        flash('Oops, parece que ha expirado la verificación de correo electrónico. Entra a tu perfil y solicita una nueva verificación')
    return redirect(url_for('public.index'))


@auth_bp.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    error = None
    if request.method == 'POST': # PARA MODAL SIGNUP
        username = request.form.get('uname')
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        city = int(request.form.get('city'))
        phone = request.form.get('phone')
        birthday = request.form.get('birthday')
        bias = request.form.getlist('bias')
        email = request.form.get('email')
        password = request.form.get('psw')
        password_confirm = request.form.get('psw_c')

        cityDb = Cities.get_by_id(city)
        # Comprobamos que no hay ya un usuario con ese email
        user = User.get_by_email(email)
        user2 = User.get_by_username(username)
        
        if user is not None:
            flash('El email digitado ya está siendo utilizado por otra persona')
        elif user2 is not None:
            flash('El nombre de usuario digitado ya está siendo utilizado por otra persona')
        elif password != password_confirm:
            flash('Las contraseñas no coinciden')
        else:
            # Creamos el usuario y lo guardamos
            user = User(username=username, name=name, lastname=lastname, email=email, city=cityDb, phone=phone, birthday=birthday)
            user.set_password(password)
            # Busqueda de bias
            for biases in bias:
                bias_for_user = Members.get_by_id(int(biases))
                user.bias.append(bias_for_user)
            user.save()
            #Verificación de correo
            mail_verification(email=email, username=username)
            # Dejamos al usuario logueado
            login_user(user, remember=True)
            next_page = request.args.get('next', None)
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('public.index')
            flash('Yujuuu, ¡Welcome to the Dream World, ' + username + '!')
            flash('¡Revisa tu correo electrónico! ;)')
            return redirect(next_page)
    return None
    #return render_template('auth/signup_form.html', form=form)


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

# Jsonify

@auth_bp.route("/member/")
def member():
    members = Members.get_all()
    memberArray = []
    for member in members:
        memberObj = {}
        memberObj['value'] = member.id
        memberObj['name'] = member.name
        memberArray.append(memberObj)
    return jsonify({'members' : memberArray})

@auth_bp.route("/city/")
def city():
    cities = Cities.get_all()
    cityArray = []
    for city in cities:
        cityObj = {}
        cityObj['value'] = city.id
        cityObj['name'] = city.name
        cityArray.append(cityObj)
    return jsonify({'cities' : cityArray})