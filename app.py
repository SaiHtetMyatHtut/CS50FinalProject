import os
from flask import Flask, redirect, render_template, request, session

# Custom Imports
from model import setup_db
from forms import Register
from src.host_modules import app_host
from src.speaker_modules import app_speaker
from src.concert_modules import app_concert
from src.register_modules import app_register
from src.image_modules import app_image


app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
setup_db(app)
app.register_blueprint(app_host)
app.register_blueprint(app_speaker)
app.register_blueprint(app_concert)
app.register_blueprint(app_register)
app.register_blueprint(app_image)

@app.route("/")
def index():
    register = Register()
    return render_template('views/home.html', form=register)

if __name__ == '__main__':
    app.run(debug=True)