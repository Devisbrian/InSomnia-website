from flask import render_template, redirect, url_for, abort, current_app
from flask_login import login_required
from app.auth.decorators import staff_required

from .models import Events, Gallery
from .forms import EventGalleryForm

import os
from werkzeug.utils import secure_filename

from . import fanclub_bp

@login_required
@staff_required
@fanclub_bp.route('/admin/fanclub/add-photos/', methods=['GET','POST'])
def add_fc_photos():
    form = EventGalleryForm()
    if form.validate_on_submit():
        name = form.name.data
        date = form.date.data
        event_file = form.event_image.data
        gallery_files = form.gallery_images.data

        if event_file:
            image_name = secure_filename(event_file.filename)
            images_dir = current_app.config['EVENTS_DIR']
            os.makedirs(images_dir, exist_ok=True)
            file_path = os.path.join(images_dir, image_name)
            event_file.save(file_path)
        event = Events(name=name, date=date)
        event.image_name = image_name
        event.save()

        eventDb = Events.get_by_name(name)
        
        images_dir = current_app.config['EVENTS_DIR']
        for file in gallery_files:
            if file:
                image_name = secure_filename(file.filename)
                os.makedirs(images_dir, exist_ok=True)
                file_path = os.path.join(images_dir, image_name)
                file.save(file_path)
                gallery = Gallery(image_name=image_name, event=eventDb)
                gallery.save()
        return redirect(url_for('fanclub.add_fc_photos'))
    return render_template("fanclub/gallery_form.html", form=form)

@login_required
@staff_required
@fanclub_bp.route('/admin/fanclub/edit/<int:event_id>', methods=['GET','POST'])
def edit_fc_photos(event_id):
    event = Events.get_by_id(event_id)
    if event is None:
        #logger.info(f'El evento no existe')
        abort(404)
    form = EventGalleryForm(obj=event)
    if form.validate_on_submit():
        event.name = form.name.data
        event.date = form.date.data
        event.file = form.event_image.data
        gallery_files = form.gallery_images.data

        if event.file:
            event.image_name = secure_filename(event.file.filename)
            images_dir = current_app.config['EVENTS_DIR']
            os.makedirs(images_dir, exist_ok=True)
            file_path = os.path.join(images_dir, event.image_name)
            event.file.save(file_path)
        event.save()

        eventDb = Events.get_by_name(event.name)
        if gallery_files:
            images_dir = current_app.config['EVENTS_DIR']
            for file in gallery_files:
                image_name = secure_filename(file.filename)
                os.makedirs(images_dir, exist_ok=True)
                file_path = os.path.join(images_dir, image_name)
                file.save(file_path)
                gallery = Gallery(image_name=image_name, event=eventDb)
                gallery.save()
        return redirect(url_for('fanclub.list_gallery'))
    return render_template("fanclub/gallery_form.html", form=form, event=event)

@login_required
@staff_required
@fanclub_bp.route('/admin/fanclub/event/delete/<int:event_id>', methods=['GET','POST'])
def delete_fc_event(event_id):
    event = Events.get_by_id(event_id)
    if event is None:
        #logger.info(f'El evento {event_id} no existe')
        abort(404)
    event.delete()
    return redirect(url_for('fanclub.list_gallery'))

@login_required
@staff_required
@fanclub_bp.route('/admin/fanclub/gallery/delete/<int:photo_id>', methods=['GET','POST'])
def delete_fc_photo(photo_id):
    gallery = Gallery.get_by_id(photo_id)
    if gallery is None:
        #logger.info(f'El evento {event_id} no existe')
        abort(404)
    gallery.delete()
    return redirect(url_for('fanclub.list_gallery'))

@fanclub_bp.route('/fanclub/events-gallery/')
def list_gallery():
    events = Events.get_all()
    return render_template("fanclub/list_gallery.html", events=events)

@fanclub_bp.route('/fanclub/events-gallery/<int:event_id>/')
def gallery_view(event_id):
    event = Events.get_by_id(event_id)
    gallery = Gallery.get_by_event(event_id)
    return render_template("fanclub/gallery_view.html", gallery=gallery, event=event)

