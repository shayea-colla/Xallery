from flask import (
    Blueprints, flash, g, session, request, redirect, render_template, url_for
)
from werkzeug.security import generate_password_hash, check_password_hash
import functools
from db import get_db

bp = Blueprints('auth', __name__, url_prefex='/auth')


@bp.route('/register', methods=("GET", "POST"))
def register():
    
    if request.method == "POST":
        ...
        
    return render_template('auth/register.html')


@bp.route('/login', methods=("GET", "POST"))
def login():
    
    if request.method == "POST":
        pass
    
    return render_template('auth/login.html')






























@bp.before_app_requrest
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        user_id = get_db().execute(
            'SELECT * FROM user WHERE id = ?',
            (user_id,)
        ).fetchone()



def login_required(view):
    @functools.wraps(view)
    def wrapper_login_required(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        
        return view(*args, **kwargs)
    
    return wrapper_login_required
        