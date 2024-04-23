import threading
from typing import Any
from urllib.parse import urlencode
from ..config import DEXCOM_BASE_URL, CLIENT
from flask import Flask, redirect, url_for, render_template, flash, session, \
    current_app, request, abort
import os
import requests
import sys
from uuid import uuid4
import json
from ..util.debug import debug
from ..util.csv import arrayToCsv
class DexcomOAuthServer(threading.Thread):
    app = Flask(__name__)
    data = []
    unsorted_data = []

    def __init__(self, secret_key: str or None = None, self_start:bool = True) -> None:
        self.token = None
        self.refresh_token = None
        self.path = os.path.join(os.path.abspath("."), "dexcom-token.json")


        if os.path.exists(self.path):
            _json = json.loads(open(self.path, "rt").read())

            self.token = _json["token"]
            self.refresh_token = _json["refresh_token"]

        self.secret_key = secret_key if type(secret_key) is str else str(uuid4())
        self.app.config['SECRET_KEY'] = self.secret_key
        self.app.config['OAUTH2_PROVIDERS'] = {
            # Google OAuth 2.0 documentation:
            # https://developers.google.com/identity/protocols/oauth2/web-server#httprest
            'dexcom': {
                'client_id':"ekNKJ3VF0ZIdkZEvLhMmPiAk8UMwLqjJ",
                'client_secret': "SSccVsr7O4wMpyPh",
                'authorize_url': DEXCOM_BASE_URL+'/v2/oauth2/login',
                'token_url': DEXCOM_BASE_URL+'/v2/oauth2/token',
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
            debug(provider_data['authorize_url'] + '?' + qs)
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
                debug("Dexcom OAuth State doesn't match, moving on", type="ok")
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
                abort(401)

            oauth2_token = response.json().get('access_token')
            self.token  = response.json().get('access_token')
            self.refresh_token  = response.json().get('refresh_token')

            self.writeTokens() # Change JSON File

            if not oauth2_token:
                debug("Fatal Error in Token: Something must have gone wrong")
                abort(401)

            self.writeTokens()

            return redirect(url_for('index'))


        # Initalize Thread Object
        threading.Thread.__init__(self, name="dexcom-oauth-server", daemon=True)

        if self_start:
            debug("Dexcon OAuth Sever Completed", type="info")
            self.start() # Starting the Server
    def writeTokens(self):
        """Writes the otken to JSON
        ```python
        # File Location is at
        self.path
        ```
        """
        with open(self.path, "w") as w:
                w.write(str({
                    "token": str(self.token),
                    "refresh_token": str(self.refresh_token)
                }).replace("'", '"'))
    def loadToken(self):
        if os.path.exists(self.path):
            _json = json.loads(open(self.path, "rt").read())

            self.token = _json["token"]
            self.refresh_token = _json["refresh_token"]
    def refreshToken(self): # TODO Confirm works
        if self.refresh_token is None:
            debug("Refresh Token is Missing! Can't refresh", type="critical")
            raise Warning("Refresh Token Missing")


        payload = {
            "grant_type": "refresh_token",
            "code": self.refresh_token,
            "redirect_uri": "http://localhost:5000/callback/dexcom",
            "client_id": CLIENT["dexcom-id"],
            "client_secret": CLIENT["dexcom-secret"]
        }


        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = requests.post(DEXCOM_BASE_URL+"/v2/oauth2/token", data=payload, headers=headers)
        print("Refresh Response" + str(response.content))
        debug("Token request sent with authorization request", type="info")
        # The callback will be called and will write the refresh token


    def requestDayData(self, year: str="2022", month: str="01", day:str="01", asList: bool = False, asCsv:bool = False):

        self.waitForToken()

        if self.token is None:
            raise Exception("Token in Undefined")
        _year, _month, _day = (int(year), int(month), int(day)) # Ensure Integers


        max_day_value = 1

            # Get Max value for a day in given month
        if _month == 1 or _month == 3 or _month == 5 or _month == 7 or _month == 8 or _month == 10 or _month == 12:
            max_day_value = 31
        elif _month == 4 or _month == 6 or _month == 9 or _month == 11:
            max_day_value = 30
        elif _year % 4 == 0:
            max_day_value = 28
        else:
            max_day_value = 28

        if len(month) != 1 and len(month) != 2: # Neither 1 nor 2 in lengt
            abort(400)
        # Next Day
        next_day = str(_day+1)

        # Max Sure format 01
        if len(month) == 1:
            month = "0" + month
        if len(day) == 1:
            day = "0" + day
        if len(next_day) == 1:
            next_day = "0" + next_day

        if _day > max_day_value or _day + 1 > max_day_value:
            raise Exception("Day is to large, request {}/{}/{}, max is {}/{}/{}".format(month, day, year, month, max_day_value, year))

        query = {
            "startDate": "{}-{}-{}T00:00:00".format(year, month, day),
            "endDate": "{}-{}-{}T23:59:59".format(year, month, next_day)
        }
        headers = {"Authorization": "Bearer {}".format(self.token)}

        response = requests.get(DEXCOM_BASE_URL+"/v3/users/self/egvs", headers=headers, params=query)

        if len(response.content) == 0: # Invalid Token
            if self.refresh_token is not None:
                debug("Attemping to Regenerate tokens with refresh tokens", type="warn")
                self.refreshToken()
                # Rerun the web-reqjest
                return self.requestDayData(year=year, month=month, day=day, asList = asList, asCsv = asCsv)
            else:
                debug("Invalid Refresh Token, waiting for user to regenerate credentials", type="warm")
                #if os.path.exists(self.path): os.remove(self.path) # Reset
                self.token = None
                self.waitForToken() # Waiting for webserver to activate the token
                #raise Exception("Token Invalid, try /erase and restarting it") # Make Custom Exception



        if asList or asCsv:
            # Get it returned as a list
            tList = []
            for i in reversed(response.json()["records"]):
                # Reverse List (Bottom Timestamp is the Lowest)
                tList.append([i["systemTime"], i["value"], i["trendRate"]])
                self.unsorted_data.append([i["systemTime"], i["value"], i["trendRate"]]) # TODO The whole dataset (not sorted by month)

            self.data.append(tList) # TODO If tList is the whole months day
            if asCsv:
                arrayToCsv(year, month, day, self.token, tList)

            return tList # Return the tList response as data
        return response
    def requestData(self, year: str="2022", month: str = "01", asList: bool = False, asCsv: bool = False):

        self.waitForToken()

        if self.token is None:
            raise Exception("Token in Undefined")
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

        response = requests.get(DEXCOM_BASE_URL+"/v3/users/self/egvs", headers=headers, params=query)

        if len(response.content) == 0 or response.content == b'':
            raise Exception("Token Invalid, try /erase and restarting it") # Make Custom Exception

        if len(response.content) == 0: # Invalid Token
            if self.refresh_token is not None:
                debug("Attemping to Regenerate tokens with refresh tokens", type="warn")
                self.refreshToken()
                # Rerun the web-reqjest
                return self.requestData(year=year, month=month, asList = asList, asCsv = asCsv)
            else:
                debug("Invalid Refresh Token, waiting for user to regenerate credentials", type="warm")
                #if os.path.exists(self.path): os.remove(self.path) # Reset
                self.token = None
                self.waitForToken() # Waiting for webserver to activate the token
                #raise Exception("Token Invalid, try /erase and restarting it") # Make Custom Exception




        if asList or asCsv:
            tList = []
            for i in reversed(response.json()["records"]):
                # Reverse List (Bottom Timestamp is the Lowest)
                tList.append([i["systemTime"], i["value"], i["trendRate"]])
                self.unsorted_data.append([i["systemTime"], i["value"], i["trendRate"]]) # TODO The whole dataset (not sorted by month)

            self.data.append(tList) # TODO If tList is the whole months day
            if asCsv:
                arrayToCsv(year, month, "01-{}".format(max_day_value), self.token, tList)

            return tList # Return the tList response as data
        return response


    def waitForToken(self,):
        if self.token is None: debug("Dexcom OAuth-Token Not Found. Either include a ./dexcom-token.json file or generate new credientals at http://localhost:5000/authorize/dexcom", type="warn")
        while self.token is None:
            pass
        debug("Dexcom OAuth-Token Found", type="sucess")
        if self.token is None: # If its None
            self.loadToken()
            self.writeTokens()

        debug("Current Token is {}".format(str(self.token)), type="info")
        return self.token

    def run(self):
        debug("Application Starting!", type="info")

        self.app.use_reloader=False
        self.app.run(debug=False, port=5000)


    def join(self, timeout: float | None = None) -> None:
        # self.app.aborter(401)
        debug("Dexcom OAuth Server Finished", type="info")
        return super().join(timeout)

