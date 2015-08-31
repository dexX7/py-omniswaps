from flask.ext.wtf import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

class PrepareFunding(Form):
    amount = StringField('amount', validators=[DataRequired()])
    identifier = IntegerField('identifier', validators=[DataRequired()])
    source = StringField('source', validators=[DataRequired()])
