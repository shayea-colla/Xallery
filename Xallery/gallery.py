from flask import Blueprint, flash, redirect, render_template, request, g, session , url_for
from .db import get_db
from .module import (
    login_required,
    get_designer,
    allowed_extention,
    save_picture,
    check_designer,
)

bp = Blueprint("gallery", __name__)


@bp.route("/")
def index():
    """present all the galleries avaliable in db to all users"""

    designers = get_designer()

    return render_template("gallery/index.html", designers=designers)


@bp.route("/<int:id>", methods=("GET", "POST"))
def profile(id):

    if request.method == "POST":

        if "upload-picture" not in request.files:
            flash("Missing file part")
            return redirect(request.url)

        file = request.files["upload-picture"]

        if file.filename == "":
            flash("Missing file")
            return redirect(request.url)

        if file and allowed_extention(file.filename) and check_designer(id):
            if save_picture(file, id):
                return redirect(request.url)

        ...
    designer = get_designer(id)
    return render_template("gallery/profile.html", designer=designer)


@bp.route("/edit", methods=("GET", "POST"))
def edit():
    if request.method == "POST":
        ...

    return render_template("gallery/edit.html")


@bp.route('/<int:id>/upload', methods=('POST', 'GET'))
def upload_picture(id):
    
    
    if request.method == "GET":
        return redirect(url_for('gallery.profile'))

    error = None
    if check_designer(id):
        if 'upload-picture' not in request.files:
            error = "MISSING FILE APART"
            
        if error is None:
            file = request.file['upload-picture']
            
            if file.filename is "":  
                error = "FILE DOES NOT EXIST; PERHAPS YOU FORGET TO CHOOSE FILE"
            else:
                if save_picture(file, id):
                    return redirect(url_for('gallery.profile'))
             
        flash(error)   
        return redirect('gallery.profile')





@bp.before_app_request
def load_logged_in_user():

    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        )
