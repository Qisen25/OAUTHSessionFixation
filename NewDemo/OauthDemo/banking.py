import objects
import model

from app import app

from flask import Flask, render_template, request, redirect, session, flash
from wtforms import Form, validators, IntegerField, SubmitField

from objects import TransactionForm

@app.route('/banking', methods=["GET","POST"])
def banking():
    print("ENTERED BANKING")
    
    if 'ACCOUNT_NUM' in session: # If user session exists
        user = model.findUser(session['ACCOUNT_NUM']) # Get the user by customer number

        transaction = TransactionForm(request.form)
        if request.method == "POST":
            if transaction.deposit.data == True:
                user.deposit(transaction.amount.data)
            elif transaction.withdraw.data == True:
                user.withdraw(transaction.amount.data)

        print(f"DEBUG: Banking - user session is {session['ACCOUNT_NUM']}")
        print(f"Initiated banking for user '{user.accountNum}'")

        return render_template('banking.html', name=(user.name), balance=user.account.balance, form=transaction)
    else:
        return redirect('/login')
