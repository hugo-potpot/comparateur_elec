from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class RefForm(FlaskForm):
	ref = StringField('Référence : ', validators=[DataRequired()])
	check = BooleanField('123Elec : ')

class InfoForm(FlaskForm):
	info = StringField('Information : ', validators=[DataRequired()])