# from OAUTH import app
# from OAUTH import objects
# from app import app
from objects import *
import sys

from flask import Flask, render_template, request, redirect, url_for
from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField

from app import app

import model

# Register route
@app.route('/register', methods=["GET","POST"])
def register():
    # Generates registration form. User input fields are not centred for some reason
    form = RegistrationForm(request.form)
    if request.method == "POST":
        # Creates the new user - form data now exists in the user object
        newUser = User(form.fname.data, form.lname.data, form.password.data)
        
        # Add the new user to the list of users
        model.addRegisteredUser(newUser)
        
        model.saveRegisteredUsers(model.REGISTERED_USERS_SAVEFILE)

        # Debug printouts
        print(newUser.name, file=sys.stdout)
        print(newUser.surname, file=sys.stdout)

        # Redirects to register complete page on submit
        return redirect(url_for('register_complete', accountNum=newUser.accountNum))

    return render_template('register.html', form=form)

# Register Complete page - Needs to show customer number for the created user!
@app.route('/register_complete')
def register_complete():
    return render_template('registration_complete.html', accountNum=request.args['accountNum'])
