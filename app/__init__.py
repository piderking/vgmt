from .main import createApp
from .routes import useRouter, base, DownloadRouter
from fastapi import FastAPI, Request
from time import sleep
# import firebase_admin




app, fireapp = createApp()
useRouter(app, base)
useRouter(app, DownloadRouter)

# from .routes.download.fetch import Blob # Firebase Cloud Storage Download Test 


