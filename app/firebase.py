import firebase_admin
from firebase_admin.storage import _StorageClient
import os

def initFirebase():
    cred = firebase_admin.credentials.Certificate(os.path.join( "auth", "firebase.json"))
    app = firebase_admin.initialize_app(cred, {'storageBucket': 'vgmt-4a063.appspot.com'})
    # bucket = firebase_admin.storage.bucket()
    
    print("Firebase Initalized")
    return app



# TODO Use Encryption Tactics