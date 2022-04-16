'''
Routes and views for the flask application.
'''

from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request
from RingAppraisal import app
import joblib
import os
from RingAppraisal.constants import RING_PROPERTIES_DICT

model_path = os.path.join(app.instance_path, '..' , 'RingAppraisal', 'model.pkl')
model = joblib.load(model_path)

@app.route('/', methods = ['POST', 'GET'])
def home():
    '''Renders the home page.'''
    if request.method == 'POST':
        #user = request.form['nm']
        return redirect(url_for('success',name = user))
    else:
        return render_template(
            'index.html',
            ring_properties_dict=RING_PROPERTIES_DICT,
            title='Home Page',
            year=datetime.now().year
    )

@app.route('/contact')
def contact():
    '''Renders the contact page.'''
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    '''Renders the about page.'''
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
