import objects
import model

from app import app

from flask import Flask, render_template, request, redirect, session

@app.route('/banking', methods=["GET","POST"])
def banking():
    print("ENTERED BANKING")
    
    if 'ACCOUNT_NUM' in session: # If user session exists
        user = model.findUser(session['ACCOUNT_NUM']) # Get the user by customer number

        print(f"DEBUG: Banking - user session is {session['ACCOUNT_NUM']}")
        print(f"Initiated banking for user '{user.accountNum}'")

        return render_template('banking.html', name=(user.name), balance=user.account.balance)
    else:
        return redirect('/login')
