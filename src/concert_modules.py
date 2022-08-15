from flask import Blueprint, render_template, abort, request, redirect
from forms import ConcertForm
from model import Concert, Host, ImageTable, Speaker, db
import datetime
import babel
from jinja2 import TemplateNotFound

app_concert = Blueprint('app_concert', __name__, template_folder='templates')


@app_concert.route("/concert")
def concert():
    concert_data = db.session.query(Concert).join(Speaker).filter(
        Concert.speaker_id == Speaker.id).join(Host).filter(Concert.host_id == Host.id).all()
    data = []
    for concert in concert_data:
        print(concert.Host.image_id)
        data.append({
            "concert_id": concert.id,
            "host_id": concert.host_id,
            "host_name": concert.Host.name,
            "speaker_id": concert.speaker_id,
            "speaker_name": concert.Speaker.first_name + concert.Speaker.last_name,
            "host_image_url": "http://127.0.0.1:5000/image/"+str(concert.Host.image_id),
            "speaker_image_url": "http://127.0.0.1:5000/image/"+str(concert.Speaker.image_id),
            "start_time": babel.dates.format_datetime(concert.start_time, "MMMM, d, y 'at' h:mma", locale='en')
        })

    return render_template('views/concert.html', concerts=data)


@app_concert.route("/concert/<int:id>")
def concert_detail(id):
    concert = Concert.query.get(id)
    if not concert:
        abort(404)
    return render_template('views/pages/concert_watch.html', concert=concert)


@app_concert.route('/concerts/book')
def book_concerts():
    hosts = Host.query.all()
    speaker = Speaker.query.all()
    hosts_data = []
    speakers_data = []
    for host in hosts:
        hosts_data.append((host.id, host.name))
    for speaker in speaker:
        speakers_data.append((speaker.id, speaker.first_name))
    print(hosts_data, speakers_data)
    concerts = ConcertForm(hosts_data, speakers_data)
    return render_template('views/pages/concert_register.html', form=concerts)


@app_concert.route('/concerts/create', methods=['POST'])
def create_concerts():
    def form_null_check(filed_name):
        if not request.form[filed_name]:
            result = ""
        else:
            result = request.form[filed_name]
        return result

    concert = Concert(
        speaker_id=form_null_check('speaker_id'),
        host_id=form_null_check('host_id'),
        youtube_url=form_null_check('youtube_url'),
        start_time=datetime.datetime.today()
    )
    concert.insert()
    return redirect("/")
