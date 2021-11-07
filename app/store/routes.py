from flask import render_template, redirect, url_for, abort, request, current_app, session, flash
from flask_login import login_required
from app.auth.decorators import staff_required

import os
from werkzeug.utils import secure_filename
from . import store_bp

from .forms import ProductForm
from .models import Product

@login_required
@staff_required
@store_bp.route("/admin/store/add", methods=["GET", "POST"])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        name = form.name.data
        price = form.price.data
        stock = form.stock.data
        file = form.image.data
        description = form.description.data
        fanmade = form.fanmade.data

        if file:
            image_name = secure_filename(file.filename)
            images_dir = current_app.config['PRODUCTS_DIR']
            os.makedirs(images_dir, exist_ok=True)
            file_path = os.path.join(images_dir, image_name)
            file.save(file_path)

        product = Product(name=name,price=price,stock=stock,description=description,fanmade=fanmade, image_name=image_name)
        product.save()
        flash('¡Yujuuu, has agregado el producto ' + name + ' a la venta!')
        return redirect(url_for('store.list_products'))
    return render_template("store/product_form.html", form=form)

@login_required
@staff_required
@store_bp.route("/admin/store/delete/<int:product_id>", methods=["POST", ])
def delete_product(product_id):
    product = Product.get_by_id(product_id)
    if product is None:
        flash('¡Oops, parece que ese producto ya no existe')
        abort(404)
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