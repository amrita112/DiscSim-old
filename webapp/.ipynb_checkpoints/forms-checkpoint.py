from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField, FloatField, IntegerField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')
    
class SampleSizeForm(FlaskForm): 
    
    #threshold = DecimalField('Threshold', validators = [DataRequired()])
    #accuracy = DecimalField('Accuracy')
    #confidence = DecimalField('Confidence')
    
    # Required input
    threshold = FloatField('Threshold', validators = [DataRequired()])
    
    # Optional inputs
    accuracy = FloatField('Accuracy', default = 0.02)
    confidence = FloatField('Confidence', default = 0.9)
    tolerance = FloatField('Tolerance', default = 0.001)
    n_high = IntegerField('Maximum # samples', default = 10000)
    n_low = IntegerField('Minimum # samples', default = 2)
    
    submit = SubmitField('Generate number of samples')