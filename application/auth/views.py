from . import auth_bp
from .forms import RegisterForm, LoginForm
from flask_login import login_user, login_required
from flask import render_template, flash, redirect, url_for
from .models import User, db


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, name=form.name.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Added user successfully", "success")
        login_user(user)
        return redirect(url_for("auth_bp.users"))
    return render_template("common_form_render.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
    return render_template("common_form_render.html", form=form)


@auth_bp.route("/users", methods=["GET", "POST"])
@login_required
def users():
    users = User.query.all()
    return render_template("records.html", keys=["id", "email", "name", "created_at", "modified_at"], records=users)
