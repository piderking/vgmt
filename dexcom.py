from httpx_oauth.integrations.fastapi import OAuth2AuthorizeCallback
from httpx_oauth.oauth2 import OAuth2
from fastapi import FastAPI, Depends
import uvicorn
import json
import requests
client = OAuth2("buW1km1Ig6BfWwh0S0S5phKWhmQSse8t", "TWg6r8sazz3WHQn0", "https://sandbox-api.dexcom.com/v2/oauth2/token", "https://sandbox-api.dexcom.com/v2/oauth2/token")
oauth2_authorize_callback = OAuth2AuthorizeCallback(client, "oauth-callback")
app = FastAPI()

tokens, refresh_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI5NzljNGRhMS1mOTliLTRmZGYtOTg3Mi0zOWVhOGQ1NDM1OGEiLCJhdWQiOiJodHRwczovL3NhbmRib3gtYXBpLmRleGNvbS5jb20iLCJzY29wZSI6WyJlZ3YiLCJjYWxpYnJhdGlvbiIsImRldmljZSIsImV2ZW50Iiwic3RhdGlzdGljcyIsIm9mZmxpbmVfYWNjZXNzIl0sImlzcyI6Imh0dHBzOi8vc2FuZGJveC1hcGkuZGV4Y29tLmNvbSIsImV4cCI6MTY4MTk1MjIxOCwiaWF0IjoxNjgxOTQ1MDE4LCJjbGllbnRfaWQiOiJidVcxa20xSWc2QmZXd2gwUzBTNXBoS1dobVFTc2U4dCJ9.fwcWQ5tMXajV0oW1Tc_RFvcLtp7e18qVYD3wLHP5FomvyLB1P8u4lqAxcPMC4XMi33QXFoXZvYQWfYS2oXWZr9N5EvEC_9Y3bK5xDQ_rlq9rxzuNTq9cv_m5VBdSaaa2FSc3ND3rq4nvjq3sQIAgnF_oyzUzu-xinNXLrfBmeOORNOe5nOT4lvPtzlYjNhO92HKPRzfHfGKEZLoVgZ3fpAcNs82iOPzsw0C9na1rw7vtijjSrZFyRFeE8ZuAW4Ocvdve5X8n_7ibwZJYS6TrsI1Jb5bB4jvmDRBuSqOt6avOcPaxTA0RDL6e_rKt2vHPF8rf2ct1n-rwM6PzWwq9JA", "f1749e8056cfebce02e29e903226dd17"

@app.get("/")
def root():
    return "Hello!"

@app.get("/oauth-callback", name="oauth-callback")
async def oauth_callback(access_token_state=Depends(oauth2_authorize_callback)):
    token, state = access_token_state
    print(token)
    # dexcom = DexcomSession("SandboxUser6", home_url="sandbox-api.dexcom.com", client_id="buW1km1Ig6BfWwh0S0S5phKWhmQSse8t", client_secret="TWg6r8sazz3WHQn0", code=json.loads(token)["access_token"])

    
    # Do something useful


@app.get("/bg")
def get_bg():
    url = "https://sandbox-api.dexcom.com/v2/users/self/egvs"

    query = {
      "startDate": "2023-04-01T09:12:35",
      "endDate": "2023-04-01T09:12:36"
    }
    
    headers = {"Authorization": "Bearer {}".format(tokens)}
    
    response = requests.get(url, headers=headers, params=query)
    
    data = response.json()
    print(data)
    return 
"""
https://sandbox-api.dexcom.com/v2/oauth2/login
