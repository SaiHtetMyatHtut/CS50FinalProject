from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
database_path = 'sqlite:///hopezone.db'

def setup_db(app, database_path = database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

class Concert(db.Model):
    __tablename__ = "Concert"
    
    id = db.Column(db.Integer, primary_key=True)
    speaker_id = db.Column(db.Integer, db.ForeignKey(
      'Speaker.id'), nullable=False)
    host_id = db.Column(db.Integer, db.ForeignKey('Host.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    youtube_url = db.Column(db.String(200), nullable=False)

    def insert(self):
      db.session.add(self)
      db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Show {}{}>'.format(self.speaker_id, self.host_id)

class Host(db.Model):
    __tablename__ = "Host"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_id = db.Column(db.Integer, db.ForeignKey('ImageTable.id'), nullable=True)
    facebook_link = db.Column(db.String(120))
    description = db.Column(db.String(300))
    available = db.Column(db.Boolean)
    motto = db.Column(db.String(300))
    concerts = db.relationship('Concert',
      backref=db.backref('Host', lazy=True))
    image_table = db.relationship('ImageTable',
      backref=db.backref('Host', lazy=True))

    def insert(self):
      db.session.add(self)
      db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Host {}>'.format(self.name)

class Speaker(db.Model):
    __tablename__ = "Speaker"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    phone = db.Column(db.String(120))
    image_id = db.Column(db.Integer, db.ForeignKey('ImageTable.id'), nullable=True)
    facebook_link = db.Column(db.String(120))
    description = db.Column(db.String(300))
    available = db.Column(db.Boolean)
    concerts = db.relationship('Concert',
      backref=db.backref('Speaker', lazy=True))
    image_table = db.relationship('ImageTable',
      backref=db.backref('Speaker', lazy=True))
    
    def insert(self):
      db.session.add(self)
      db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Speaker {}>'.format(self.first_name)

class ImageTable(db.Model):
    __tablename__ = "ImageTable"

    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.LargeBinary)
    
    def insert(self):
      db.session.add(self)
      db.session.commit()
      return self.id
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Image {}>'.format(self.id)
