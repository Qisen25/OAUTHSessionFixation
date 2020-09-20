from objects import *
from random import seed
from random import randint

def auth_menu(currentUser, registeredUsers, registeredAccounts):

    valid = 0

    #Input validate
    while valid == 0:

        options = [1,2,3,4]
        menuOption = int(input("\n1: Check balance\n2: Make deposit\n3: Make payment\n4: Log out\nChoice: "))

        if menuOption not in options:
            print("Please enter a valid choice!")
        else:
            valid = 1

    return menuOption
