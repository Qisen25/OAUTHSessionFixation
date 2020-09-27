from objects import *
from random import seed
from random import randint

def login_menu(sessionID, registeredUsers):

    valid = 0

    #Input validate
    while valid == 0:

        options = [1,2,3,0]
        loginChoice = int(input("\nPlease log in or register to continue\n1: Login\n2: Register\n3: Attacker Menu\n0: Exit\nChoice: "))

        if loginChoice not in options:
            print("\nPlease enter a valid choice!")
        else:
            valid = 1

    return loginChoice

def login(sessionID, registeredUsers):

    match = 0

    #Auto login if existing token is authenticated (after changing session ID via attacker menu)
    if sessionID.auth:
        for item in registeredUsers:
            if item.customerNum == sessionID.authCustomerNum:
                currentUser = item
                match = 1

    else:
        #Get credentials
        customerNum = int(input("\nCustomer Identification Number: "))
        password = input("Password: ")

        #Match provided credentials with user objects
        for item in registeredUsers:
            if item.customerNum == customerNum:
                if item.password == password:
                    match = 1
                    sessionID.auth = True
                    sessionID.authCustomerNum = item.customerNum
                    currentUser = item

    #No match, set return value to None
    if match == 0:
        print("\nInvalid CIN or password, please try again")
        currentUser = None

    return currentUser

def register(sessionID, registeredUsers):

    #Name and surname are capitalised for aesthetics
    name = (input("\nFirst Name: ")).capitalize()
    surname = (input("Surname: ")).capitalize()
    password = input("Enter a password: ")

    #Creates user object, append to registeredUsers list
    currentUser = user(name, surname, password)
    registeredUsers.append(currentUser)

    print("\nYour Customer Identification Number is: ", currentUser.customerNum)

    return None
