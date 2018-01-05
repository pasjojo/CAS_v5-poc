from cas_client import CASClient
from flask import Flask, redirect, request, session, url_for
import logging

logging.basicConfig(level=logging.DEBUG, filename='/tmp/app.log')


app = Flask(__name__)
app.secret_key = '\rr8tIPn7'

app_login_url = 'http://localhost:5000/login'
cas_url = 'https://172.17.0.1:8443'
cas_client = CASClient(cas_url, auth_prefix='/cas', headers={'cn': 'plop', 'firstname':'givenName', 'sn': 'sn'})
#cas_client = CASClient(cas_url, auth_prefix='/cas')

@app.route('/login')
def login():
    ticket = request.args.get('ticket')
    if ticket:
        try:
            cas_response = cas_client.perform_service_validate(
                ticket=ticket,
                service_url=app_login_url,
                )
        except:
            # CAS server is currently broken, try again later.
            return redirect(url_for('root'))
        if cas_response and cas_response.success:
            #session['dir'] = dir(cas_response) #.extra_attributes
            session['attributes'] = cas_response.attributes
            #session['data'] = cas_response.data
            session['user'] = cas_response.user
            session['logged-in'] = True
            return redirect(url_for('root'))
    #del(session['logged-in'])
    cas_login_url = cas_client.get_login_url(service_url=app_login_url)
    return redirect(cas_login_url)

@app.route('/logout')
def logout():
    del(session['logged-in'])
    cas_logout_url = cas_client.get_logout_url(service_url=app_login_url)
    return redirect(cas_logout_url)

@app.route('/')
def root():
    img = '<img src="http://www.chambres-agriculture.fr/fileadmin/user_upload/National/002_inst-site-chambres/Interface/logo_CA_France_RVB.png" alt="Logo APCA" />'
    if session.get('logged-in'):
        s = '\n'.join(['{} : {}'.format(str(k), str(v)) for (k, v) in session.items()])
        return '<h1>Python flask PoC</h1>'+img+'<p><big>Connecté '+session['user']+'</big> <a href="/logout">Logout</a></p><pre>'+s+'</pre>'
    else:
        
        return '<h1>Python flask PoC</h1>'+img+'<p><big>Non connecté</big> <a href="/login">Login</a></p>'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
