from flask import Blueprint, flash, redirect, render_template, request, g, session

from .db import get_db
from .module import login_required
bp = Blueprint("gallery", __name__)


@bp.route("/")
def index():
    """present all the galleries avaliable in db to all users"""
    return render_template("gallery/index.html")


@bp.route("/profile/<int:user_id>")
@login_required
def profile():
    return "profile"






@bp.before_app_request
def load_logged_in_user():
    
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        user_id = get_db().execute("SELECT * FROM user WHERE id = ?", 
                        (user_id,)
                    ).fetchone()
        

