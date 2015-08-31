from flask import render_template, flash, redirect, jsonify
from app import app
from controller import *

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.route('/pubkey')
@app.route('/pubkey/<pubkeyhash>')
def pubkey(pubkeyhash=None):
    return getpubkey(pubkeyhash)

@app.route('/createshared/<pubkey>')
def destination(pubkey):
    return jsonify(createshared(pubkey))

@app.route('/createunsigned/<txid>-<int:vout>')
def unsigned(txid, vout):
    return jsonify(createunsigned(txid, vout))

@app.route('/createsigned/<txid>-<int:vout>-<scriptPubKey>-<redeemScript>')
def signed(txid, vout, scriptPubKey, redeemScript):
    return jsonify(createsigned(txid, vout, scriptPubKey, redeemScript))

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}  # fake user
    posts = [  # fake array of posts
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html",
                           title='Home',
                           user=user,
                           posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form)
