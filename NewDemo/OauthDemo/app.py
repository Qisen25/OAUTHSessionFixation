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
#   Sessions are stored as custom Session objects which contain a unique identifier and the associated customer. 
#   The session ID is stored in the session as "SESSION_ID".

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
    if not model.validateSession(session): # If customer not already logged in
        login = LoginForm(request.form)

        if request.method == "POST":
            #Debug print
            print(f"Attempted login with account '{login.accountNum}', password '{login.password.data}'", file=sys.stdout)

            # Try to find a user with input username & password
            user = model.validateUser(int(login.accountNum.data), login.password.data)

            print(f"DEBUG: Tried to get user and got {user}", file=sys.stdout)

            # If a user with the given username and password was found
            if (user is not None):
                # Debug print
                print(f"Login for {login.accountNum.data} accepted!", file=sys.stdout)
                print("Creating new session for user")

                # Create a session object for this new session (which is now stored in the dict of session objects)
                newSessionObj = model.createSession(user)

                # print(f"JUST CREATED SESSION {}: {}")
                print(model.sessions)
                # Linking new session object with the user's actual session
                session['SESSION_ID'] = newSessionObj.ID

                print(model.sessions)

                #On successful login, will redirect to that user's profile
                return redirect('/')
            else:
                flash("Invalid username or password")
        return render_template('login.html', form=login)
    else: # If customer already logged in
        return redirect('/')

@app.route('/logout', methods=["GET", "POST"])
def logout():
    """Logs out a user from the application by removing their session and invalidating their session ID."""
    if (model.validateSession(session)):
        print("Logging out a user...")
        # Remove the session object from the list of permitted sessions
        model.invalidateSession(session['SESSION_ID'])
        
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