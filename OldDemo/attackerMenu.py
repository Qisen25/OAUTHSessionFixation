from objects import *
from random import seed
from random import randint

def attackerMenu():

    valid = 0
    options = [1,2,0]

    #Input Validate
    while valid == 0:
        attackerChoice = int(input("\nWhat do you want to do?\n1: View current session ID\n2: Enter a sessioniD\n0: Back\nChoice: "))

        if attackerChoice not in options:
            print("Please enter a valid option!")
        else:
            valid = 1

    return attackerChoice

def enterSessionID(token, sessions):

    match = 0
    newSessionID = int(input("\nEnter a session ID: "))

    #Search session data for provided token ID
    #If match found, set current session token to this existing token
    for item in sessions:
        if item.ID == newSessionID:
            print("Existing session found! Login to continue")
            token = item
            match = 1

    #If no match, set to new value
    if match == 0:
        print("No token found, changing current session ID")
        token.ID = newSessionID

    return token
