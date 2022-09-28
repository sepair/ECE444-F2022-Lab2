from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[validators.DataRequired()]) 
    name2 = StringField('What is your UofT email?', validators=[validators.DataRequired(), validators.email()]) 
    submit = SubmitField('Submit')

app = Flask(__name__)
boostrap= Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'this should be hard to guess'

@app.route('/') 
def index():
    return render_template('index.html')

@app.route('/form', methods=['GET', 'POST']) 
def form():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        old_name2 = session.get('name2')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!') 
        if old_name2 and old_name2 != form.name2.data:
            flash('Looks like you just changed your email!')
        session['name'] = form.name.data
        session['name2'] = form.name2.data
        form.name.data = form.name2.data = ''
        return redirect(url_for('form'))
    return render_template('form.html', form = form, name = session.get('name'), name2 = session.get('name2'))

@app.route('/user/<name>') 
def user(name):
    return render_template('user.html', name=name, current_time=datetime.utcnow())

@app.errorhandler(404) 
def page_not_found(e):
    return render_template('404.html'), 404