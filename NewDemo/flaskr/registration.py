import os

from OAUTH import app

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

@app.route('/register', methods=["GET","POST"])
def register():

    if request.method == "POST":
        req = request.form

        print(req)

        return redirect(request.url)

    return render_template('register.html')
