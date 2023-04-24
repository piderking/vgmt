from .sessionToken import SessionToken, validateWrapper
from pydantic import BaseModel
import requests
import concurrent.futures


# Outside, basic fetch url
def load_url(url, token, timeout):
    # url = "https://sandbox-api.dexcom.com/v3/users/self/egvs
    query = {
    # TODO implement custom date
    "startDate": "2022-02-06T09:12:00",
    "endDate": "2022-02-06T09:12:35",
    }

    headers = {"Authorization": "Bearer {}".format(token)}

    return requests.get(url, timeout=timeout, headers=headers, params=query)
class DexcomData():
    _urls: list[str] # Normal (Non-Sanbox API Route)
    sandbox: bool= False
    
    def __init__(self, url:list[str], dates: list[list[str]], sanbox:bool = True) -> None:
        self.sandbox = sanbox
        self._urls = url 
        self.dates = dates
    @property
    def urls(self):
        return ["sandbox-" + url if self.sandbox else url for url in self._urls]
    
    @url.setter
    def url(self, url: str): # TODO Change from sandbox to prod
        self._urls = url
        
    def fetch(self, bearer_token:str):
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            future_to_url = {executor.submit(load_url, url, bearer_token, 10): url for url in self.urls()}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    data = future.result()
                    print(data)
                except Exception as exc:
                    resp_err = resp_err + 1





class DexcomUser(object):
    def __init__(self, user_id, auth_token, refresh_token) -> None:
        self.userId: str = user_id
        self._authToken: str = auth_token
        self._refresh_token: str = refresh_token 
    
    
    @property
    @validateWrapper()
    def authToken(self, sessionToken: SessionToken, accept: bool = False) -> str | None:

        return self._authToken if accept else  None # Wrapper will change around parameters
        
    def authenticate(self):
        pass