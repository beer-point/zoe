import firebase_admin
from firebase_admin import firestore
import os
# from google.cloud.firestore.Firestore

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./src/firebaseAdminCredentials.json"

default_app = firebase_admin.initialize_app()
client = firestore.client()


def getFirestoreClient() -> firestore.firestore.Client:
    return client
