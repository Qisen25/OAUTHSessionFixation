import objects
import model

from flask import Flask, render_template, request, redirect

@app.route('/banking', methods=["GET","POST"])
def banking():
    return render_template('banking.hmtl')