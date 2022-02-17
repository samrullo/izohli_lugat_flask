from . import main_bp
from flask import render_template, flash, redirect, url_for
from .forms import ProductForm,CategoryForm
from application.main.models import Product, Category, db

@main_bp.app_context_processor
def inject_functions():
    return {'getattr':getattr}

@main_bp.route("/")
def home():
    return render_template("index.html")


@main_bp.route("/products")
def products():
    products = Product.query.all()
    return render_template("products.html", products=products)


@main_bp.route("/products/new", methods=["GET", "POST"])
def new_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data, price=form.price.data)
        db.session.add(product)
        db.session.commit()
        flash(f"Added {product}", "success")
        return redirect(url_for("main_bp.products"))
    return render_template("common_form_render.html", form=form)


@main_bp.route("/categories")
def categories():
    categories = Category.query.all()
    return render_template("records.html", keys=["id", "name", "created_at", "modified_at"], records=categories)

@main_bp.route("/category/new",methods=["GET","POST"])
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash(f"Added {category}", "success")
        return redirect(url_for("main_bp.categories"))
    return render_template("common_form_render.html", form=form)