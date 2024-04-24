import threading
from typing import Any
from urllib.parse import urlencode
from ..config import DEXCOM_BASE_URL, CLIENT
from flask import Flask, redirect, url_for, render_template, flash, session, \
    current_app, request, abort
import os
import requests
from tinydb import TinyDB, Query
from uuid import uuid4
import json
from ..util.debug import debug
from ..util.csv import arrayToCsv
from ..dexcom.worker import DexcomWorker, InvalidToken
class OAUTH_Server(threading.Thread):

    app = Flask(__name__)
    data = []
    unsorted_data = []
    workers: dict[DexcomWorker] = {
        "dexcom": DexcomWorker()
    } # List of All Types of Workers "provider": Object()

    def __init__(self, port: int=5000, secret_key: str or None = None, self_start:bool = True,) -> None:
        self.port = port # Port which this runs off of

        # Refresh Token
        # self._tokens = {}
        #self._refresh_tokens = {}

        # JSON Path
        self.path = os.path.join(os.path.abspath("."), "token.json")

        # Tiny DB:  DB
        self.db = TinyDB(self.path)

        # Self Start (on/off)
        self.self_start = self_start

        # Flask Releated Configuations
        self.secret_key = secret_key if type(secret_key) is str else str(uuid4()) # Set Flask Secret Key
        self.app.config['SECRET_KEY'] = self.secret_key

        # Configurations for Providers
        self.oauth_providers = {
            # Google OAuth 2.0 documentation:
            # https://developers.google.com/identity/protocols/oauth2/web-server#httprest
            "dexcom": {

                'client_id':"ekNKJ3VF0ZIdkZEvLhMmPiAk8UMwLqjJ",
                'client_secret': "SSccVsr7O4wMpyPh",
                'authorize_url': DEXCOM_BASE_URL+'/v2/oauth2/login',
                'token_url': DEXCOM_BASE_URL+'/v2/oauth2/token',
                'data_url': DEXCOM_BASE_URL+'/v3/users/self/egvs',
                'scopes': ['offline_access'],
            },
        }

        # Rest of Varaibles
        @self.app.route('/')
        def index():
            return str({"tokens":[
                {"token": entry["token"], "refresh_token": entry["refresh_token"],  "provider": entry["provider"]} for entry in self.db.all()
            ]})

        @self.app.route("/token")
        def token_p():
          return str({"tokens":[
                {"token": entry["token"], "refresh_token": entry["refresh_token"],  "provider": entry["provider"]} for entry in self.db.all()
            ], "token_path":self.path})

        @self.app.route('/authorize/<provider>')
        def oauth2_authorize(provider): # Authorization (Simple Redirect)
            if self.checkToken(provider):
                # return redirect(url_for('get_data'))
                pass

            provider_data = self. get(provider)
            if provider_data is None:
                abort(404)

            # random state (close to provider to)
            session['oauth2_state'] = "george"

            # create a query with the parameters
            qs = urlencode({
                'client_id': provider_data['client_id'],
                'redirect_uri': "http://localhost:5000/callback/{}".format(provider),
                'response_type': 'code',
                'scope': ' '.join(provider_data['scopes']),
                'state': session['oauth2_state'],
            })


            debug("Autorization URL: \n"+ provider_data['authorize_url'] + '?' + qs)
            # redirect the user to the OAuth2 provider authorization URL
            return redirect(provider_data['authorize_url'] + '?' + qs)

        @self.app.route("/data")
        def data():
            # Standard Loading Page: Request Data Through WebAPI
            return str({"error":"Page Not Found", "message": "Data Fetching Format is data/{year}?month=01"})

        @self.app.route("/data/<provider>/<year>")
        def get_months_data(provider:str, year: str):
            """Get the data for the month

            Args:
                month (str or int): URL Param
            """

            # Provider Data
            #provider_data = current_app.config['OAUTH2_PROVIDERS'].get(provider)

            if not self.checkToken(provider):
                return str({"message": "Token is not valid", "action":str("http://localhost:5000/" +  url_for("oauth2_authorize", provider=provider))})
            elif not provider in self.workers.keys():
                return str({"message": "Provider is not valid", "action":""})

            month = request.args.get("month")

            if month is None :
                return str({"arg": "URL Paramter not defined"})

            response = self.requestData(provider, "month", year, month)

            return response # Will be JSON

        @self.app.route("/erase/<provider>")
        def erase_token(provider): # Erase the current token in memory and in DRIVE
            self.removeToken(provider)
            return redirect(url_for("oauth2_authorize", provider=provider))

        @self.app.route('/callback/<provider>') # Call back function (only works for DEXCOM)
        def oauth2_callback(provider: str): # OAuth-Provider Function (Don't Touch)
            provider_data = self.oauth_providers.get(provider)
            if provider_data is None:
                abort(404)

            # if there was an authentication error, flash the error messages and exit
            if 'error' in request.args:
                for k, v in request.args.items():
                    if k.startswith('error'):
                        flash(f'{k}: {v}')
                return redirect(url_for('index'))

            # Dexcom OAuth Cycle (Different then others)
            if provider == "dexcom" and provider.strip().lower() == "dexcom":

                # make sure that the state parameter matches the one we created in the
                # authorization request
                if request.args['state'] != session.get('oauth2_state'):
                    debug("Dexcom OAuth State doesn't match, moving on", type="warn")
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

                if not oauth2_token:
                    debug("Fatal Error in Token: Something must have gone wrong")
                    abort(401)
                #
                self.writeToken(provider,  response.json().get('access_token'), response.json().get('refresh_token') )

                return redirect(url_for('index'))

            else: # TODO Add Basic Logic for additional providers
                return redirect(url_for("index"))


        # Initalize Thread Object
        threading.Thread.__init__(self, name="oauth-server", daemon=True)

        if self.self_start: self.start() # Starting the Server
    def start(self):
        debug("Starting all the Worker threads", type="info")

        for worker in self.workers.items():
            worker[1].start() # Start All the workers

        debug("OAuth Sever Starting", type="info")
        super().start()
    def supplyToken(self, provider:str or None = None):
        if provider is not None:
            self.workers[provider].web_worker._token =self.getToken(provider)
        else:
            for provider in self.workers.keys():
                # Update all providers
                self.workers[provider].web_worker._token =self.getToken(provider)

    def checkToken(self, provider: str,)-> bool:
        """Check if token exsists

        Args:
            provider (str): The provider for the OAuth Token

        Returns:
            bool: If the token exsists
        """
        Tokens = Query() # Query TinyDB
        if len(self.db.search(Tokens.provider == provider)) == 0:
            return False # Provider's Token Doesn't Exsist
        else:
            # debug(str(self.db.search(Tokens.provider == provider)), type="Error")
            return True # Some Entry Exsists for the Provider
    def getToken(self, provider: str, isRefresh: bool = False):
        """Get the token of the povider

        Args:
            provider (str): The provider which token is being looked for

        Returns:
            String: Returns the first token for the provider
        """
        Tokens = Query() # Query TinyDB
        return self.db.search(Tokens.provider == provider)[0]["token"] if not isRefresh else self.db.search(Tokens.provider == provider)[0]["refresh_toke"] # Should be token object
    def writeToken(self, provider: str, token: str, refresh_token: str) -> str:
        """Write the tokens or update the exsisting entry

        Args:
            provider (str): OAuth Provider
            token (str): OAuth Token
            refresh_token (str): OAuth Refresh TOken

        Returns:
            str: Current OAuth Token
        """
        Tokens = Query()
        if len(self.db.search(Tokens.provider == provider)) == 1:
            # Update the Query
            self.db.update({"token":token, "refresh_token":refresh_token}, Tokens.provider == provider)
            return self.getToken(provider) # End Context
        elif len(self.db.search(Tokens.provider == provider)) > 1:
            debug("Multiple Providers are listed", type="warn")
            self.db.remove(Tokens.provider == provider)
        # Insert new token data
        self.db.insert({"provider": provider, "token":token, "refresh_token":refresh_token})

        return token

    def requestData(self, provider: str, _type: str, year: str, month: str, day:str or None=None, asCsv:bool = False) -> str:
        try:
            self.supplyToken(provider) # Add Token
            uuid = self.workers[provider].web_worker.getData(_type=_type,url=self.oauth_providers.get(provider)["data_url"],year=year,month=month,day=day,asCsv=asCsv)
            return self.workers[provider].web_worker.getResult(uuid)
        except InvalidToken as e:
            debug(e, type="error")
    def removeToken(self, provider: str) -> None:
        Tokens = Query()

        debug("Removing all providers under the provider tag: {}".format(provider), type="info")

        self.db.remove(Tokens.provider == provider)
        return None

    def refreshToken(self, provider: str) -> None: # TODO Confirm works
        """Refresh the token, only after it expires

        Args:
            provider (str): OAuth Refresh Token's Provider

        Raises:
            Warning: If the token is mising
        Returns:
            Nothing: The token will be written through
        """
        provider_data: dict = current_app.config['OAUTH2_PROVIDERS'].get(provider)

        if not self.checkToken(provider): # If the token is missing
            debug("Refresh Token Provider is Missing!", type="critical")
            raise Warning("Refresh Token Provider Missing: {}".format(self.getToken(provider)))


        # Dexcom OAuth Cycle (Different then others) TODO Implement differents for different ones, should be fine here though
        # if self.provider == "dexcom" and provider.strip().lower() == "dexcom":
        payload = {
            "grant_type": "refresh_token",
            "code": self.getToken(provider, isRefresh=True), # Get Refresh Token
            "redirect_uri": "http://localhost:5000/callback/{}".format(provider),
            "client_id": provider_data["client_id"],
            "client_secret": provider_data["client_secret"]
        }


        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = requests.post(DEXCOM_BASE_URL+"/v2/oauth2/token", data=payload, headers=headers)
        print("Refresh Response" + str(response.content))
        debug("Token request sent with authorization request", type="info")




    def run(self):
        debug("OAuth Application Starting!", type="info")

        self.app.use_reloader=False
        self.app.run(debug=False, port=self.port)


    def join(self, timeout: float | None = None) -> None:
        # self.app.aborter(401)
        debug("OAuth Server Finished", type="info")
        return super().join(timeout)

