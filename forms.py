from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, DateTimeField, PasswordField
from wtforms.validators import DataRequired, URL
from model import Host, Speaker

class Register(FlaskForm):
    first_name = StringField(
        'first_name',
        validators=[DataRequired()],
    )
    last_name = StringField(
        'last_name',
        validators=[],
    )
    email = StringField(
        'email',
        validators=[DataRequired()],
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
    )
    user_type = SelectField(
        'user_type',
        validators=[DataRequired()],
        choices=[
            ('Speaker', 'Speaker'),
            ('Host', 'Host'),
        ],
    )

class HostRegister(FlaskForm):
    state = SelectField(
        'state',
        validators=[DataRequired()],
        choices=[
            ('South Dagon', 'South Dagon'),
            ('North Dagon', 'North Dagon'),
        ]
    )
    address = TextAreaField(
        'address',
        validators=[DataRequired()],
    )
    phone = StringField(
        'phone',
        validators=[DataRequired()],
    )
    facebook_url = StringField(
        'facebook_url',
        validators=[URL()]
    )
    description = TextAreaField(
        'description',
        validators=[DataRequired()],
    )

class SpeakerRegister(FlaskForm):
    phone = StringField(
        'phone',
        validators=[DataRequired()],
    )
    facebook_url = StringField(
        'facebook_url',
        validators=[URL()]
    )
    description = TextAreaField(
        'description',
        validators=[DataRequired()],
    )
    

class ConcertForm(FlaskForm):
    host_id = SelectField(
        'host_id',
        validators=[DataRequired()],
        choices=[]
    )
    speaker_id = SelectField(
        'speaker_id',
        validators=[DataRequired()],
        choices=[]
    )
    concert_time = DateTimeField(
        'concert_time',
        validators=[DataRequired()],
        default = datetime.today(),
    )
    youtube_url = StringField(
        'youtube_url',
        validators=[URL()]
    )
    def __init__(self, host_choices: list = None, speaker_choices: list = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if host_choices:
            self.host_id.choices = host_choices
        if speaker_choices:
            self.speaker_id.choices = speaker_choices

class HostForm(FlaskForm):
    name = StringField(
        'name',
        validators=[DataRequired()],
    )
    state = SelectField(
        'state',
        validators=[DataRequired()],
        choices=[
            ('South Dagon', 'South Dagon'),
            ('North Dagon', 'North Dagon'),
        ]
    )
    address = TextAreaField(
        'address',
        validators=[DataRequired()],
    )
    phone = StringField(
        'phone',
        validators=[DataRequired()],
    )
    image_url = StringField(
        'image_url',
        validators=[URL()]
    )
    facebook_url = StringField(
        'facebook_url',
        validators=[URL()]
    )
    availiablity = BooleanField("availiablity")
    motto = StringField(
        'motto'
    )

class SpeakerForm(FlaskForm):
    name = StringField(
        'name',
        validators=[DataRequired()],
    )
    address = StringField(
        'address',
        validators=[DataRequired()],
    )
    phone = StringField(
        'phone',
        validators=[DataRequired()],
    )
    image_url = StringField(
        'image_url',
        validators=[URL()]
    )
    facebook_url = StringField(
        'facebook_url',
        validators=[URL()]
    )
    availiablity = BooleanField("availiablity")
    quote = StringField(
        'quote'
    )
