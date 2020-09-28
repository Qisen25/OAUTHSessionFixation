# import os
# import pickle

# from flask import Flask, render_template, request, redirect
# from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField

# #App creation
# app = Flask(__name__)

# #Package for registration page
# import registration

# #Package for objects
# import objects

# #Check for existing data & load - can use as standin for database - use code from old demo
# if os.path.isfile('./OAUTHUsers.txt') and os.stat('OAUTHUsers.txt').st_size != 0:

#     loadfile = open('OAUTHUsers.txt', 'rb')
#     registeredUsers = pickle.load(loadfile)

#     loadfile.close()

# else:
#     registeredUsers = []

# #Default page
# @app.route('/')
# def index():
    
#     #Create login form, both fields are mandatory -- user input fields are not centred for some reason
#     login = loginForm(request.form)
#     if request.method == "POST":

#         #Debug print
#         print(login.customerNum.data)
#         print(login.password.data)

#         #On successful login, will redirect to that user's profile (NOT IMPLEMENTED)
#         return redirect('/login')
#     return render_template('index.html', form=login)

# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=5000)
