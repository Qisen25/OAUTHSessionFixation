import objects
import model

from app import app

from flask import Flask, render_template, request, redirect
from flask_login import login_required

@app.route('/banking', methods=["GET","POST"])
def banking():
    return render_template('banking.html', username=request.args['user'])
