# This class is a copy of __init__.py but works with the docker
# __init__ class has import problems but this one is compatible

import os
import pickle

from flask import Flask, render_template, request, redirect, url_for, session
from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField
# from form import LoginForm

#App creation
app = Flask(__name__)
app.secret_key = '!secret'
app.config.from_object('config')

#Package for registration page
# import OAUTH.registration
import oauthcopy.registration

# #Package for objects
# import OAUTH.objects
from oauthcopy.objects import *

#AAAAAAAAAAAAAAAAAAAAAJcCIAEAAAAAzkfSQwMowxr39wXFnMqybIYAuqc%3D4W5cl7ClWSgnCwLg8sHrJx3oVKvgrnVdUghM7wZX9Fx6MiK3tL

from authlib.integrations.flask_client import OAuth
oauth = OAuth(app)
oauth.register(
    name='twitter',
    api_base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
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

#Default page
@app.route('/')
def index():
    
    # Create login form, both fields are mandatory -- user input fields are not centred for some reason
    login = loginForm(request.form)
    if request.method == "POST":

        #Debug print
        print(login.customerNum.data)
        print(login.password.data)

        #On successful login, will redirect to that user's profile (NOT IMPLEMENTED)
        return redirect('/login')
    return render_template('index.html', form=login)

@app.route('/login')
def login():
    twitter = oauth.create_client("twitter")
    redirect_uri = url_for('authorize', _external=True)
    return twitter.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    twitter = oauth.create_client("twitter")
    token = twitter.authorize_access_token()
    resp = twitter.get('account/verify_credentials.json')
    profile = resp.json()
    # do something with the token and profile
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
