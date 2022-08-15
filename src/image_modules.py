from crypt import methods
import io
from flask import Blueprint, render_template, abort, request, redirect, send_file
from model import Concert, Host, ImageTable, Speaker, setup_db, db
from forms import HostRegister, Register, SpeakerRegister
from base64 import b64encode, b64decode
from jinja2 import TemplateNotFound

app_image = Blueprint('app_image', __name__, template_folder='templates')

@app_image.route("/image/<int:id>", methods=["GET","POST"])
def image(id):
    raw_image = ImageTable.query.get(id)
    image = io.BytesIO(raw_image.image)
    return send_file(image, attachment_filename='logo.jpeg', mimetype='image/jpg')
