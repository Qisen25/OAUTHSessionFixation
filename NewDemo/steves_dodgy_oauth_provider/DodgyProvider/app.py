# coding: utf-8
import os 
import json
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from flask import Flask
from flask import session, request, url_for
from flask import render_template, redirect
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
import re


from authlib.integrations.flask_client import OAuth, OAuthError
from authlib.integrations.sqla_oauth1 import OAuth1ClientMixin
from authlib.integrations.sqla_oauth1 import OAuth1TemporaryCredentialMixin
from authlib.integrations.sqla_oauth1 import OAuth1TokenCredentialMixin
from authlib.integrations.sqla_oauth1 import OAuth1TimestampNonceMixin

from authlib.integrations.flask_oauth1 import AuthorizationServer, current_credential
from authlib.integrations.sqla_oauth1 import create_query_client_func
from authlib.oauth1.errors import OAuth1Error

app = Flask(__name__, template_folder='templates')
app.debug = True
app.secret_key = '!secret'
app.config.update({
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///app.db',
})
app.config.update(SESSION_COOKIE_SAMESITE="None")
db = SQLAlchemy(app)

app.config.update({
    'OAUTH1_PROVIDER_ENFORCE_SSL': False,
    'OAUTH1_PROVIDER_KEY_LENGTH': (10, 100),
})

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(40))#, unique=True)

    def get_user_id(self):
        return self.id
    
    def get_username(self):
        return self.username

class Client(db.Model, OAuth1ClientMixin):
    

    id = db.Column(db.Integer, primary_key=True)
    client_key = db.Column(db.String(48))
    client_secret = db.Column(db.String(55), index=True, nullable=False)

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')
    )
    user = db.relationship('User')

    def get_client_id(self):
        return self.id
    
    def get_client_key(self):
        return self.client_key

    def get_client_secret(self):
        return self.client_secret

    def get_default_redirect_uri(self):
        return self.default_redirect_uri

    def get_client_id(self):
        return self.client_id

class TemporaryCredential(db.Model, OAuth1TemporaryCredentialMixin):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')
    )
    user = db.relationship('User')

    def check_verifier(self, verifier):
        return self.oauth_verifier == verifier

    def get_oauth_token(self):
        return self.oauth_token
    
    def get_oauth_token_secret(self):
        return self.oauth_token_secret
    
    def get_user_id(self):
        return self.user_id

class TokenCredential(db.Model, OAuth1TokenCredentialMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')
    )
    user = db.relationship('User')

    def get_oauth_token(self):
        return self.oauth_token

    def get_oauth_token_secret(self):
        return self.oauth_token_secret

    def get_user_id(self):
        return self.user_id



class TimestampNonce(db.Model, OAuth1TimestampNonceMixin):
    id = db.Column(db.Integer, primary_key=True)

query_client = create_query_client_func(db.session, Client)
server = AuthorizationServer(app, query_client=query_client)

from authlib.integrations.sqla_oauth1 import (
    register_nonce_hooks,
    register_temporary_credential_hooks,
    register_token_credential_hooks
)

register_nonce_hooks(server, db.session, TimestampNonce)
register_temporary_credential_hooks(server, db.session, TemporaryCredential)
register_token_credential_hooks(server, db.session, TokenCredential)

# def set_user_id(self, user_id):
#     self.user_id = user_id

def current_user():
    if 'id' in session:
        uid = session['id']
        return User.query.get(uid)
    return None


def currently_authorized():
    if 'isAuth' in session:
        uid = session['isAuth']
        return User.query.get(uid)
    return None

@app.route('/', methods=('GET', 'POST'))
def home():
    session.permanent = True
    if current_user():
        return redirect('http://127.0.0.1:5000/steveLogin')

    if request.method == 'POST':
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
        print("User id : " + str(user.id))
        session['id'] = user.id
        session['isAuth'] = None
        return redirect('http://127.0.0.1:5000/steveLogin')
    user = current_user()
    return render_template('home.html', user=user)

@app.route('/initiate', methods=['POST'])
def initiate_temporary_credential():
    # poop = create_temporary_credential(request)
    cl = Client.query.get(0)
    if cl is None:
        cl = Client(
            id=0, 
            client_key='nUf0hXbeiEn4mOE1HH8fiua7lcpCPET2Nn2hhZKB',
            client_secret='ZKXDSaewa29o26YwidwnoOfwlBqH6tnkNh5nkmBAgOcxJ2kGeU',
            default_redirect_uri = 'http://127.0.0.1:5000/steveAuthorized'
        )
        db.session.add(cl)
        db.session.commit()

    request.client_id= 1
    request.redirect_uri='http://127.0.0.1:5000/steveAuthorized'
    temp = server.create_temporary_credential(request)
    #print("Hey client " + repr(cl.client_key))
    # return temp.get_oauth_token()#server.create_temporary_credentials_response()
    # return server.create_temporary_credentials_response()
    return jsonify(
        oauth_token=temp.get_oauth_token(),# note a new token is generated on each request
        oauth_token_secret=temp.get_oauth_token_secret(),
    )

@app.route('/authorize', methods=['GET', 'POST'])
def authorize():
    user = current_user()
    grant_user = None
    session.permanent = True

    print("My request " + repr(request.url))
    authUrl = request.url
    start = 'oauth_token='
    end = '&oauth_callback'
    daToken = authUrl[authUrl.find(start) + len(start) : authUrl.find(end)]
    print(daToken)
    userID = 0
    if request.method == 'GET':
        foundT = TemporaryCredential.query.filter_by(oauth_token=daToken).first()
        usr = {'resource_owner_key': str(foundT.get_oauth_token()), 'id': foundT.get_user_id()}
        userID = foundT.get_user_id()
        grant_user = User.query.get(foundT.get_user_id())
        #print("before updated id " + str(foundT.get_user_id()))
        if user is None and foundT.get_user_id() is None:
            return redirect('/')
            
        if foundT.get_user_id() is None and currently_authorized() is None:
            usr = {'resource_owner_key': str(foundT.get_oauth_token()), 'id': user.get_user_id() }
            userID = user.get_user_id()
            grant_user = User.query.get(foundT.get_user_id())
            # session['id'] = user.id
        
            try:
                req = server.check_authorization_request()
                return render_template('authorize.html', user=usr)
            except OAuth1Error as error:
                return render_template('error.html', error=error)
    elif request.method == 'POST':
        token = request.form.get('oauth_token')
        foundT = TemporaryCredential.query.filter_by(oauth_token=token).first()
        granted = request.form.get('confirm')
        if granted == "yes":
            print('granted!')
            grant_user = user # user session will be stored
            foundT.user_id = user.id
            db.session.commit()

            session['isAuth'] = user.id
            #print(user.id)
        else:
            grant_user = None

    try:
        #server.create_authorization_verifier(request)
        return server.create_authorization_response(grant_user=grant_user)
    except OAuth1Error as error:
        return render_template('error.html', _external=True, error=error)

@app.route('/user', methods=['GET'])
def getUser():
    #print(repr(request.args))
    temp = TemporaryCredential.query.filter_by(oauth_token=request.args['token']).first()
    return str(User.query.get(temp.get_user_id()).username)

with app.app_context():
    # your code here
    db.create_all()

if __name__ == '__main__':
    app.run(port=8001)
    db.create_all()
    app.run()
