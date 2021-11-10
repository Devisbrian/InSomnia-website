import logging
from flask import render_template, redirect, url_for, abort, current_app, jsonify, flash
from flask_login import login_required
from app.auth.decorators import admin_required, staff_required

import os
from werkzeug.utils import secure_filename

from .models import PhotocardDb, AlbumType, Album, Members
from . import dreamcatcher_bp
from .forms import PhotocardDbForm, AlbumTypeForm, AlbumForm, MemberDcForm

logger = logging.getLogger(__name__)


@dreamcatcher_bp.route("/admin/album", methods=['GET', 'POST'])
@login_required
@staff_required
def album_add():
    form = AlbumForm()
    if form.validate_on_submit():
        album = form.album.data
        date = form.date.data
        songs = form.songs.data
        producers = form.producers.data
        spotify = form.spotify.data
        youtube = form.youtube.data
        file = form.album_image.data
        album_image_name = None
        albumdb = Album(album=album, date=date, songs=songs, producers=producers, spotify=spotify, youtube=youtube)
        albumdb.save()
        if file:
            album_image_name = 'album-' + str(album.id) + '-'
            album_image_name += secure_filename(file.filename)
            images_dir = current_app.config['ALBUMS_IMAGES_DIR']
            os.makedirs(images_dir, exist_ok=True)
            file_path = os.path.join(images_dir, album_image_name)
            file.save(file_path)
        albumdb.album_image_name = album_image_name
        albumdb.save()
        logger.info(f'Guardando nuevo album {album}')
        flash('¡Yujuuu, agregaste el álbum ' + album + '!')
        return redirect(url_for('public.list_albums'))
    return render_template("dreamcatcher/album_form.html", form=form)

@dreamcatcher_bp.route("/admin/album/<int:album_id>", methods=['GET', 'POST'])
@login_required
@staff_required
def update_album_form(album_id):
    album = Album.get_by_id(album_id)
    if album is None:
        logger.info(f'El album no existe')
        abort(404)
    form = AlbumForm(obj=album)
    if form.validate_on_submit():
        album.album = form.album.data
        album.date = form.date.data
        album.songs = form.songs.data
        album.producers = form.producers.data
        album.spotify = form.spotify.data
        album.youtube = form.youtube.data
        album.file = form.album_image.data
        if album.file:

            old_file_name = album.album_image_name
            images_dir = current_app.config['ALBUMS_IMAGES_DIR']
            old_file_path = os.path.join(images_dir, old_file_name)
            os.remove(old_file_path)

            album.album_image_name = 'album-' + str(album.id) + '-'
            album.album_image_name += secure_filename(album.file.filename)
            os.makedirs(images_dir, exist_ok=True)
            file_path = os.path.join(images_dir, album.album_image_name)
            album.file.save(file_path)
        album.save()
        logger.info(f'Guardando el álbum {album_id}')
        flash('¡Has editado el álbum ' + album.album + '!')
        return redirect(url_for('public.list_albums'))
    return render_template("dreamcatcher/album_form.html", album=album, form=form)

@dreamcatcher_bp.route("/admin/album/delete/<int:album_id>/", methods=['POST', ])
@login_required
@staff_required
def delete_album(album_id):
    logger.info(f'Se va a eliminar el album {album_id}')
    album = Album.get_by_id(album_id)
    if album is None:
        logger.info(f'El album {album_id} no existe')
        flash('¡Oops, parece que ese álbum ya no existe!')
        abort(404)
    
    file_name = album.album_image_name
    images_dir = current_app.config['ALBUMS_IMAGES_DIR']
    file_path = os.path.join(images_dir, file_name)
    os.remove(file_path)

    album.delete()
    logger.info(f'El album {album_id} ha sido eliminado')
    flash('¡El álbum ' + album.album + ' ha sido borrado!')
    return redirect(url_for('public.list_albums'))

@dreamcatcher_bp.route("/admin/album-type-database", methods=['GET', 'POST'])
@login_required
@staff_required
def albumtype_add():
    form = AlbumTypeForm()
    form.album.choices = [(albums.album, albums.album) for albums in Album.get_all()]
    form.album.choices.insert(0, ("", "Seleccione"))
    if form.validate_on_submit():
        album = form.album.data
        pc_type = form.pc_type.data
        albumDb = Album.get_by_album(album)
        albumtype = AlbumType(album=albumDb, pc_type=pc_type)
        albumtype.save()
        logger.info(f'Guardando nueva categoria de photocard')
        flash('¡Yeiii, has creado la nueva categoría de photocard ' + pc_type + ' para el álbum ' + album + '!')
        return redirect(url_for('dreamcatcher.albumtype_add'))
    return render_template("dreamcatcher/albumtype_form.html", form=form)

@dreamcatcher_bp.route("/admin/pctype/", methods=['GET', 'POST'])
@login_required
@staff_required
def list_albumtype():
    album_type = AlbumType.get_all()
    albums = AlbumType.get_album_distinct()
    return render_template("dreamcatcher/albumtype.html", album_type=album_type, albums=albums)

@dreamcatcher_bp.route("/admin/pctype/<int:album_type_id>", methods=['GET', 'POST'])
@login_required
@staff_required
def update_albumtype_form(album_type_id):
    album_type = AlbumType.get_by_id(album_type_id)
    if album_type is None:
        logger.info(f'La categoría de photocard no existe')
        flash('¡Oops, parece que esa categoría de photocard no existe!')
        abort(404)
    form = AlbumTypeForm(obj=album_type)
    form.album.choices = [(albums.album, albums.album) for albums in Album.get_all()]
    form.album.choices.insert(0, ("", "Seleccione"))
    if form.validate_on_submit():
        album = form.album.data
        album_type.pc_type = form.pc_type.data
        albumDb = Album.get_by_album(album)
        album_type.album = albumDb
        album_type.save()
        flash('¡Has editado la categoría ' + album_type.pc_type + ' del álbum ' + album_type.album.album + '!')
        return redirect(url_for('dreamcatcher.list_albumtype'))
    return render_template("dreamcatcher/albumtype_form.html", album_type=album_type, form=form)

@dreamcatcher_bp.route("/admin/pctype/delete/<int:album_type_id>/", methods=['POST', ])
@login_required
@staff_required
def delete_albumtype(album_type_id):
    logger.info(f'Se va a eliminar la categoria {album_type_id}')
    pc_type = AlbumType.get_by_id(album_type_id)
    if pc_type is None:
        logger.info(f'La categoria {album_type_id} no existe')
        flash('¡Oops, parece que esa categoría de photocard no existe!')
        abort(404)
    pc_type.delete()
    logger.info(f'La categoria {album_type_id} ha sido eliminada')
    flash('La categoría de photocard ' + pc_type.pc_type + ' ha sido borrada!')
    return redirect(url_for('dreamcatcher.list_albumtype'))

@dreamcatcher_bp.route("/admin/photocard", methods=['GET', 'POST'])
@login_required
@staff_required
def photocarddb_add():
    form = PhotocardDbForm()
    form.album.choices = [(albums.album, albums.album) for albums in Album.get_all()]
    form.album.choices.insert(0, ("", "Seleccione"))
    form.pc_type.choices = [(pc_type.pc_type, pc_type.pc_type) for pc_type in AlbumType.get_all()]
    form.pc_type.choices.insert(0, ("", "Seleccione"))
    form.member.choices = [(members.name, members.name) for members in Members.get_all()]
    form.member.choices.insert(0, ("", "Seleccione"))
    if form.validate_on_submit():
        album = form.album.data #foreign
        member = form.member.data #foreign
        pc_type = form.pc_type.data #foreign
        pc_name = form.pc_name.data
        file = form.photocard_image.data
        pc_image_name = None
        albumDb = Album.get_by_album(album)
        memberDb = Members.get_by_name(member)
        pc_typeDb = AlbumType.get_by_type(pc_type)
        pc_db = PhotocardDb(album=albumDb, member=memberDb, pc_type=pc_typeDb, pc_name=pc_name)
        pc_db.save()
        if file:
            pc_image_name = 'pc-' + str(pc_db.id) + '-'
            pc_image_name += secure_filename(file.filename)
            images_dir = current_app.config['PCS_IMAGES_DIR']
            os.makedirs(images_dir, exist_ok=True)
            file_path = os.path.join(images_dir, pc_image_name)
            file.save(file_path)
        pc_db.pc_image_name = pc_image_name
        pc_db.save()
        logger.info(f'Guardando nueva photocard {pc_name}')
        flash('¡Yujuuu, has creado la nueva photocard ' + pc_name + '!')
        return redirect(url_for('public.list_photocards'))
    return render_template("dreamcatcher/photocarddb_form.html", form=form)

@dreamcatcher_bp.route("/admin/photocard/<int:pc_id>", methods=['GET', 'POST'])
@login_required
@staff_required
def update_photocard_form(pc_id):
    photocard = PhotocardDb.get_by_id(pc_id)
    if photocard is None:
        logger.info(f'La photocard no existe')
        flash('¡Oops, parece que esa photocard no existe!')
        abort(404)
    form = PhotocardDbForm(obj=photocard)
    form.album.choices = [(albums.album, albums.album) for albums in Album.get_all()]
    form.album.choices.insert(0, ("", "Seleccione"))
    form.pc_type.choices = [(pc_type.pc_type, pc_type.pc_type) for pc_type in AlbumType.get_all()]
    form.pc_type.choices.insert(0, ("", "Seleccione"))
    form.member.choices = [(members.name, members.name) for members in Members.get_all()]
    form.member.choices.insert(0, ("", "Seleccione"))

    if form.validate_on_submit():
        album = form.album.data
        member = form.member.data
        pc_type = form.pc_type.data
        photocard.pc_name = form.pc_name.data
        photocard.file = form.photocard_image.data

        albumDb = Album.get_by_album(album)
        memberDb = Members.get_by_name(member)
        pc_typeDb = AlbumType.get_by_type(pc_type)

        photocard.album = albumDb
        photocard.member = memberDb
        photocard.pc_type = pc_typeDb

        if photocard.file:
            old_file_name = photocard.pc_image_name
            images_dir = current_app.config['PCS_IMAGES_DIR']
            old_file_path = os.path.join(images_dir, old_file_name)
            os.remove(old_file_path)

            photocard.pc_image_name = 'pc-' + str(photocard.id) + '-'
            photocard.pc_image_name += secure_filename(photocard.file.filename)
            os.makedirs(images_dir, exist_ok=True)
            file_path = os.path.join(images_dir, photocard.pc_image_name)
            photocard.file.save(file_path)
        photocard.save()
        logger.info(f'Guardando la photocard {pc_id}')
        flash('¡Has editado la photocard ' + photocard.pc_name + '!')
        return redirect(url_for('public.list_photocards'))
    return render_template("dreamcatcher/photocarddb_form.html", photocard=photocard, form=form)

@dreamcatcher_bp.route("/admin/photocard/delete/<int:photocard_id>/", methods=['POST', ])
@login_required
@staff_required
def delete_photocard(photocard_id):
    logger.info(f'Se va a eliminar la photocard {photocard_id}')
    photocard = PhotocardDb.get_by_id(photocard_id)
    if photocard is None:
        logger.info(f'La photocard {photocard_id} no existe')
        flash('Oops, parece que esa photocard no existe!')
        abort(404)
    old_file_name = photocard.pc_image_name
    images_dir = current_app.config['PCS_IMAGES_DIR']
    old_file_path = os.path.join(images_dir, old_file_name)
    os.remove(old_file_path)
    photocard.delete()
    logger.info(f'La photocard {photocard_id} ha sido eliminada')
    flash('¡La photocard ' + photocard.pc_name + ' ha sido borrada!')
    return redirect(url_for('public.list_photocards'))

@dreamcatcher_bp.route("/admin/dcmembers/", methods=['POST', 'GET'])
@login_required
@admin_required
def dc_members():
    form = MemberDcForm()
    if form.validate_on_submit():
        name = form.member.data
        memberdb = Members(name=name)
        memberdb.save()
        return redirect(url_for('dreamcatcher.dc_members'))
    return render_template('dreamcatcher/dcmembers_form.html', form=form)


# Jsonify
@dreamcatcher_bp.route("/pc_type/<album>")
def pc_type(album):
    albums = Album.get_by_album(album)
    pc_types = AlbumType.get_by_album(albums.id)
    
    pc_typeArray = []
    
    for pc_type in pc_types:
        pc_typeObj = {}
        pc_typeObj['value'] = pc_type.pc_type
        pc_typeObj['name'] = pc_type.pc_type
        pc_typeArray.append(pc_typeObj)
        
    return jsonify({'pc_types' : pc_typeArray})