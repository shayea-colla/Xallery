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
from werkzeug.security import generate_password_hash, check_password_hash
import functools
from .db import get_db
from .module import User


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email    = request.form['email']
        

        user = User(username, password, email)

        user.register()

        if user.error is None:
            return redirect(url_for("auth.login"))

        flash(user.error)
    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        
        user = User(username, password)
        return render_template('tmp.html', tmp=user)
        if user.check():
            print(user.check())
            user.login()
            
        if user.error is not None:
            return redirect(url_for('index'))
        
        flash(user.error)
    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        user_id = (
            get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        )


def login_required(view):
    @functools.wraps(view)
    def wrapper_login_required(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(*args, **kwargs)

    return wrapper_login_required
