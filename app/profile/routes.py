from flask import render_template, redirect, url_for, abort, current_app, flash, jsonify, request
from flask_login import login_required, current_user
import logging

from app.auth.models import User, Cities
from .forms import AddProfilePic, AddAlbums, AddPhotocards, EditPersonalInfo
from app.dreamcatcher.models import Album, Members, PhotocardDb, AlbumType
from app.common.mail import mail_verification

import os
from werkzeug.utils import secure_filename
from . import profile_bp
from app import profile

logger = logging.getLogger(__name__)


@profile_bp.route('/profile/<username>/')
@login_required
def index(username):
    user = User.get_by_username(username)
    if current_user.id != user.id:
        flash('¡Oops, nadie puede ver el perfil de otro usuario!.. Por ahora ;)')
        return redirect(url_for('public.index'))
    
    albums = [(albums.album, albums.album) for albums in Album.get_all()]
    album_types = [(album_type.pc_type, album_type.pc_type) for album_type in AlbumType.get_all()]
    cities = [(city.name, city.name) for city in Cities.get_all()]

    form = AddProfilePic(obj=user)

    albumForm = AddAlbums(obj=user)
    albumForm.albums.choices = albums
    #albumForm.albums.choices.insert(0, ("", "Seleccione"))

    pcForm = AddPhotocards(obj=user)
    pcForm.album.choices = albums
    pcForm.album.choices.insert(0, ("", "Seleccione"))
    pcForm.album_type.choices = album_types
    pcForm.album_type.choices.insert(0, ("", "Seleccione"))
    pcForm.members.choices = [(member.name, member.name) for member in Members.get_all()]
    pcForm.members.choices.insert(0, ("", "Seleccione"))

    infoForm = EditPersonalInfo(obj=user)
    infoForm.bias.choices = [(member.id, member.name) for member in Members.get_all()]
    infoForm.bias.choices.insert(0, ("", "Seleccione"))
    infoForm.city.choices = cities
    infoForm.city.choices.insert(0, ("", "Seleccione"))
    return render_template('profile/index.html', user=user, form=form, albumForm=albumForm, pcForm=pcForm, infoForm=infoForm)

@profile_bp.route('/profile/pic_upload/', methods=['GET', 'POST'])
def pic_upload():
    user_id = current_user.id
    user = User.get_by_id(user_id)
    form = AddProfilePic(obj=user)
    if form.validate_on_submit():
        file = form.profile_pic.data
        pic_name = None
        if file:
            images_dir = current_app.config['USER_PIC_DIR']
            if user.profile_pic_name:
                old_image_name = user.profile_pic_name
                old_file_path = os.path.join(images_dir, old_image_name)
                os.remove(old_file_path)
            pic_name = secure_filename(file.filename)
            os.makedirs(images_dir, exist_ok=True)
            file_path = os.path.join(images_dir, pic_name)
            file.save(file_path)
        user.profile_pic_name = pic_name
        user.save()
        flash('¡Yujuuu, has cambiado la foto de perfil!')
    return redirect(url_for('profile.index', username=current_user.username))

@profile_bp.route('/profile/add_album/', methods=['GET', 'POST'])
def add_album():
    user = User.get_by_id(current_user.id)
    if request.method == 'POST':
        albums = request.form.getlist('albums')
        user.albums.clear()
        for album in albums:
            album_for_user = Album.get_by_album(album)
            user.albums.append(album_for_user)
        user.save()
        flash('¡Yujuuu!, has agregado los álbumes:')
        for data in albums:
            flash(data)
    return redirect(url_for('profile.index', username=current_user.username))

@profile_bp.route('/profile/add_pc/', methods=['GET', 'POST'])
def add_pc():
    user = User.get_by_id(current_user.id)
    if request.method == 'POST':
        albumData = request.form.get('album')
        album_typeData = request.form.get('album_type')
        membersData = request.form.getlist('members')
        album = Album.get_by_album(albumData)
        album_type = AlbumType.get_by_type(album_typeData)

        for memberData in membersData:
            member = Members.get_by_name(memberData)
            pc_for_user = PhotocardDb.get_filtered(album.id, album_type.id, member.id)
            print(pc_for_user)
            user.photocards.append(pc_for_user)
        user.save()
        flash('¡Yujuuu!, has agregado photocards')
    return redirect(url_for('profile.index', username=current_user.username))

@profile_bp.route('/profile/update_info/', methods=['GET', 'POST'])
def update_info():
    user = User.get_by_id(current_user.id)
    if request.method == 'POST':
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        city = request.form.get('city')
        phone = request.form.get('phone')
        birthday = request.form.get('birthday')
        bias = request.form.getlist('bias')
        facebook = request.form.get('facebook')
        twitter = request.form.get('twitter')
        instagram = request.form.get('instagram')
        if bias:
            for element in user.bias:
                user.bias.remove(element)
        if city:
            cityObj = Cities.get_by_name(city)
            user.city = cityObj
        user.name = name
        user.lastname = lastname
        user.phone = phone
        user.birthday = birthday
        user.facebook = facebook
        user.twitter = twitter
        user.instagram = instagram
        for biases in bias:
            bias_for_user = Members.get_by_id(int(biases))
            user.bias.append(bias_for_user)
        user.save()
        flash('¡Super, acabas de actualizar tu información personal!')
    return redirect(url_for('profile.index', username=current_user.username))

@profile_bp.route('/email-confirm/')
def email_confirm():
    email = current_user.email
    username = current_user.username
    mail_verification(email=email, username=username)
    flash('¡Revisa tu correo electrónico, recibirás un enlace para verificarlo ;)!')
    return redirect(url_for('profile.index', username=username))