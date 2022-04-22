'''
Routes and views for the flask application.
'''

from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, jsonify
from RingAppraisal import app
import joblib
import os
from RingAppraisal.constants import RING_PROPERTIES_DICT
from RingAppraisal.process_data import ProcessFormData
import sys

model_path = os.path.join(app.instance_path, '..' , 'RingAppraisal', 'model.pkl')
model = joblib.load(model_path)

process_object = ProcessFormData(RING_PROPERTIES_DICT)

@app.route('/', methods = ['POST', 'GET'])
def home():
    '''Renders the home page.'''
    if request.method == 'POST':
        d = process_object.process_form_data(request.form)
        print(d)
        #return render_template(
        #    'index.html',
        #    ring_properties_dict=RING_PROPERTIES_DICT,
        #    title='Home Page',
        #    year=datetime.now().year)
        return redirect(url_for('test', data=request.form))
    else:
        return render_template(
            'index.html',
            ring_properties_dict=RING_PROPERTIES_DICT,
            title='Home Page',
            year=datetime.now().year
    )

@app.route('/test/<data>')
def test(data):
    return f"{data}"

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
