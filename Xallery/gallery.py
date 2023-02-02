from flask import (
    Blueprint, flash, redirect, render_template, request, g, session
)

from .module import Gallery


bp = Blueprint('index', __name__)



bp.route('/')
def index():
    pass




