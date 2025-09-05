from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileRequired, FileAllowed
from config import Config

class ApplicationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    address = TextAreaField('Address')
    academic_details = TextAreaField('Academic Details')
    id_proof = FileField('ID Proof', validators=[
        FileRequired(),
        FileAllowed(Config.ALLOWED_EXTENSIONS, 'PDF or Image files only!')
    ])
    degree_certificate = FileField('Degree Certificate', validators=[
        FileRequired(),
        FileAllowed(Config.ALLOWED_EXTENSIONS, 'PDF or Image files only!')
    ])
    submit = SubmitField('Submit Application')
