from .sessionToken import SessionToken, validateWrapper


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