import logging
from flask import render_template, redirect, url_for, abort, request, current_app, jsonify
from flask_login import login_required, current_user
from app.auth.decorators import admin_required, staff_required
from app.auth.models import User

import os
from werkzeug.utils import secure_filename

from app.models import Post, PhotocardDb, AlbumType, Album
from . import admin_bp
from .forms import PostForm, UserAdminForm, PhotocardDbForm, AlbumTypeForm, AlbumForm

logger = logging.getLogger(__name__)

@admin_bp.route("/admin/")
@login_required
@staff_required
def index():
    return render_template("admin/index.html")


@admin_bp.route("/admin/post/", methods=['GET', 'POST'])
@login_required
@staff_required
def post_form():
    # Crea un nuevo post
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        content = form.content.data
        file = form.post_image.data
        image_name = None
        # Comprueba si la petición contiene la parte del fichero
        if file:
            image_name = secure_filename(file.filename)
            images_dir = current_app.config['POSTS_IMAGES_DIR']
            os.makedirs(images_dir, exist_ok=True)
            file_path = os.path.join(images_dir, image_name)
            file.save(file_path)
        post = Post(user_id=current_user.id, title=title, description=description, content=content)
        post.image_name = image_name
        post.save()
        logger.info(f'Guardando nuevo post {title}')
        return redirect(url_for('public.index'))
    return render_template("admin/post_form.html", form=form)


@admin_bp.route("/admin/post/<int:post_id>/", methods=['GET', 'POST'])
@login_required
@staff_required
def update_post_form(post_id):
    # Actualiza un post existente
    post = Post.get_by_id(post_id)
    if post is None:
        logger.info(f'El post {post_id} no existe')
        abort(404)
    # Crea un formulario inicializando los campos con
    # los valores del post.
    form = PostForm(obj=post)
    if form.validate_on_submit():
        # Actualiza los campos del post existente
        post.title = form.title.data
        post.description = form.description.data
        post.content = form.content.data
        post.file = form.post_image.data

        # Comprueba si la petición contiene la parte del fichero
        if post.file:
            post.image_name = secure_filename(post.file.filename)
            images_dir = current_app.config['POSTS_IMAGES_DIR']
            os.makedirs(images_dir, exist_ok=True)
            file_path = os.path.join(images_dir, post.image_name)
            post.file.save(file_path)
        post.save()
        logger.info(f'Guardando el post {post_id}')
        return redirect(url_for('public.index'))
    return render_template("admin/post_form.html", form=form, post=post)

@admin_bp.route("/admin/post/delete/<int:post_id>/", methods=['POST', ])
@login_required
@staff_required
def delete_post(post_id):
    # Elimina un post existente
    logger.info(f'Se va a eliminar el post {post_id}')
    post = Post.get_by_id(post_id)
    if post is None:
        logger.info(f'El post {post_id} no existe')
        abort(404)
    post.delete()
    logger.info(f'El post {post_id} ha sido eliminado')
    return redirect(url_for('public.index'))


@admin_bp.route("/admin/users/")
@login_required
@staff_required
def list_users():
    users = User.get_all()
    return render_template("admin/users.html", users=users)

@admin_bp.route("/admin/user/<int:user_id>/", methods=['GET', 'POST'])
@login_required
@staff_required
def update_user_form(user_id):
    # Aquí entra para actualizar un usuario existente
    user = User.get_by_id(user_id)
    if user is None:
        logger.info(f'El usuario {user_id} no existe')
        abort(404)
    # Crea un formulario inicializando los campos con
    # los valores del usuario.
    form = UserAdminForm(obj=user)
    if form.validate_on_submit():
        # Actualiza los campos del usuario existente
        user.is_admin = form.is_admin.data
        user.is_staff = form.is_staff.data
        user.save()
        logger.info(f'Guardando el usuario {user_id}')
        return redirect(url_for('admin.list_users'))
    return render_template("admin/user_form.html", form=form, user=user)

@admin_bp.route("/admin/user/delete/<int:user_id>/", methods=['POST', ])
@login_required
@admin_required
def delete_user(user_id):
    # Aquí se elimina un usuario
    logger.info(f'Se va a eliminar al usuario {user_id}')
    user = User.get_by_id(user_id)
    if user is None:
        logger.info(f'El usuario {user_id} no existe')
        abort(404)
    user.delete()
    logger.info(f'El usuario {user_id} ha sido eliminado')
    return redirect(url_for('admin.list_users'))


@admin_bp.route("/admin/album", methods=['GET', 'POST'])
@login_required
@staff_required
def album_add():
    form = AlbumForm()
    if form.validate_on_submit():
        album = form.album.data
        file = form.album_image.data
        album_image_name = None
        if file:
            album_image_name = secure_filename(file.filename)
            images_dir = current_app.config['ALBUMS_IMAGES_DIR']
            os.makedirs(images_dir, exist_ok=True)
            file_path = os.path.join(images_dir, album_image_name)
            file.save(file_path)
        albumdb = Album(album=album)
        albumdb.album_image_name = album_image_name
        albumdb.save()
        logger.info(f'Guardando nuevo album {album}')
        return redirect(url_for('admin.index'))
    return render_template("admin/album_form.html", form=form)

@admin_bp.route("/admin/album/<int:album_id>", methods=['GET', 'POST'])
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
        album.file = form.album_image.data
        album.album_image_name = None
        if album.file:
            album.album_image_name = secure_filename(album.file.filename)
            images_dir = current_app.config['ALBUMS_IMAGES_DIR']
            os.makedirs(images_dir, exist_ok=True)
            file_path = os.path.join(images_dir, album.album_image_name)
            album.file.save(file_path)
        album.save()
        logger.info(f'Guardando el álbum {album_id}')
        return redirect(url_for('public.list_album'))
    return render_template("admin/album_form.html", album=album, form=form)

@admin_bp.route("/admin/album/delete/<int:album_id>/", methods=['POST', ])
@login_required
@staff_required
def delete_album(album_id):
    logger.info(f'Se va a eliminar el album {album_id}')
    album = Album.get_by_id(album_id)
    if album is None:
        logger.info(f'El album {album_id} no existe')
        abort(404)
    album.delete()
    logger.info(f'El album {album_id} ha sido eliminado')
    return redirect(url_for('public.list_albums'))



@admin_bp.route("/admin/album-type-database", methods=['GET', 'POST'])
@login_required
@staff_required
def albumtype_add():
    form = AlbumTypeForm()
    form.album.choices = [(albums.album, albums.album) for albums in Album.get_all()]
    form.album.choices.insert(0, ("", "Seleccione"))
    if form.validate_on_submit():
        album = form.album.data
        pc_type = form.pc_type.data
        albumtype = AlbumType(album=album, pc_type=pc_type)
        albumtype.save()
        logger.info(f'Guardando nueva categoria de photocard')
        return redirect(url_for('admin.index'))
    return render_template("admin/albumtype_form.html", form=form)

@admin_bp.route("/admin/pctype/", methods=['GET', 'POST'])
@login_required
@staff_required
def list_albumtype():
    album_type = AlbumType.get_all()
    return render_template("admin/albumtype.html", album_type=album_type)

@admin_bp.route("/admin/pctype/<int:album_type_id>", methods=['GET', 'POST'])
@login_required
@staff_required
def update_albumtype_form(album_type_id):
    album_type = AlbumType.get_by_id(album_type_id)
    if album_type is None:
        logger.info(f'La categoría de photocard no existe')
        abort(404)
    form = AlbumTypeForm(obj=album_type)
    form.album.choices = [(albums.album, albums.album) for albums in Album.get_all()]
    form.album.choices.insert(0, ("", "Seleccione"))
    if form.validate_on_submit():
        album_type.album = form.album.data
        album_type.pc_type = form.pc_type.data
        album_type.save()
        return redirect(url_for('admin.list_albumtype'))
    return render_template("admin/albumtype_form.html", album_type=album_type, form=form)

@admin_bp.route("/admin/pctype/delete/<int:album_type_id>/", methods=['POST', ])
@login_required
@staff_required
def delete_albumtype(album_type_id):
    logger.info(f'Se va a eliminar la categoria {album_type_id}')
    pc_type = AlbumType.get_by_id(album_type_id)
    if pc_type is None:
        logger.info(f'La categoria {album_type_id} no existe')
        abort(404)
    pc_type.delete()
    logger.info(f'La categoria {album_type_id} ha sido eliminada')
    return redirect(url_for('admin.list_albumtype'))


@admin_bp.route("/admin/photocard", methods=['GET', 'POST'])
@login_required
@staff_required
def photocarddb_add():
    form = PhotocardDbForm()
    form.album.choices = [(albums.album, albums.album) for albums in Album.get_all()]
    form.album.choices.insert(0, ("", "Seleccione"))
    form.pc_type.choices = [(pc_type.pc_type, pc_type.pc_type) for pc_type in AlbumType.get_all()]
    form.pc_type.choices.insert(0, ("", "Seleccione"))
    if form.validate_on_submit():
        album = form.album.data
        member = form.member.data
        pc_type = form.pc_type.data
        pc_name = form.pc_name.data
        file = form.photocard_image.data
        pc_image_name = None
        
        if file:
            pc_image_name = secure_filename(file.filename)
            images_dir = current_app.config['PCS_IMAGES_DIR']
            os.makedirs(images_dir, exist_ok=True)
            file_path = os.path.join(images_dir, pc_image_name)
            file.save(file_path)
        pc_db = PhotocardDb(album=album, member=member, pc_type=pc_type, pc_name=pc_name)
        pc_db.pc_image_name = pc_image_name
        pc_db.save()
        logger.info(f'Guardando nueva photocard {pc_name}')
        return redirect(url_for('public.list_photocards'))
    return render_template("admin/photocarddb_form.html", form=form)

@admin_bp.route("/admin/photocard/<int:pc_id>", methods=['GET', 'POST'])
@login_required
@staff_required
def update_photocard_form(pc_id):
    photocard = PhotocardDb.get_by_id(pc_id)
    if photocard is None:
        logger.info(f'La photocard no existe')
        abort(404)
    form = PhotocardDbForm(obj=photocard)
    form.album.choices = [(albums.album, albums.album) for albums in Album.get_all()]
    form.album.choices.insert(0, ("", "Seleccione"))
    form.pc_type.choices = [(pc_type.pc_type, pc_type.pc_type) for pc_type in AlbumType.get_all()]
    form.pc_type.choices.insert(0, ("", "Seleccione"))

    if form.validate_on_submit():
        photocard.album = form.album.data
        photocard.member = form.member.data
        photocard.pc_type = form.pc_type.data
        photocard.pc_name = form.pc_name.data
        photocard.file = form.photocard_image.data

        if photocard.file:
            photocard.pc_image_name = secure_filename(photocard.file.filename)
            images_dir = current_app.config['PCS_IMAGES_DIR']
            os.makedirs(images_dir, exist_ok=True)
            file_path = os.path.join(images_dir, photocard.pc_image_name)
            photocard.file.save(file_path)
        photocard.save()
        logger.info(f'Guardando la photocard {pc_id}')
        return redirect(url_for('public.list_photocards'))
    return render_template("admin/photocarddb_form.html", photocard=photocard, form=form)

@admin_bp.route("/admin/photocard/delete/<int:photocard_id>/", methods=['POST', ])
@login_required
@staff_required
def delete_photocard(photocard_id):
    logger.info(f'Se va a eliminar la categoria {photocard_id}')
    photocard = PhotocardDb.get_by_id(photocard_id)
    if photocard is None:
        logger.info(f'La categoria {album_type_id} no existe')
        abort(404)
    photocard.delete()
    logger.info(f'La photocard {photocard_id} ha sido eliminada')
    return redirect(url_for('public.list_photocards'))


# FILTROS Jsonify
@admin_bp.route("/pc_type/<album>")
def pc_type(album):
    pc_types = AlbumType.get_by_album(album)
    
    pc_typeArray = []
    
    for pc_type in pc_types:
        pc_typeObj = {}
        pc_typeObj['value'] = pc_type.pc_type
        pc_typeObj['name'] = pc_type.pc_type
        pc_typeArray.append(pc_typeObj)
        
    return jsonify({'pc_types' : pc_typeArray})