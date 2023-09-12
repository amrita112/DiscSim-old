from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')
    
class SampleSizeForm(FlaskForm): 
    threshold = DecimalField('Threshold', validators = [DataRequired()])
    accuracy = DecimalField('Accuracy')
    confidence = DecimalField('Confidence')
    submit = SubmitField('Generate number of samples')