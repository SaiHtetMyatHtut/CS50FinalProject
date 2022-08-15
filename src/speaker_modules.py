from crypt import methods
from flask import Blueprint, render_template, abort, request, redirect
from model import Concert, Host, Speaker, setup_db, db
import babel
from jinja2 import TemplateNotFound

app_speaker = Blueprint('app_speaker', __name__, template_folder='templates')

@app_speaker.route("/speaker")
def speaker():
    speaker = Speaker.query.all()
    return render_template('views/speaker.html', data = speaker)

@app_speaker.route("/speaker/<int:id>", methods=['GET'])
def speaker_detail(id):
    concert_data = db.session.query(Concert).join(Speaker).filter(Concert.speaker_id == Speaker.id).join(Host).filter(Concert.host_id == Host.id).filter(Speaker.id == id).all()
    concerts_data = []
    for concert in concert_data:
        concerts_data.append({
          "concert_id" : concert.id,
          "host_id": concert.host_id,
          "host_name": concert.Host.name,
          "speaker_id": concert.speaker_id,
          "speaker_name": concert.Speaker.first_name + concert.Speaker.last_name, 
          "host_image_url": "http://127.0.0.1:5000/image/"+str(concert.Host.image_id),
          "speaker_image_url": "http://127.0.0.1:5000/image/"+str(concert.Speaker.image_id),
          "start_time": babel.dates.format_datetime(concert.start_time, "MMMM, d, y 'at' h:mma", locale='en') 
        })

    speaker = Speaker.query.get_or_404(id)
    data = {
        "id": speaker.id,
        "first_name": speaker.first_name,
        "last_name": speaker.last_name,
        "email": speaker.email,
        "phone": speaker.phone,
        "description": speaker.description,
        "image_id": "http://127.0.0.1:5000/image/"+str(speaker.image_id),
        "facebook_link": speaker.facebook_link,
        "available": speaker.available,
    }
    return render_template('views/pages/speaker_detail.html', speaker = data, concerts = concerts_data)

@app_speaker.route("/speaker/<int:id>", methods=['DELETE'])
def speaker_delete(id):
    concert_data = db.session.query(Concert).join(Speaker).filter(Concert.speaker_id == id).all()
    speaker = Speaker.query.get_or_404(id)
    for concert in concert_data:
        concert.delete()   
    speaker.delete()
    return redirect('/speaker')

@app_speaker.route("/speakers/search", methods=['POST'])
def search_speakers():
    search_keywords = request.form['search_keywords']
    search_result = Speaker.query.filter(Speaker.first_name.ilike(f'%{search_keywords}%')).all()
    return render_template('views/speaker.html', data = search_result)
