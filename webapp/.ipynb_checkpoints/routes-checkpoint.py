from flask import render_template, flash, redirect, url_for
from webapp import webapp
from webapp.forms import LoginForm

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