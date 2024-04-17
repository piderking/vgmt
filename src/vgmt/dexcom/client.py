import os
from ..config import BASE_URL, CLIENT, SANDBOX
from uuid import uuid4
from ..util import Thread
# https://developer.dexcom.com/account/apps



class DexcomClient(Thread):
    def __init__(self, token:str or None = None) -> None:
        self.url = BASE_URL
        self.id = uuid4()

        self.token = self.requestToken() if token is None else token # Get the token


        if self.token is None:
            raise ValueError("Token Code is Wrong")

        super.__init__(self_start=False)

    def requestToken(self):
        return None

    def requestData(index: int, request: dict): # [{}]
        # Request Data from Dexcom
        pass
