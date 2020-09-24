import os
import pickle

from flask import Flask, render_template, request, redirect
from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField

#App creation
app = Flask(__name__)

#Package for registration page
import OAUTH.registration

#Package for objects -- Not yet working correctly
import OAUTH.objects

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
    
    #Create login form using above class. Both fields are mandatory
    login = loginForm(request.form)
    if request.method == "POST":

        #Debug print
        print(login.customerNum.data)
        print(login.password.data)

        #On successful login, will redirect to that user's profile (NOT IMPLEMENTED)
        return redirect('/login')
    return render_template('index.html', form=login)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
