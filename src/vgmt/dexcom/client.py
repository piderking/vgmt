import os
from ..config import BASE_URL, CLIENT, SANDBOX
from uuid import uuid4
from ..util import Thread
from .data import DexcomData
# https://developer.dexcom.com/account/apps



class DexcomClient(Thread):
    def __init__(self) -> None:
        self.url = BASE_URL
        self.id = uuid4()
        self.requests=[]
        self.data=DexcomData()

        self.token = self.requestToken()

        if self.token is None:
            raise ValueError("Token Code is Wrong")

        super.__init__(data=self.data, self_start=False)

    def requestToken(self):
        return None

    @super().threaded
    def requestData(index: int, request: dict): # [{}]
        # Request Data from Dexcom
        pass
