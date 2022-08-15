from flask import Blueprint, render_template, abort, request,redirect
from model import Concert, Host, Speaker, setup_db, db
import babel
from jinja2 import TemplateNotFound

app_host = Blueprint('app_host', __name__, template_folder='templates')

@app_host.route("/host")
def host():
    state_list = db.session.query(Host.state).distinct()
    data = []
    for state in state_list:
        host_in_state = {
            "state" : state.state,
            "hosts" : [],
        }
        for host_data in Host.query.all():
            if host_data.state == state.state:
                host_in_state["hosts"].append(host_data)
        data.append(host_in_state)
    return render_template('views/host.html', data = data)

@app_host.route("/host/<int:id>")
def host_detail(id):

    concert_data = db.session.query(Concert).join(Speaker).filter(Concert.speaker_id == Speaker.id).join(Host).filter(Concert.host_id == Host.id).filter(Host.id == id).all()
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

    host = Host.query.get_or_404(id)
    data = {
        "id": host.id,
        "name": host.name,
        "email": host.email,
        "state": host.state,
        "address": host.address,
        "phone": host.phone,
        "image_id": "http://127.0.0.1:5000/image/"+str(host.image_id),
        "facebook_link": host.facebook_link,
        "available": host.available,
        "motto": host.motto,
    }
    return render_template('views/pages/host_detail.html', host = data, concerts = concerts_data)

@app_host.route("/host/<int:id>", methods=['DELETE'])
def host_delete(id):
    concert_data = db.session.query(Concert).join(Host).filter(Concert.host_id == id).all()
    host = Host.query.get_or_404(id)
    for concert in concert_data:
        concert.delete()  
    host.delete()
    return redirect('/host')

@app_host.route("/hosts/search", methods=['POST'])
def search_hosts():
    search_keywords = request.form['search_keywords']
    state_list = db.session.query(Host.state).distinct().filter(Host.name.ilike(f'%{search_keywords}%')).all()
    search_result = Host.query.filter(Host.name.ilike(f'%{search_keywords}%')).all()
    data = []
    for state in state_list:
        host_in_state = {
            "state" : state.state,
            "hosts" : [],
        }
        for host_data in search_result:
            if host_data.state == state.state:
                host_in_state["hosts"].append(host_data)
        data.append(host_in_state)
    return render_template('views/host.html', data = data)

