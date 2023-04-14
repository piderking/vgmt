from fastapi import FastAPI
from .util import config

"""
from fastapi.middleware.trustedhost import TrustedHostMiddleware
app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com"]
)
"""


def createApp():
    app = FastAPI(title=config.title, debug=config.debug)

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    return app
