from flask import render_template, flash, redirect, jsonify
from app import app
from .forms import PrepareFunding
from controller import *

@app.route('/test')
def test():
    return jsonify(test_shared())

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/funding', methods=['GET', 'POST'])
def funding():
    form = PrepareFunding()
    if form.validate_on_submit():
        flash('Preparing funding transactions for amount=%s, identifier=%d, source=%s' %
              (form.amount.data, form.identifier.data, form.source.data))
        return redirect('/index')
    return render_template('prepare_funding.html',
                           title='Prepare Funding Transaction',
                           form=form)
