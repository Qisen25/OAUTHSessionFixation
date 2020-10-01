#Taken from old demo. Need to put other objects here once they're importing correctly
from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField, SubmitField
from flask import flash
from random import seed
from random import randint

class User():
    def __init__(self, name, surname, password):
        self.name = name
        self.surname = surname
        self.password = password
        self.accountNum = randint(1, 9999) # For convenience
        self.account = Account(self.accountNum)

    def deposit(self, deposit):
        # valid = 0
        # while valid == 0:
        #     deposit = int(input("How much would you like to deposit? "))

        #     if deposit < 0:
        #         print("Please enter a valid number!")
        #     else:
        #         self.account.balance = self.account.balance + deposit
        #         print("Deposit complete!\n")
        #         valid = 1

        if (deposit > 0):
            self.account.balance += deposit
            model.saveRegisteredUsers(model.REGISTERED_USERS_SAVEFILE)
        # else:
            #TODO flash/error

    def withdraw(self, withdrawal):
        if (withdrawal > 0):
            if (self.account.balance - withdrawal >= 0):
                self.account.balance -= withdrawal
                model.saveRegisteredUsers(model.REGISTERED_USERS_SAVEFILE)
            # else:
                #TODO flash/error
        # else:
            #TODO flash/error


    #FIXME never used
    def payment(self, registeredAccounts): 
        accountExists = 0
        payeeAccount = int(input("Please enter a payee account number: "))

        for account in registeredAccounts:
            if account.accountNum == payeeAccount:
                payee = account
                accountExists = 1

        if accountExists == 1:
            valid = 0

            while valid == 0:
                payment = int(input("How much would you like to pay? "))

                if payment < 0:
                    print("Please enter a valid amount!\n")
                else:
                    self.account.balance = self.account.balance - payment
                    payee.balance = payee.balance + payment
                    print("Payment complete!\n")
                    valid = 1
        else:
            print("Account not found!\n")

        return None

    def checkBalance(self):
        print("\nAccount Number:",self.account.accountNum)
        print("Account Balance: $",self.account.balance)

        return None

class Account():
    def __init__(self, accountNum):
        self.accountNum = accountNum #randint(10000,20000) # FIXME replaced account number with account number, hope this is ok
        # self.accountNum = accountNum
        self.balance = 1000000

class Session():
    def __init__(self, ID, accountNum):
        self.ID = ID
        self.accountNum = accountNum


#############
### FORMS ###
#############
class RegistrationForm(Form):
    fname = StringField('First name: ', [validators.DataRequired()])
    lname = StringField('Last name: ', [validators.DataRequired()])
    password = PasswordField('Password:', [validators.DataRequired()])

class LoginForm(Form):
    accountNum = IntegerField('Account Number: ', [validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired()])

class TransactionForm(Form):
    amount = IntegerField('Transaction Amount ($): ', [validators.DataRequired()])
    deposit = SubmitField(label='Deposit')
    withdraw = SubmitField(label='Withdraw')