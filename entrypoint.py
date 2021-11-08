import os
from flask import send_from_directory

from app import create_app


settings_module = os.getenv('APP_SETTINGS_MODULE')
app = create_app(settings_module)


@app.route('/media/users/<filename>')
def media_users(filename):
    dir_path = os.path.join(
        app.config['MEDIA_DIR'],
        app.config['USER_PIC_DIR'])
    return send_from_directory(dir_path, filename)

@app.route('/media/posts/<filename>')
def media_posts(filename):
    dir_path = os.path.join(
        app.config['MEDIA_DIR'],
        app.config['POSTS_IMAGES_DIR'])
    return send_from_directory(dir_path, filename)

@app.route('/media/photocards/<filename>')
def media_photocards(filename):
    dir_path = os.path.join(
        app.config['MEDIA_DIR'],
        app.config['PCS_IMAGES_DIR'])
    return send_from_directory(dir_path, filename)

@app.route('/media/albums/<filename>')
def media_albums(filename):
    dir_path = os.path.join(
        app.config['MEDIA_DIR'],
        app.config['ALBUMS_IMAGES_DIR'])
    return send_from_directory(dir_path, filename)

@app.route('/media/fanclub/events/<filename>')
def media_galery(filename):
    dir_path = os.path.join(
        app.config['MEDIA_DIR'],
        app.config['EVENTS_DIR'])
    return send_from_directory(dir_path, filename)

@app.route('/media/products/<filename>')
def media_products(filename):
    dir_path = os.path.join(
        app.config['MEDIA_DIR'],
        app.config['PRODUCTS_DIR'])
    return send_from_directory(dir_path, filename)