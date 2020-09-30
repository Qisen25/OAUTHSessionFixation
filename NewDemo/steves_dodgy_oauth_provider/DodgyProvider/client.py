# This class is a copy of __init__.py but works with the docker
# __init__ class has import problems but this one is compatible

import os
import pickle

from flask import Flask, render_template, request, redirect, url_for, session
from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField
import requests
# from form import LoginForm

#App creation
app = Flask(__name__)
app.secret_key = '!secret'

#AAAAAAAAAAAAAAAAAAAAAJcCIAEAAAAAzkfSQwMowxr39wXFnMqybIYAuqc%3D4W5cl7ClWSgnCwLg8sHrJx3oVKvgrnVdUghM7wZX9Fx6MiK3tL

from authlib.integrations.flask_client import OAuth

# TODO: fill them
CLIENT_KEY = 'nUf0hXbeiEn4mOE1HH8fiua7lcpCPET2Nn2hhZKB'
CLIENT_SECRET = 'ZKXDSaewa29o26YwidwnoOfwlBqH6tnkNh5nkmBAgOcxJ2kGeU'

oauth = OAuth(app)
oauth.register(
    'custom',
    client_id=CLIENT_KEY,
    client_secret=CLIENT_SECRET,
    api_base_url='http://127.0.0.1:5000/',
    request_token_url='http://127.0.0.1:5000/initiate',
    access_token_url='http://127.0.0.1:5000/token',
    authorize_url='http://127.0.0.1:5000/authorize',
    fetch_token=lambda: session.get('token'),  # DON'T DO IT IN PRODUCTION
)

#List from old demo that needs to be passed to different modules - Not yet working
registeredAccounts = []

#Check for existing data & load - can use as standin for database - use code from old demo
if os.path.isfile('./OAUTHUsers.txt') and os.stat('OAUTHUsers.txt').st_size != 0:

    loadfile = open('OAUTHUsers.txt', 'rb')
    registeredUsers = pickle.load(loadfile)

    for item in registeredUsers:
        registeredAccounts.append(item.account)

    loadfile.close()

else:
    registeredUsers = []

@app.route('/', methods=['GET', 'POST'])
def init():
    return redirect('http://127.0.0.1:5000/')

@app.route('/login')
def login():
    twitter = oauth.create_client("custom")
    redirect_uri = url_for('authorize', _external=True)
    poo = twitter.authorize_redirect(redirect_uri)
    # print("hey there")
    print("Hey this is at login " + repr(poo.headers['location']))
    start = 'oauth_token='
    end = '&oauth_callback'
    s = repr(poo.headers['location'])
    token = s[s.find(start) + len(start) : s.find(end)]
    print("My token " + token)
    session['token'] = token
    return poo

@app.route('/authorized', methods=['GET', 'POST'])
def authorize():
    #print(str(session["name"]))
    twitter = oauth.create_client("custom")
    # token = twitter.authorize_access_token(kwargs=session['token'])
    # print(token)
    #resp = twitter.get('account/verify_credentials.json')
    # profile = resp.json()
    # print("hey there" + repr(profile))
    # do something with the token and profile
    session['token'] = request.args['oauth_token']
    print(repr(session['token']))
    params = {'token': session['token']}
    r = requests.get('http://127.0.0.1:5000/user', params=params)
    print(r.text)
    return redirect(url_for('banking', username=r.text))

@app.route('/banking', methods=['GET', 'POST'])
def banking():
    if 'token' in session:
        return render_template('banking.html', username=request.args['username'])
    else:
        return redirect("/")

if __name__ == '__main__':
    app.run(port=8000)
