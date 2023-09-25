from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField, FloatField, IntegerField
from wtforms.validators import DataRequired, NumberRange

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
    thresh_desc = 'Threshold for classifying workers in \'red band\'. Discrepancy scores > threshold will be classified as red band. Should be a decimal between 0 and 1.'
    threshold = FloatField('Threshold', validators = [DataRequired(), NumberRange(min = 0, max = 1, message = 'Threshold must be a decimal value between 0 and 1')], description = thresh_desc)
    
    # Optional inputs
    acc_desc = 'Distance from threshold at which confidence guarantee applies.'
    accuracy = FloatField('Accuracy', default = 0.02, validators = [NumberRange(min = 0, max = 1, message = 'Accuracy must be a decimal value between 0 and 1')], description = acc_desc)
    
    conf_desc = 'Desired probability of correctly classifying workers as red band.'
    confidence = FloatField('Confidence', default = 0.9, validators = [NumberRange(min = 0, max = 1, message = 'Confidence must be a decimal value between 0 and 1')], description = conf_desc)
    
    tol_desc = 'Distance from desired probability at which binary search of number of samples is stopped.'
    tolerance = FloatField('Tolerance', default = 0.001, validators = [NumberRange(min = 0, max = 1, message = 'Tolerance must be a decimal value between 0 and 1')], description = tol_desc)
    
    n_high_desc = 'Maximum possible number of samples for initializing binary search.'
    n_high = IntegerField('Maximum # samples', default = 10000, validators = [NumberRange(2, 10000000, message = 'Maximum number of samples should be at least 2')], 
                          description = n_high_desc)
    
    n_low_desc = 'Minimum possible number of samples for initializing binary search.'
    n_low = IntegerField('Minimum # samples', default = 2, validators = [NumberRange(1, 1000000, message = 'Minimum number of samples should be at least 1')], 
                         description = n_low_desc)
    
    submit = SubmitField('Generate number of samples')