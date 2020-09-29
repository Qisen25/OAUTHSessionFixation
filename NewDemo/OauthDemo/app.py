# This class is a copy of __init__.py but works with the docker
# __init__ class has import problems but this one is compatible

import os
import pickle
import sys

from flask import Flask, render_template, request, redirect, url_for, session, flash
from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField
# from form import LoginForm

#App creation
app = Flask(__name__)
app.secret_key = '!secret'
app.config.from_object('config')

#Package for registration page
# import OAUTH.registration
import registration
from banking import *

# #Package for objects
# import OAUTH.objects
from objects import *

import model


############################
## INTERNAL DOCUMENTATION ##
############################
# Session Information:
#   User information is stored in the session by storing the customer number under the key "CUSTOMER_NUM".
#       If this key is not present, the user is not logged in.


#########################
## RUNTIME STARTS HERE ##
#########################
#Check for existing data & load - can use as standin for database - use code from old demo
if os.path.isfile('./OAUTHUsers.txt') and os.stat('OAUTHUsers.txt').st_size != 0:

    loadfile = open('OAUTHUsers.txt', 'rb')
    model.registeredUsers = pickle.load(loadfile)

    loadfile.close()


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
def index():
    # For now just redirects to banking page TODO make an actual index page
    return redirect('/banking')

    # if 'username' in session: # If the user has a session
    #     return render_template('index.html')
    # else:
    #     # Redirect to login page
    #     return redirect('/login')

@app.route('/login')
def login():
    #Create login form, both fields are mandatory -- user input fields are not centred for some reason
    login = LoginForm(request.form)
    if not 'CUSTOMER_NUM' in session: # If customer not already logged in
        if request.method == "POST":

            #Debug print
            print(f"Attempted login with customerNum {login.customerNum.data}, password {login.password.data}", file=sys.stdout)

            user = model.validateUser(login.customerNum.data, login.password.data)

            print(f"DEBUG: Tried to get user and got {user}", file=sys.stdout)

            if (user):
                # Debug print
                print(f"Login for {login.customerNum.data} accepted!", file=sys.stdout)

                #Set the session to the current user's customer number
                session['CUSTOMER_NUM'] = user.customerNum

                #On successful login, will redirect to that user's profile
                return redirect('/')
            else:
                flash("Invalid username or password")
        return render_template('login.html', form=login)
    else: # If customer already logged in
        return redirect('/')

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
    
    if not 'CUSTOMER_NUM' in session:
        session['CUSTOMER_NUM'] = profile['id']
    #print(profile)
    # can store to db or whatever
    return redirect(url_for('banking', user=str(profile['name'])))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
