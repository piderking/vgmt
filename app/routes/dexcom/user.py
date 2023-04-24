from .sessionToken import SessionToken, validateWrapper
from pydantic import BaseModel

class DexcomData():
    _url: str # Normal (Non-Sanbox API Route)
    sandbox: bool= False
    
    def __init__(self, url:str, sanbox:bool = True) -> None:
        self.sandbox = sanbox
        self.url = url
    @property
    def url(self):
        return "sandbox-" + self._url if self.sandbox else self._url
    @url.setter
    def url(self, url: str): # TODO Change from sandbox to prod
        self._url = url
    
    def fetch(self, token)
import requests
import concurrent.futures

def get_urls():
    return ["https://google.com","https://google.com"]

def load_url(url, timeout):
    return requests.get(url, timeout = timeout)

with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:

    future_to_url = {executor.submit(load_url, url, 10): url for url in     get_urls()}
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