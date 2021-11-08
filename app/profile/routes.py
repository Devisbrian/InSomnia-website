from flask import render_template, redirect, url_for, abort, current_app, flash, jsonify, request
from flask_login import login_required, current_user
import logging

from app.auth.models import User
from .forms import AddProfilePic, AddAlbums, AddPhotocards
from app.dreamcatcher.models import Album, Members, PhotocardDb, AlbumType

import os
from werkzeug.utils import secure_filename
from . import profile_bp

logger = logging.getLogger(__name__)


@profile_bp.route('/profile/<username>/')
@login_required
def index(username):
    user = User.get_by_username(username)
    if current_user.id != user.id:
        flash('¡Oops, no tienes permisos para ver el perfil de otra persona!')
        return redirect(url_for('public.index'))
    form = AddProfilePic(obj=user)

    albumForm = AddAlbums(obj=user)
    albumForm.albums.choices = [(albums.album, albums.album) for albums in Album.get_all()]
    albumForm.albums.choices.insert(0, ("", "Seleccione"))

    pcForm = AddPhotocards(obj=user)
    pcForm.album.choices = [(albums.album, albums.album) for albums in Album.get_all()]
    pcForm.album.choices.insert(0, ("", "Seleccione"))
    pcForm.album_type.choices = [(album_type.pc_type, album_type.pc_type) for album_type in AlbumType.get_all()]
    pcForm.album_type.choices.insert(0, ("", "Seleccione"))
    pcForm.members.choices = [(member.name, member.name) for member in Members.get_all()]
    pcForm.members.choices.insert(0, ("", "Seleccione"))

    return render_template('profile/index.html', user=user, form=form, albumForm=albumForm, pcForm=pcForm)

@profile_bp.route('/profile/pic_upload/', methods=['GET', 'POST'])
def pic_upload():
    user_id = current_user.id
    user = User.get_by_id(user_id)
    form = AddProfilePic(obj=user)
    if form.validate_on_submit():
        file = form.profile_pic.data
        pic_name = None
        if file:
            pic_name = secure_filename(file.filename)
            images_dir = current_app.config['USER_PIC_DIR']
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
        for album in albums:
            album_for_user = Album.get_by_album(album)
            user.albums.append(album_for_user)
        user.save()
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
            user.photocards.append(pc_for_user)
        user.save()
    return redirect(url_for('profile.index', username=current_user.username))

