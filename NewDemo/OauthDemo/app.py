# This class is a copy of __init__.py but works with the docker
# __init__ class has import problems but this one is compatible

import os
import pickle

from flask import Flask, render_template, request, redirect, url_for
from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField
from flask_login import login_required, login_user, current_user

#App creation
app = Flask(__name__)
app.secret_key = '!secret'
app.config.from_object('config')

#login_manager = LoginManager()
#login_manager.init_app(app)
#login_manager.login_view = 'login'

#Package for registration page
# import OAUTH.registration
import registration
from banking import *

# #Package for objects
# import OAUTH.objects
from objects import *

import model

#List from old demo that needs to be passed to different modules - Not yet working
registeredAccounts = []

#Check for existing data & load - can use as standin for database - use code from old demo
if os.path.isfile('./OAUTHUsers.txt') and os.stat('OAUTHUsers.txt').st_size != 0:

    loadfile = open('OAUTHUsers.txt', 'rb')
    registeredUsers = pickle.load(loadfile)

    loadfile.close()

else:
    registeredUsers = []



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

#Default page
@app.route('/', methods=["GET","POST"])
def login():
    #Create login form, both fields are mandatory -- user input fields are not centred for some reason
    login = LoginForm(request.form)
    if request.method == "POST":

        #Debug print
        print(login.customerNum.data)
        print(login.password.data)

        #On successful login, will redirect to that user's profile (NOT IMPLEMENTED)
        return redirect('/login')
    return render_template('index.html', form=login)

@app.route('/twitterLogin')
def twitterLogin():
    twitter = oauth.create_client("twitter")
    redirect_uri = url_for('authorize', _external=True)
    return twitter.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    twitter = oauth.create_client("twitter")
    token = twitter.authorize_access_token()
    resp = twitter.get('account/verify_credentials.json')
    profile = resp.json()
    #login_user(current_user)
    #print(profile)
    # can store to db or whatever
    return redirect(url_for('banking', user=str(profile['name'])))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
