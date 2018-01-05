# -*- coding: UTF-8 -*-
#
# Client python flask oauth2 pour apereo cas.
#
# 

## Configuration
#
CAS_SERVER = '172.17.0.1:8443/cas/'
CAS_KEY = 'clientoauth'
CAS_SECRET = 'passwd'
#
## 

from flask import Flask, redirect, url_for, session, request, jsonify
from flask_oauthlib.client import OAuth
import ssl

# Désactiver la verficiation du certificat
ssl._create_default_https_context = ssl._create_unverified_context


# Création de l'application falsh
app = Flask(__name__)
app.debug = True
app.secret_key = 'UEsrtqaJWiei84'
oauth = OAuth(app)

cas_apca = oauth.remote_app(
    'cas_apca',
    consumer_key=CAS_KEY,
    consumer_secret=CAS_SECRET,
#    request_token_params={'scope': 'user'},
    base_url='https://'+CAS_SERVER,
    request_token_url=None, 
    access_token_method='POST',
    access_token_url='https://'+CAS_SERVER+'/oauth2.0/accessToken',
    authorize_url='https://'+CAS_SERVER+'/oauth2.0/authorize'
)


# Si l'utilisateur n'est pas connu ou que le token à expiré redirigé vers la
# page deconnexion du cas
@app.route('/')
def index():
    if 'cas_apca_token' in session:
        me = cas_apca.get('oauth2.0/profile')
        if me.data.get(u'error') != [u'expired_accessToken']:
            return jsonify(me.data)
    return redirect(url_for('login'))

# Demande explicite de connexion
@app.route('/login')
def login():
    return cas_apca.authorize(callback=url_for('authorized', _external=True))


# Déconnexion
@app.route('/logout')
def logout():
    session.pop('cas_apca_token', None)
    return redirect(url_for('index'))


# Après la connexion si la connexion est valide afficher les informations
# (attributs) de l'utilisateur
@app.route('/login/authorized')
def authorized():
    resp = cas_apca.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason=%s error=%s resp=%s' % (
            request.args['error'],
            request.args['error_description'],
            resp
        )
    session['cas_apca_token'] = (resp['access_token'], '')
    me = cas_apca.get('oauth2.0/profile')
    return jsonify(me.data)


@cas_apca.tokengetter
def get_cas_apca_oauth_token():
    return session.get('cas_apca_token')


if __name__ == '__main__':
    app.run()
