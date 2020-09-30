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
#   User information is stored in the session by storing the account number under the key "ACCOUNT_NUM".
#       If this key is not present, the user is not logged in.


#########################
## RUNTIME STARTS HERE ##
#########################
#Check for existing data & load - can use as standin for database - use code from old demo
model.loadRegisteredUsers(model.REGISTERED_USERS_SAVEFILE)
print("LOADED ALL REGISTERED USERS - here they are:")
[print(user.accountNum) for user in model.registeredUsers] #TODO get rid of this


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

@app.route('/login', methods=["GET","POST"])
def login():
    #Create login form, both fields are mandatory -- user input fields are not centred for some reason
    # print(repr(login.accountNum))
    if not 'ACCOUNT_NUM' in session: # If customer not already logged in
        login = LoginForm(request.form)

        print(request.method == "POST")
        if request.method == "POST":

            #Debug print
            print(f"Attempted login with account '{login.accountNum}', password '{login.password.data}'", file=sys.stdout)

            user = model.validateUser(int(login.accountNum.data), login.password.data)

            print(f"DEBUG: Tried to get user and got {user}", file=sys.stdout)

            if (user is not None):
                # Debug print
                print(f"Login for {login.accountNum.data} accepted!", file=sys.stdout)

                #Set the session to the current user's customer number
                session['ACCOUNT_NUM'] = user.accountNum

                #On successful login, will redirect to that user's profile
                return redirect('/')
            else:
                flash("Invalid username or password")
        return render_template('login.html', form=login)
    else: # If customer already logged in
        return redirect('/')

@app.route('/logout', methods=["GET", "POST"])
def logout():
    print("Logging out a user...")
    # Invalidate the current session
    session.clear()

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
    
    if not 'ACCOUNT_NUM' in session:
        session['ACCOUNT_NUM'] = profile['id']
        
    #print(profile)
    # can store to db or whatever
    # return redirect(url_for('banking', user=str(profile['name']))) TODO replace with this (sorry Kei i'm lazy)
    return redirect(url_for('banking', name=str(profile['name']).user))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)