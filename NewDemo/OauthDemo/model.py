########################
### Registered Users ###
########################
registeredUsers = []
# TODO REPLACE THE LIST OF USERS WITH A DICTIONARY BECAUSE THAT MAKES WAY MORE SENSE

def addRegisteredUser(user):
    """Adds the imported user to the list of users"""
    registeredUsers.add(user)

def validateUser(customerNum, password):
    """Checks if the imported customer and password match a user of the website. 
    If so, returns the relevant user object. Returns 'None' otherwise."""
    
    foundUser = None

    for user in registeredUsers:
        if user.customerNum == customerNum and user.password == password:
            foundUser = user
            break

    return foundUser

def findUser(customerNum):
    for user in registeredUsers:
        if user.customerNum == customerNum:
            return user
    
    return None