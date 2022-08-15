import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

credential=credentials.ApplicationDefault()
firebase_admin.initialize_app(credential)

db=firestore.client()

def get_users():
    return db.collection("users").get()

