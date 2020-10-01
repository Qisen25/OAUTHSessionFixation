
import pickle
import os
import string
import random
from objects import Session

########################
### Registered Users ###
########################
registeredUsers = []
# TODO REPLACE THE LIST OF USERS WITH A DICTIONARY BECAUSE THAT MAKES WAY MORE SENSE

REGISTERED_USERS_SAVEFILE = 'OAUTHUsers.pickle'

def addRegisteredUser(user):
    """Adds the imported user to the list of users"""
    registeredUsers.append(user)

def loadRegisteredUsers(filepath):
    if os.path.isfile(filepath) and os.stat(filepath).st_size != 0:
        loadfile = open(filepath, 'rb')

        global registeredUsers
        registeredUsers = pickle.load(loadfile)

        loadfile.close()

        print("Here's all the registered user we just loaded")
        [print(user.accountNum) for user in registeredUsers] #TODO get rid of this

def saveRegisteredUsers(filepath):
    saveFile = open(filepath, 'wb')
    pickle.dump(registeredUsers, saveFile)
    saveFile.close()

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


################
### SESSIONS ###
################
# All the adding/removing for sessions must be handled externally to this dictionary

sessions = {} # KEY: Session ID | VALUE: Session Object

# RETRIEVED FROM https://pynative.com/python-generate-random-string/
def get_random_string(length):
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string is:", result_str)
    return result_str

def createSession(user):
    """Create a session object for the imported user. Returns the session ID of the created session. 
        ACTUAL SESSION MANAGEMENT IS NOT THE RESPONSIBILITY OF THIS METHOD."""

    # Generate a random session ID
    randomID = get_random_string(8)
    while randomID in sessions:
        randomID = get_random_string(8)
        print(sessions)

    print(f"Creating new session with ID {randomID} and user account Num {user.accountNum}")

    # Create the new session and add it to the session dict
    newSession = Session(randomID, user.accountNum)
    sessions[randomID] = newSession

    return newSession

# things = {} TODO remove this junk

# def createSessionTEST():
#     """Create a session object for the imported user. Returns the session ID of the created session. 
#         ACTUAL SESSION MANAGEMENT IS NOT THE RESPONSIBILITY OF THIS METHOD."""

#     # Generate a random session ID
#     randomID = get_random_string(8)
#     while randomID in sessions:
#         randomID = get_random_string(8)
    
#     things[randomID] = "YEET"


def validateSession(session):
    print("In validate session - here's all the sessions:")
    print(sessions)
    for s in sessions:
        sessionObj = sessions[s]
        print(f"{sessionObj.ID}: {sessionObj.accountNum}")
    
    """Checks whether the imported session has a session object and whether that session object is still validated (i.e. in the dict of session objects)"""
    if "SESSION_ID" in session:
        if session["SESSION_ID"] in sessions:
            return True
    
    return False

def invalidateSession(sessionID):
    """Invalidates the session object with the imported session ID. Does NOT remove the actual session."""
    sessions.pop(sessionID)