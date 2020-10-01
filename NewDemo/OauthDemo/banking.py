import objects
import model

from app import app

from flask import Flask, render_template, request, redirect, session

@app.route('/banking', methods=["GET","POST"])
def banking():
    print("ENTERED BANKING")
    
    if model.validateSession(session): # If user session exists
        user = model.findUser(model.sessions[session['SESSION_ID']].accountNum) # Get the user by customer number

        print(f"DEBUG: Banking - user session ID is {session['SESSION_ID']}")
        print(f"Initiated banking for user '{user.accountNum}'")

        return render_template('banking.html', name=(user.name + ' ' + user.surname), balance=user.account.balance)
    else:
        return redirect('/login')
