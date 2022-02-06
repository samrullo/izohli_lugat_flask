from . import main_bp
from flask import render_template, flash, redirect, url_for
from .forms import RegisterForm
from application.main.models import User, db


@main_bp.route("/")
def home():
    return render_template("index.html")


@main_bp.route("/users")
def users():
    users = User.query.all()
    return render_template("users.html", users=users)


@main_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash(f"Registered {form}", "success")
        return redirect(url_for("main_bp.users"))
    return render_template("common_form_render.html", form=form)
