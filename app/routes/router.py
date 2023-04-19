from fastapi import APIRouter

class Router(APIRouter):


    def __init__(self, prefix:str, *args, **kwargs):
        super().__init__(args, kwargs, prefix=prefix) # Give 