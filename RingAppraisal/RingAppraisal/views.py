'''
Routes and views for the flask application.
'''

from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, jsonify
from RingAppraisal import app
import joblib
import os
import pandas as pd
from RingAppraisal.constants import RING_PROPERTIES_DICT, INPUT_COLUMNS_LIST
from RingAppraisal.process_data import ProcessFormData

model_path = os.path.join(app.instance_path, '..' , 'RingAppraisal', 'model.pkl')
model = joblib.load(model_path)

process_object = ProcessFormData(RING_PROPERTIES_DICT)

@app.route('/', methods = ['POST', 'GET'])
def home():
    '''Renders the home page.'''
    if request.method == 'POST':
        d = process_object.process_form_data(request.form)
        # print(d)

        input_row = [[d[col] for col in INPUT_COLUMNS_LIST]]
        df_row = pd.DataFrame(input_row, columns=INPUT_COLUMNS_LIST)

        price = model.predict(df_row)[0]
        # print(price)

        if price:
            r = .0684 # Compounding rate as calculated in "Jewelry Appraisal Project.ipynb"
            
            start_date = datetime.strptime('042020', "%m%Y").date() # Start date from time of data scraping
            today_date = datetime.now().date()
            num_of_months = (today_date.year - start_date.year) * 12 + today_date.month - start_date.month
            t = num_of_months / 12

            current_price = price * (1 + r/12) ** (12 * t) # Compound interest formula
            formatted_current_price = round(current_price, 2)
            return redirect(url_for('test', data=formatted_current_price))
        else:
            return redirect(url_for('test', data=price))
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
