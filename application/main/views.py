from . import main_bp
from flask import render_template


@main_bp.route("/")
def home():
    return render_template("index.html")
