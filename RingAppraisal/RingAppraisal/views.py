'''
Routes and views for the flask application.
'''

from datetime import datetime
from flask import Flask, render_template, url_for, request, jsonify
from RingAppraisal import app
import joblib
import os
from pandas import DataFrame
from RingAppraisal.static.data.constants import RING_PROPERTIES_DICT, INPUT_COLUMNS_LIST
from RingAppraisal.process_data import ProcessFormData


model_path = os.path.join(app.instance_path, '..', 'RingAppraisal', 'static', 'data', 'model.pkl')
model = joblib.load(model_path)

process_object = ProcessFormData(RING_PROPERTIES_DICT)

@app.route('/', methods = ['GET'])
def home():
    '''Renders the home page.'''
    return render_template(
        'index.html',
        ring_properties_dict=RING_PROPERTIES_DICT,
        title='Ring Appraisal',
        year=datetime.now().year
    )

@app.route('/data', methods = ['POST'])
def appraisal():
    d = process_object.process_form_data(request.form)

    input_row = [[d[col] for col in INPUT_COLUMNS_LIST]]
    df_row = DataFrame(input_row, columns=INPUT_COLUMNS_LIST)

    price = model.predict(df_row)[0]

    if price:
        r = .0684 # Compounding rate as calculated in "Jewelry Appraisal Project.ipynb"
            
        start_date = datetime.strptime('042020', "%m%Y").date() # Start date from time of data scraping
        today_date = datetime.now().date()
        num_of_months = (today_date.year - start_date.year) * 12 + today_date.month - start_date.month
        t = num_of_months / 12

        current_price = price * (1 + r/12)**(12 * t) # Compound interest formula
        rounded_current_price = f'{current_price:,.2f}'
        return jsonify({"price":rounded_current_price})
    else:
        return jsonify(({"price":price}))

@app.route('/contact')
def contact():
    '''Renders the contact page.'''
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year
    )

@app.route('/about')
def about():
    '''Renders the about page.'''
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year
    )
