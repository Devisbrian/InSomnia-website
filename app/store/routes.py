import logging
from flask import render_template, redirect, url_for, abort, request, current_app, session, flash
from flask_login import login_required
from app.auth.decorators import staff_required

import os
from werkzeug.utils import secure_filename
from . import store_bp

from .forms import ProductForm
from .models import Product

logger = logging.getLogger(__name__)

@store_bp.route("/admin/store/add", methods=["GET", "POST"])
@login_required
@staff_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        name = form.name.data
        price = form.price.data
        stock = form.stock.data
        file = form.image.data
        description = form.description.data
        fanmade = form.fanmade.data
        image_name = None
        
        product = Product(name=name,price=price,stock=stock,description=description,fanmade=fanmade)
        product.save()
        if file:
            image_name = 'producto-' + str(product.id) + '-'
            image_name += secure_filename(file.filename)
            images_dir = current_app.config['PRODUCTS_DIR']
            os.makedirs(images_dir, exist_ok=True)
            file_path = os.path.join(images_dir, image_name)
            file.save(file_path)
        product.image_name = image_name
        product.save()
        flash('¡Yujuuu, has agregado el producto ' + name + ' a la venta!')
        return redirect(url_for('store.list_products'))
    return render_template("store/product_form.html", form=form)

@store_bp.route('/admin/store/<int:product_id>', methods=["GET", "POST"])
@login_required
@staff_required
def update_product(product_id):
    product = Product.get_by_id(product_id)
    if product is None:
        logger.info(f'El producto {product_id} no existe')
        flash('¡Oops, parece que ese producto no existe!')
        abort(404)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data
        product.stock = form.stock.data
        product.file = form.image.data
        product.description = form.description.data
        product.fanmade = form.fanmade.data

        if product.file:
            old_image_name = product.image_name
            images_dir = current_app.config['PRODUCTS_DIR']
            old_file_path = os.path.join(images_dir, old_image_name)
            os.remove(old_file_path)

            product.image_name = 'producto-' + str(product.id) + '-'
            product.image_name += secure_filename(product.file.filename)
            os.makedirs(images_dir, exist_ok=True)
            file_path = os.path.join(images_dir, product.image_name)
            product.file.save(file_path)
        product.save()
        logger.info(f'Guardando el producto {product_id}')
        flash('¡Super, has editado el producto ' + product.name + '!')
        return redirect(url_for('store.list_products'))
    return render_template("store/product_form.html", form=form)

@store_bp.route("/admin/store/delete/<int:product_id>", methods=['GET', ])
@login_required
@staff_required
def delete_product(product_id):
    product = Product.get_by_id(product_id)
    if product is None:
        flash('¡Oops, parece que ese producto ya no existe')
        abort(404)
    image_name = product.image_name
    images_dir = current_app.config['PRODUCTS_DIR']
    file_path = os.path.join(images_dir, image_name)
    os.remove(file_path)
    product.delete()
    flash('¡El producto ' + product.name + ' ha sido borrado!')
    return redirect(url_for('store.list_products'))

@store_bp.route("/store/")
def list_products():
    products = Product.get_all()
    return render_template('store/list_products.html', products=products)

@store_bp.route("/store/cart/")
def cart_view():
    if not 'products' in session:
        products = None
        flash('¡Ummm, parece que el carrito de compras está vacío!')
        flash('¿Qué tal si agregas un producto?')
    else:
        products = session['products']

    total = 0
    total_quantity = 0
    try:
        for product in products:
            total += product[4]
            total_quantity += product[2]
    except:
        None
    return render_template("store/cart_view.html", products=products, total=total, total_quantity=total_quantity) 

@store_bp.route("/store/cart/add/<int:product_id>", methods=['GET', 'POST'])
def addto_cart(product_id):
    if request.method == 'POST':
        quantity = int(request.form.get('addquantity'))
        if not 'products' in session:
            session['products'] = []
        products = session['products']
        product_name = Product.get_by_id(product_id)
        product = [product_id, product_name.name, quantity, product_name.price, quantity*product_name.price]
        products.append(product)
        session['products'] = products
        product = Product.get_by_id(product_id)
        flash('¡Yeiii, has agregado el producto ' + product_name.name + ' al carrito!')
        return redirect(url_for('store.cart_view'))
    return redirect(url_for('store.list_products'))

@store_bp.route("/store/cart/delete/<product>", methods=['GET', 'POST'])
def deleteto_cart(product):
    products = session['products']
    if product == "all":
        products.clear()
        flash('¡Ohhh, has borrado todos los productos del carrito')
    else:
        index = int(product)
        products.pop(index)
        flash('¡Has borrado un producto del carrito!')
    session['products'] = products
    return redirect(url_for('store.cart_view'))