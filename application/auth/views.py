from . import auth_bp
from .forms import RegisterForm, LoginForm
from flask_login import login_user, login_required,logout_user,current_user
from flask import render_template, flash, redirect, url_for,request
from .models import User, db
from application import login_manager

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
            flash(f"Logged in {user} successfully","success")
            next=request.args.get("next")
            if next is not None:
                return redirect(next)
            else:
                return redirect(url_for("auth_bp.users"))
    return render_template("common_form_render.html", form=form)

@auth_bp.route("/logout",methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for("main_bp.home"))

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('auth_bp.login', next=request.path))


@auth_bp.route("/users", methods=["GET", "POST"])
@login_required
def users():
    users = User.query.all()
    return render_template("records.html", keys=["id", "email", "name", "created_at", "modified_at"], records=users)
