import os
import secrets
from urllib.parse import urlencode

from flask import Flask, redirect, url_for, render_template, flash, session, \
    current_app, request, abort

import requests
import sys
from threading import Thread
app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret!'
app.config['OAUTH2_PROVIDERS'] = {
    # Google OAuth 2.0 documentation:
    # https://developers.google.com/identity/protocols/oauth2/web-server#httprest
    'dexcom': {
        'client_id':"ekNKJ3VF0ZIdkZEvLhMmPiAk8UMwLqjJ",
        'client_secret': "SSccVsr7O4wMpyPh",
        'authorize_url': 'https://sandbox-api.dexcom.com/v2/oauth2/login',
        'token_url': 'https://sandbox-api.dexcom.com/v2/oauth2/token',
        'scopes': ['offline_access'],
    },
}



class Token():
   # g4 _token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIwMDc4ZjM5Mi1jMmM4LTQ5NjktYWNiNy0zOWVhOGQ0Yzk4OGMiLCJhdWQiOiJodHRwczovL3NhbmRib3gtYXBpLmRleGNvbS5jb20iLCJzY29wZSI6WyJlZ3YiLCJjYWxpYnJhdGlvbiIsImRldmljZSIsImV2ZW50Iiwic3RhdGlzdGljcyIsIm9mZmxpbmVfYWNjZXNzIl0sImlzcyI6Imh0dHBzOi8vc2FuZGJveC1hcGkuZGV4Y29tLmNvbSIsImV4cCI6MTcxMzQ3ODU4OCwiaWF0IjoxNzEzNDcxMzg4LCJjbGllbnRfaWQiOiJla05LSjNWRjBaSWRrWkV2TGhNbVBpQWs4VU13THFqSiJ9.ybEaB4Go6hZR8V_LNMEtrhk_LHg0g7lH4vrI6QBFb4xxXzGr3vIIMznBvn0ZX1NPOFDdOZT9Vp05JJqmbR2ksDeBRTt5JswXQr_QyXpjn2YHdYTV4Th0PzOrit4248LI3c_w4afOoI89LsRutdieza9cVuBx3O9OAimDmFyJp4I7KY2ThhtNb3W4li-07CHrbXvlaX4_VGmVuZ2KN_RuWL9ZpYYVW9R3tGp8v60qPe-AMZky1HujpwMJaTRgqou8xjKn-ck8inuI5XocxM-TezFSgtqbx2GDAloV2r9Y0wfm-Yqo3etOWKsXC6GUO-FFhODDUN_jyzq3qxc_5nVn6w"
    _token = None
    @property
    def token(self):
        print("Getting Token")
        return self._token
    def set_token(self, token):
        print("Changing Token")
        self._token = token



token = Token()


@app.route('/')
def index():
    return str(token)



@app.route('/authorize/<provider>')
def oauth2_authorize(provider):
    if type(token.token) is str and token.token is not None:
        return redirect(url_for('get_data'))

    provider_data = current_app.config['OAUTH2_PROVIDERS'].get(provider)
    if provider_data is None:
        abort(404)

    # generate a random string for the state parameter
    session['oauth2_state'] = "george"

    # create a query string with all the OAuth2 parameters
    qs = urlencode({
        'client_id': provider_data['client_id'],
        'redirect_uri': "http://localhost:5000/callback/dexcom",
        'response_type': 'code',
        'scope': ' '.join(provider_data['scopes']),
        'state': session['oauth2_state'],
    })
    # url_for('oauth2_callback', provider=provider,
    print(provider_data['authorize_url'] + '?' + qs, file=sys.stderr)
    # redirect the user to the OAuth2 provider authorization URL
    return redirect(provider_data['authorize_url'] + '?' + qs)

@app.route("/data")
def get_data():
    if token.token is None:
        return redirect(url_for("oauth2_authorize", provider="dexcom"))
    url = "https://sandbox-api.dexcom.com/v3/users/self/egvs"

    query = {
      "startDate": "2022-01-18T00:00:00",
      "endDate": "2022-01-19T00:12:00"
    }

    headers = {"Authorization": "Bearer {}".format(token.token)}

    response = requests.get(url, headers=headers, params=query)

    data = response.json()
    for i in data["records"]:
        print(i["value"])
    return response.content
@app.route('/callback/<provider>')
def oauth2_callback(provider):


    provider_data = current_app.config['OAUTH2_PROVIDERS'].get(provider)
    if provider_data is None:
        abort(404)

    # if there was an authentication error, flash the error messages and exit
    if 'error' in request.args:
        for k, v in request.args.items():
            if k.startswith('error'):
                flash(f'{k}: {v}')
        return redirect(url_for('index'))

    # make sure that the state parameter matches the one we created in the
    # authorization request
    if request.args['state'] != session.get('oauth2_state'):
        print("state doesn't match")
        # abort(401)

    # make sure that the authorization code is present
    if 'code' not in request.args:
        abort(401)

    # exchange the authorization code for an access token
    response = requests.post(provider_data['token_url'], data={
        'client_id': provider_data['client_id'],
        'client_secret': provider_data['client_secret'],
        'code': request.args['code'],
        'grant_type': 'authorization_code',
        'redirect_uri': url_for('oauth2_callback', provider=provider,
                                _external=True),
    }, headers={'Accept': 'application/json'})

    if response.status_code != 200:
        print("here")
        abort(401)
    oauth2_token = response.json().get('access_token')
    token.set_token(response.json().get('access_token'))
    if not oauth2_token:
        print("OAUTH NO TOKEN")
        abort(401)

    print(oauth2_token)

    return redirect(url_for('get_data'))


def runApp():
    app.run(debug=True)

runApp()