from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired


class RefForm(FlaskForm):
	ref = StringField('Référence : ', validators=[DataRequired()])

class InfoForm(FlaskForm):
	info = StringField('Information : ', validators=[DataRequired()])