from flask import render_template, flash, redirect, url_for
from webapp import webapp
from webapp.forms import LoginForm, SampleSizeForm
from Scripts import binomial_confidence

@webapp.route('/') # Decorator that registeres the function as a callback when a web browser requests the URL /
@webapp.route('/index') # Decorator that registeres the function as a callback when a web browser requests the URL /index

def index():
    
    user = {'username': 'Amrita'}
    posts = [
        {
            'author': {'username': 'Ganesh'},
            'body': 'We need data!'
        },
        {
            'author': {'username': 'Parul'},
            'body': 'We need it now!'
        },
        {
            'author': {'username': 'Karthik'},
            'body': 'I will come for the retreat'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)
    
@webapp.route('/login', methods=['GET', 'POST']) # Decorator that registeres the function as a callback when a web browser requests the URL /login

def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title = 'Sign in', form = form)

@webapp.route('/sample_size', methods=['GET', 'POST']) # Decorator that registers the function as a callback when a web browser requests the URL /sample_size

def sample_size():
    
    form = SampleSizeForm()
    
    if form.validate_on_submit():
        
        a = form.accuracy.data
        t = form.threshold.data
        c = form.confidence.data

        output = binomial_confidence.get_n_samples_single_threshold(t, accuracy = a, confidence = c)
        return render_template('sample_size.html', title = 'Sample size', form = form, output = output)
    
    return render_template('sample_size.html', title = 'Sample size', form = form)