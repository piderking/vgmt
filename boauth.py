
from oauth2_client.credentials_manager import CredentialManager, ServiceInformation


scopes = ['offline_access']
service_information = ServiceInformation('https://sandbox-api.dexcom.com/v2/oauth2/login',
                                            'https://sandbox-api.dexcom.com/v2/oauth2/token',
                                            "buW1km1Ig6BfWwh0S0S5phKWhmQSse8t",
                                            "TWg6r8sazz3WHQn0",
                                            scopes)

manager = CredentialManager(service_information,
                                proxies=dict(http='http://localhost:3128', https='http://localhost:3128'))

redirect_uri = 'http://sandbox-api.dexcom.com/v2/oauth2/code'

    # Builds the authorization url and starts the local server according to the redirect_uri parameter
url = manager.init_authorize_code_process(redirect_uri, 'just_a_simple_state')
print('Open this url in your browser\n%s', url)
code = manager.wait_and_terminate_authorize_code_process()
    # From this point the http server is opened on 8080 port and wait to receive a single GET request
    # All you need to do is open the url and the process will go on
    # (as long you put the host part of your redirect uri in your host file)
    # when the server gets the request with the code (or error) in its query parameters
print('Code got = %s', code)
manager.init_with_authorize_code(redirect_uri, code)