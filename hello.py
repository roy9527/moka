from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask import Flask, render_template
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
import sys, os

baseDir = os.path.abspath(os.path.dirname(__file__))

class NameForm(FlaskForm):
    name=StringField('What is your name?', validators=[Required()])
    submit=SubmitField('Submit')

app = Flask(__name__)
app.config['SECRET_KEY']='its your dream.'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(baseDir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    name=None
    form=NameForm()
    if form.validate_on_submit():
        name=form.name.data
        form.name.data=''
    return render_template('index.html', form=form, name=name, current_time=datetime.utcnow())

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


if __name__ =='__main__':
    manager.run()
