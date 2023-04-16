from fastapi import FastAPI
from .util import config
from .firebase import initFirebase
"""
from fastapi.middleware.trustedhost import TrustedHostMiddleware
app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com"]
)
"""


def createApp():
    # Initialize the App (so no errors on restart)
    fireapp = initFirebase()
    app = FastAPI(title=config.title, debug=config.debug)
    
    @app.get("/")
    async def root():
        return {"message": "Hello World"}
    print("API Server Initalized")
    return app, fireapp
