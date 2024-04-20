import threading
from typing import Any
from urllib.parse import urlencode
from ..config import BASE_URL, CLIENT
from flask import Flask, redirect, url_for, render_template, flash, session, \
    current_app, request, abort
import os
import requests
import sys
from uuid import uuid4
import json

class DexcomOAuthServer(threading.Thread):
    app = Flask(__name__)
    path = os.path.join(os.path.abspath("."), "token.txt")
    data = []

    def requestData(self, year: str, month: str or None, asList: bool = False):
        _year, _month = (int(year), int(month)) # Ensure Integers


        max_day_value = "01"

            # Get Max value for a day in given month
        if _month == 1 or _month == 3 or _month == 5 or _month == 7 or _month == 8 or _month == 10 or _month == 12:
            max_day_value = "31"
        elif _month == 4 or _month == 6 or _month == 9 or _month == 11:
            max_day_value = "30"
        elif _year % 4 == 0:
            max_day_value = "28"
        else:
            max_day_value = "28"

        if len(month) != 1 and len(month) != 2: # Neither 1 nor 2 in lengt
            abort(400)

        if len(month) == 1:
            month = "0" + month



        query = {
            "startDate": "{}-{}-01T00:00:00".format(year, month),
            "endDate": "{}-{}-{}T23:59:59".format(year, month, max_day_value)
        }

        headers = {"Authorization": "Bearer {}".format(self.token)}

        response = requests.get(BASE_URL+"/v3/users/self/egvs", headers=headers, params=query)

        if asList:
            tList = []
            for i in reversed(response.json()["records"]):
                # Reverse List (Bottom Timestamp is the Lowest)
                tList.append([i["systemTime"], i["value"], i["trendRate"]])
                self.data.append([i["systemTime"], i["value"], i["trendRate"]])

            print("TList is {} terms long".format(str(len(tList))))
            return tList # Return the tList response as data
        return response
    def __init__(self, secret_key: str or None = None, self_start:bool = True) -> None:
        self.token = None
        if os.path.exists(self.path):
            if len(open(self.path, "r").read()) > 0:
                self.token = open(self.path, "r").read().strip()
        self.secret_key = secret_key if type(secret_key) is str else str(uuid4())
        self.app.config['SECRET_KEY'] = self.secret_key
        self.app.config['OAUTH2_PROVIDERS'] = {
            # Google OAuth 2.0 documentation:
            # https://developers.google.com/identity/protocols/oauth2/web-server#httprest
            'dexcom': {
                'client_id':"ekNKJ3VF0ZIdkZEvLhMmPiAk8UMwLqjJ",
                'client_secret': "SSccVsr7O4wMpyPh",
                'authorize_url': BASE_URL+'/v2/oauth2/login',
                'token_url': BASE_URL+'/v2/oauth2/token',
                'scopes': ['offline_access'],
            },
        }

        # Rest of Varaibles


        @self.app.route('/')
        def index():
            return str({"token": str(self.token)})

        @self.app.route("/token")
        def token_p():
            return str({"token":str(self.token), "token_path":self.path})

        @self.app.route('/authorize/<provider>')
        def oauth2_authorize(provider): # Authorization (Simple Redirect)
            if type(self.token) is str and self.token is not None:
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

        @self.app.route("/data")
        def data_cent(): # Error Message Page
            return str({"error":"Page Not Found", "message": "Data Fetching Format is data/{year}?month=01"})

        @self.app.route("/data/<year>")
        def get_data(year: str):
            """Get the data for the month

            Args:
                month (str or int): URL Param
            """
            if self.token is None:
                return redirect(url_for("oauth2_authorize", provider="dexcom"))

            month = request.args.get("month")

            if month is None :
                return str({"arg": "URL Paramter not defined"})

            response = self.requestData(year, month)
            #for i in data["records"]:
            #    print(i["value"])
            return response.content

        @self.app.route("/erase")
        def erase_token(): # Erase the current token in memory and in SSD
            if os.path.exists(self.path):
                os.remove(self.path)
            self.token = None
            return redirect(url_for("oauth2_authorize", provider="dexcom"))

        @self.app.route('/callback/<provider>')
        def oauth2_callback(provider): # OAuth-Provider Function (Don't Touch)
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
            self.token  = response.json().get('access_token')
            if not oauth2_token:
                print("OAUTH NO TOKEN")
                abort(401)

            with open(self.path, "w") as w:
                w.write(self.token)

            return redirect(url_for('index'))


        # Initalize Thread Object
        threading.Thread.__init__(self, name="dexcom-oauth-server", daemon=True)

        if self_start:
            print("Start the Server")
            self.start() # Starting the Server

    def run(self):
        print("Application Starting!")

        self.app.use_reloader=False
        self.app.run(debug=False, port=5000)
        print("Server Finished")

    def join(self, timeout: float | None = None) -> None:
        # self.app.aborter(401)
        return super().join(timeout)

