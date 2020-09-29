import objects
import model

from app import app

from flask import Flask, render_template, request, redirect, session
from flask_login import login_required

@app.route('/banking', methods=["GET","POST"])
def banking():
    if 'CUSTOMER_NUM' in session: # If user session exists
        user = model.findUser(session['CUSTOMER_NUM']) # Get the user by customer number

        return render_template('banking.html', username=request.args['user'])
    else:
        return redirect('/login')
