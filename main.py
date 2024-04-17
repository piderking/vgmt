client_id = r'buW1km1Ig6BfWwh0S0S5phKWhmQSse8t'
client_secret = r'TWg6r8sazz3WHQn0'
redirect_uri = 'https://sandbox-api.dexcom.com/v2/oauth2/login'

scopes = ['offline_access']

from requests_oauthlib import OAuth2Session
oauth = OAuth2Session(client_id, redirect_uri=redirect_uri,
                          scope=scopes)
authorization_url, state = oauth.authorization_url(
        'https://sandbox-api.dexcom.com/v2/oauth2/login')

print(f'Please go to {authorization_url} and authorize access.')
authorization_response = input('Enter the full callback URL')