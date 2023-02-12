from flask import (
    Blueprint,
    flash,
    g,
    session,
    request,
    redirect,
    render_template,
    url_for,
)

from .db import get_db
from .module import User


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User(username, password)

        user.register()

        if user.error is None:
            return redirect(url_for("auth.login"))

        flash(user.error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User(username, password)

        if user.check():
            user.login()

        if user.error is None:
            return redirect(url_for("index"))

        flash(user.error)
    return render_template("auth/login.html")


@bp.route("logout")
def logout():
    if session["user_id"]:
        session.clear()
    return redirect(url_for("index"))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        )
