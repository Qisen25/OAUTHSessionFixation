########################
### Registered Users ###
########################
registeredUsers = []
# TODO REPLACE THE LIST OF USERS WITH A DICTIONARY BECAUSE THAT MAKES WAY MORE SENSE

def addRegisteredUser(user):
    """Adds the imported user to the list of users"""
    registeredUsers.append(user)

def validateUser(accountNum, password):
    """Checks if the imported customer and password match a user of the website. 
    If so, returns the relevant user object. Returns 'None' otherwise."""
    
    print("DEBUG: Here's all the users")
    [print(user.accountNum) for user in registeredUsers] #TODO get rid of this

    foundUser = None

    for user in registeredUsers:
        if user.accountNum == accountNum and user.password == password:
            foundUser = user
            break

    return foundUser

def findUser(accountNum):
    print(f"DEBUG: Searching for account {accountNum}")
    print("DEBUG: Here's all the users")
    [print(user.accountNum) for user in registeredUsers] #TODO get rid of this

    for user in registeredUsers:
        if user.accountNum == accountNum:
            print("User found!")
            return user
    
    return None