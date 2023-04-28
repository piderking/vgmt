from .main import createApp
from .routes import base, DownloadRouter
from fastapi import FastAPI, Request
from time import sleep
# import firebase_admin




app, fireapp = createApp()
app.include_router(base)
app.include_router(DownloadRouter)

# from .routes.download.fetch import Blob # Firebase Cloud Storage Download Test 
