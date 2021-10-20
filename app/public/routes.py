import logging

from flask import abort, render_template, request, current_app, redirect, url_for
from werkzeug.exceptions import NotFound
from flask_login import current_user, login_required
from .forms import CommentForm, ExchangeForm
from app.models import Post, Comment, PhotocardDb, PhotocardExchange, Album, AlbumType, Members
from . import public_bp

logger = logging.getLogger(__name__)

@public_bp.route("/")
def index():
    logger.info('Mostrando la página principal')
    page = int(request.args.get('page', 1))
    per_page = current_app.config['ITEMS_PER_PAGE']
    post_pagination = Post.all_paginated(page, per_page)
    
    return render_template("public/index.html", post_pagination=post_pagination)


@public_bp.route("/p/<string:slug>/", methods=['GET', 'POST'])
def show_post(slug):
    logger.info('Mostrando un post')
    logger.debug(f'Slug: {slug}')
    post = Post.get_by_slug(slug)
    if not post:
        logger.info(f'El post {slug} no existe')
        abort(404)
    form = CommentForm()
    if current_user.is_authenticated and form.validate_on_submit():
        content = form.content.data
        comment = Comment(content=content, user_id=current_user.id,
                          user_username=current_user.username, post_id=post.id)
        comment.save()
        return redirect(url_for('public.show_post', slug=post.title_slug))
    return render_template("public/post_view.html", post=post, form=form)

@public_bp.route("/photocards/", methods=['GET', 'POST'])
def list_photocards():
    photocards = PhotocardDb.get_all()
    albums = PhotocardDb.get_albums()
    pc_types = PhotocardDb.get_type()
    return render_template("public/photocards.html", photocards=photocards, albums=albums, pc_types=pc_types)

@public_bp.route("/albums/")
def list_albums():
    albums = Album.get_all()
    return render_template("public/albums.html", albums=albums)

#@public_bp.route("/pc/<string:pc_name>/", methods=['GET', 'POST'])
#def show_pcs(pc_name):
#    photocard = PhotocardDb.get_by_pcname(pc_name)
#    if not photocard:
#        logger.info(f'La photocard {pc_name} no existe')
#        abort(404)
#    return render_template("public/photocard_view.html", photocard=photocard)

@public_bp.route("/exchange/", methods=['GET', ])
def show_exchange():
    exchanges = PhotocardExchange.get_all()
    for exchange in exchanges:
        print(exchange.user)
    return render_template("public/exchange_view.html", exchanges=exchanges)

@public_bp.route("/exchange/create/", methods=['GET', 'POST'])
@login_required
def exchange_form():
    # Crea un nuevo post
    form = ExchangeForm()

    form.album_from.choices = [(albums.album, albums.album) for albums in Album.get_all()]
    form.album_from.choices.insert(0, ("", "Seleccione"))
    form.album_to.choices = [(albums.album, albums.album) for albums in Album.get_all()]
    form.album_to.choices.insert(0, ("", "Seleccione"))

    form.pc_type_from.choices = [(pc_type.pc_type, pc_type.pc_type) for pc_type in AlbumType.get_all()]
    form.pc_type_from.choices.insert(0, ("", "Seleccione"))
    form.pc_type_to.choices = [(pc_type.pc_type, pc_type.pc_type) for pc_type in AlbumType.get_all()]
    form.pc_type_to.choices.insert(0, ("", "Seleccione"))

    form.member_from.choices = [(member.name, member.name) for member in Members.get_all()]
    form.member_from.choices.insert(0, ("", "Seleccione"))
    form.member_to.choices = [(member.name, member.name) for member in Members.get_all()]
    form.member_to.choices.insert(0, ("", "Seleccione"))

    if form.validate_on_submit():
        album_from = form.album_from.data
        member_from = form.member_from.data
        pc_type_from = form.pc_type_from.data
        album_to = form.album_to.data
        member_to = form.member_to.data
        pc_type_to = form.pc_type_to.data

        # Consultas
        album_f = Album.get_by_album(album_from)
        album_t = Album.get_by_album(album_to)
        member_f = Members.get_by_name(member_from)
        member_t = Members.get_by_name(member_to)
        pc_type_f = AlbumType.get_by_type(pc_type_from)
        pc_type_t = AlbumType.get_by_type(pc_type_to)

        pc_from = PhotocardDb.get_filtered(album_f.id, pc_type_f.id, member_f.id)
        pc_to = PhotocardDb.get_filtered(album_t.id, pc_type_t.id, member_t.id)

        exchange = PhotocardExchange(user_id=current_user.id)
        exchange.pc_from.append(pc_from)
        exchange.pc_to.append(pc_to)
        print(exchange.pc_from)
        print(exchange.pc_to)
        exchange.save()
        logger.info(f'Guardando nueva entrada photocardExchange')
        return redirect(url_for('public.index'))
    return render_template("public/post_exchange.html", form=form)