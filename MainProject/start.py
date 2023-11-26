from io import BytesIO
from flask import Blueprint, render_template, redirect, url_for, send_file
import requests
from PIL import Image
import os

BPstart = Blueprint('start', __name__)


def picture():
    image_default = Image.open("MainProject/static/maxresdefault.jpg")
    response = requests.get("https://coffee.alexflipnote.dev/random.json")
    if response.status_code == 200:
        data = response.json()
        image_data = requests.get(data.get('file')).content
        image_path = os.path.join('MainProject/static/', 'background.jpg')
        with open(image_path, 'wb') as f:
            f.write(image_data)
        return image_path
    else:
        image_path = os.path.join('MainProject/static/', 'background.jpg')
        image_default.save(image_path, 'background.jpg')
        return image_path


@BPstart.route('/')
def index():
    picture()
    return render_template('start.html')


@BPstart.route('/get_image')
def get_image():
    image_path = picture()
    return send_file(image_path, mimetype='image/jpg')
