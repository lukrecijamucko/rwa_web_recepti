from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db
from models.user import User
from sqlalchemy.exc import IntegrityError


users_bp = Blueprint("users", __name__)


@users_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        email = request.form["email"].strip()
        password = request.form["password"]

        existing_user = User.query.filter(
            (User.username == username) |
            (User.email == email)
        ).first()

        if existing_user:
            return render_template(
                "register.html",
                error="Korisničko ime ili email već postoje."
            )

        user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )

        db.session.add(user)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

            return render_template(
                "register.html",
                error="Korisničko ime ili email već postoje."
            )

        return redirect(url_for("users.login"))

    return render_template("register.html")


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id

            return redirect(url_for("home.index"))

    return render_template("login.html")


@users_bp.route("/logout")
def logout():
    session.pop("user_id", None)

    return redirect(url_for("home.index"))