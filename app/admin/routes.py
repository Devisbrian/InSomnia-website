import logging
from flask import render_template, redirect, url_for, abort, current_app, flash
from flask_login import login_required, current_user
from app.auth.decorators import admin_required, staff_required
from app.auth.models import User, Cities

import os
from werkzeug.utils import secure_filename

from app.models import Post
from . import admin_bp
from .forms import CityForm, PostForm, UserAdminForm, CityForm

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
        flash('¡Yeiii, se ha creado el nuevo post ' + title + '!')
        return redirect(url_for('admin.post_form'))
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
        flash('¡Super, has editado el post ' + post.title + '!')
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
    flash('¡El post ' + post.title + ' ha sido eliminado!')
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
    city = Cities.get_by_id(user.id)
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
        flash('¡Has modificado el rol del usuario ' + user.username + '!')
        return redirect(url_for('admin.list_users'))
    return render_template("admin/user_form.html", form=form, user=user, city=city)

@admin_bp.route("/admin/user/delete/<int:user_id>/", methods=['POST', ])
@login_required
@admin_required
def delete_user(user_id):
    # Aquí se elimina un usuario
    logger.info(f'Se va a eliminar al usuario {user_id}')
    user = User.get_by_id(user_id)
    if user is None:
        logger.info(f'El usuario {user_id} no existe')
        flash('Oops, parece que ese usuario no existe ;)')
        abort(404)
    user.delete()
    logger.info(f'El usuario {user_id} ha sido eliminado')
    flash('¡Has eliminado al usuario ' + user.username + '!')
    return redirect(url_for('admin.list_users'))

@admin_bp.route("/admin/add-city/", methods=['POST', 'GET'])
def add_city():
    form = CityForm()
    if form.validate_on_submit():
        name = form.name.data
        city = Cities(name=name)
        city.save()
        flash('¡Qué bien, agregaste la ciudad ' + name + '!')
        return redirect(url_for('admin.add_city'))
    return render_template('admin/city_form.html', form=form)


