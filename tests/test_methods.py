#   ---------------------------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""This is a sample python file for testing functions from the source code."""
from __future__ import annotations

from vgmt import __version__
from vgmt.util import Thread, Data
from vgmt.config import  STATUS, CLIENT, BASE_URL
import time
import time
import random

def test_version():
    """
    This test is marked implicitly as an integration test because the name contains "_init_"
    https://docs.pytest.org/en/6.2.x/example/markers.html#automatically-adding-markers-based-on-test-names
    """

    print(__version__)
    assert STATUS if __version__ != None else False

def test_threads():

    t = Thread(self_start=True, data=[x for x in range(1000)])


    time.sleep(1)
    t.join()

    #print(t.results)
    #for x in t.results:
    #    print("The target was {} during the datasets from percents {}% to {}%".format(len(x), x[0]/10, x[-1]/10))
    print(t.results)
    assert True



from oauth2_client.credentials_manager import CredentialManager, ServiceInformation

def test_oauth():
    scopes = ['scope_1', 'scope_2']

    service_information = ServiceInformation(BASE_URL + '/v2/oauth2/login',
                                            BASE_URL + '/v2/oauth2/token',
                                            CLIENT["dexcom-id"],
                                            CLIENT["dexcom-secret"],
                                            scopes)
    print(BASE_URL + '/v2/oauth2/login',
                                            BASE_URL + '/v2/oauth2/token',
                                            CLIENT["dexcom-id"],
                                            CLIENT["dexcom-secret"],
                                            scopes)
    manager = CredentialManager(service_information,
                                proxies=dict(http='http://localhost:3128', https='http://localhost:3128'))
    redirect_uri = 'http://somewhere.io:8080/oauth/code'

    # Builds the authorization url and starts the local server according to the redirect_uri parameter
    url = manager.init_authorize_code_process(redirect_uri, 'state_test')
    print('Open this url in your browser\n%s', url)

    code = manager.wait_and_terminate_authorize_code_process()
    # From this point the http server is opened on 8080 port and wait to receive a single GET request
    # All you need to do is open the url and the process will go on
    # (as long you put the host part of your redirect uri in your host file)
    # when the server gets the request with the code (or error) in its query parameters
    print('Code got = %s', code)
    manager.init_with_authorize_code(redirect_uri, code)