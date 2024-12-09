from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from database import db
from models.user import User

auth_blueprint = Blueprint("auth", __name__, template_folder="../views/auth")


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if (
            user and user.password == password
        ):  # Replace with hashed password comparison
            login_user(user)
            return redirect(url_for("chat.index"))
        flash("Invalid credentials", "danger")
    return render_template("login.html")


@auth_blueprint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if User.query.filter_by(username=username).first():
            flash("Username already exists", "danger")
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("auth.login"))
    return render_template("register.html")
