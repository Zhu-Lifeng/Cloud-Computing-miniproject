from flask import Blueprint, render_template,redirect,url_for
import requests
from PIL import Image

BPstart = Blueprint('start', __name__)
def picture():
    image_default = Image.open("MainProject/Asset/maxresdefault.jpg")
    response = requests.get("https://coffee.alexflipnote.dev/random.json")
    if response.status_code == 200:
        data = response.json()
        return data['file']
    else:

        return image_default

@BPstart.route('/')
def index():
    return render_template('start.html', P=picture())