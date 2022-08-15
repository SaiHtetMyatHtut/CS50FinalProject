from flask import Blueprint, render_template, abort, session, request, redirect
from model import Concert, Host, ImageTable, Speaker, setup_db, db
from forms import HostRegister, Register, SpeakerRegister
from jinja2 import TemplateNotFound

app_register = Blueprint('app_register', __name__, template_folder='templates')

@app_register.route("/register", methods=['POST'])
def register():
    session['first_name'] = request.form['first_name']
    session['email'] = request.form['email']
    session['password'] = "request.form['password']"
    user_type = session['user_type'] = request.form['user_type']
    if user_type == 'Speaker':
        session['last_name'] = request.form['last_name']
        speaker_register = SpeakerRegister()
        return render_template('views/pages/speaker_register.html', form=speaker_register)
    elif user_type == 'Host':
        host_register = HostRegister()
        return render_template('views/pages/host_register.html', form=host_register)


@app_register.route("/register_confirm", methods=['POST'])
def register_confirm():
    if session['user_type'] == 'Speaker':
        image = request.files['image']
        session['phone'] = request.form['phone']
        session['facebook_url'] = request.form['facebook_url']
        session['description'] = request.form['description']
        new_image = ImageTable()
        new_image.image = image.read()
        new_id = new_image.insert()
        session['image_id'] = new_id
        speaker = Speaker()
        speaker.first_name = session['first_name']
        speaker.last_name = session['last_name']
        speaker.phone = session['phone']
        speaker.image_id = session['image_id']
        speaker.email = session['email']
        speaker.password = session['password']
        speaker.facebook_link = session['facebook_url']
        speaker.description = session['description']
        speaker.available = True
        speaker.insert()
    elif session['user_type'] == 'Host':
        image = request.files['image']
        session['state'] = request.form['state']
        session['address'] = request.form['address']
        session['phone'] = request.form['phone']
        session['facebook_url'] = request.form['facebook_url']
        session['description'] = request.form['description']
        new_image = ImageTable()
        new_image.image = image.read()
        new_id = new_image.insert()
        session['image_id'] = new_id
        host = Host()
        host.name = session['first_name']
        host.email = session['email']
        host.password = session['password']
        host.state = session['state']
        host.address = session['address']
        host.phone = session['phone']
        host.image_id = session['image_id']
        host.facebook_link = session['facebook_url']
        host.description = session['description']
        host.available = False
        host.motto = "I'm a host"
        host.insert()
    return redirect('/')
