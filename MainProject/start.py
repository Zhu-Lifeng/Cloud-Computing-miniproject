from flask import Blueprint, render_template

BPstart = Blueprint('start', __name__)


@BPstart.route('/')
def index():
    return render_template('start.html')
