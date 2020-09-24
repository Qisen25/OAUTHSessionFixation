import os

from OAUTH import app

from flask import Flask, render_template, request, redirect

#Register route
@app.route('/register', methods=["GET","POST"])
def register():

    if request.method == "POST":
        req = request.form
    
        #Proof of concept for now
        print(req)

        return redirect(request.url)

    return render_template('register.html')
