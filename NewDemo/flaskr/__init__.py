import os
import pickle

from flask import Flask, render_template, request, redirect

#App creation
app = Flask(__name__)

#Package for registration page
import OAUTH.registration

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
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
