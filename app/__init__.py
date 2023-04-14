from .main import createApp
from .routes import useRouter, base, DownloadRouter
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .firebase import fireapp, bucket, initFirebase   
import firebase_admin

# Initialize the App (so no errors on restart)
fireapp, bucket = initFirebase()
print(bucket.blob("default.txt").download_as_string())

app = createApp()
useRouter(app, base)
useRouter(app, DownloadRouter)



