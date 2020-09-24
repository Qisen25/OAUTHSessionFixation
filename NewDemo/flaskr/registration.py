import os

from OAUTH import app
from OAUTH import objects

from flask import Flask, render_template, request, redirect
from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField

#Needs to be passed from main, placed here to temporarily stop errors
registeredAccounts = []

#Register route
@app.route('/register', methods=["GET","POST"])
def register():

    #Generates registration form using above class. All fields are mandatory
    form = objects.registrationForm(request.form)
    if request.method == "POST":

        #Creates the new user - form data now exists in the user object
        newUser = objects.user(form.fname.data, form.lname.data, form.password.data, registeredAccounts)
        
        #Debug printouts
        print(newUser.name)
        print(newUser.surname)

        #Redirects to register complete page on submit
        return redirect('/register_complete')

    return render_template('register.html', form=form)
