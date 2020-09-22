import numpy as np
import pickle
import os
from random import seed
from random import randint

from loginMenu import *
from authMenu import *
from attackerMenu import *
from objects import *

#Generates random number seed
seed()

#Contains account info
registeredAccounts = []

#Contains session info - simulates a cookie
sessions = []

#Check for existing data & load
if os.path.isfile('./OAUTHUsers.txt') and os.stat('OAUTHUsers.txt').st_size != 0:

    loadfile = open('OAUTHUsers.txt', 'rb')
    registeredUsers = pickle.load(loadfile)

    for item in registeredUsers:
        registeredAccounts.append(item.account)

    loadfile.close()

else:
    registeredUsers = []

exit = 0
while exit == 0:

    input("\nPress any key to start banking!\n")

    #Generate blank token with random ID
    token = sessionID(randint(100000,200000))

    #Create session
    sessions.append(token)

    print("##########\nWelcome to Steve From IT Banking!\n##########")

    #Login, register, attacker menu, exit
    loginChoice = login_menu(token, registeredUsers, registeredAccounts)

    end = 0
    while end == 0:

        #Login
        if loginChoice == 1:

            #Get user input for customer number & password, compare with user objects in registeredUsers.
            #Return user if match, return none if no match
            currentUser = login(token, registeredUsers)

            if currentUser != None:

                print("\nWelcome,", currentUser.name,"\nHow can we help you today?")

                #Debug
                #print("\nYour current session ID is: ",token.ID)

                #Uncomment to fix OAUTH vulnerability
                #Randomises the token ID after login (the attacker can only record the ID before login)
                #token.ID = randint(100000,200000)

                #More debug
                #print("\nYour new session ID is: ",token.ID)

                menuOption = None

                while menuOption != 4:
                    menuOption = auth_menu(currentUser, registeredUsers, registeredAccounts)

                    #Balance check
                    if menuOption == 1:
                        currentUser.checkBalance()

                    #Deposit
                    elif menuOption == 2:
                        currentUser.deposit()

                    #Payment
                    elif menuOption == 3:
                        currentUser.payment(registeredAccounts)

                #Log out
                print("Thank you for supporting Steve From IT bank!\n")

                #Failsafe that removes all session data
                #Uncomment when patching vulnerability.
                #for item in sessions:
                    #sessions.remove(item)

                #Reset token for next user login
                token = None
                end = 1

            else:
                loginChoice = login_menu(token, registeredUsers, registeredAccounts)

        elif loginChoice == 2:

            #Register new user, returns customer number
            register(token, registeredUsers, registeredAccounts)
            print("\nThank you for registering with us!")

            loginChoice = login_menu(token, registeredUsers, registeredAccounts)

        elif loginChoice == 3:

            attackerChoice = None

            while attackerChoice != 0:
                attackerChoice = attackerMenu()

                #Print out the current token ID (can only be done before login)
                if attackerChoice == 1:
                    print("\nCurrent Session ID is: ",token.ID)

                #Enter a session ID to simulate stealing a victim session
                elif attackerChoice == 2:
                    token = enterSessionID(token, sessions)
                    attackerChoice = 0

            loginChoice = login_menu(token, registeredUsers, registeredAccounts)

        elif loginChoice == 0:
            end = 1
            exit = 1

savefile = open('OAUTHUsers.txt','wb')
pickle.dump(registeredUsers, savefile)
savefile.close()
