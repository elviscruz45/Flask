import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

credential=credentials.ApplicationDefault()
firebase_admin.initialize_app(credential)

db=firestore.client()

def get_users():
    return db.collection("Users").get()

def get_todos(user_id):
    return db.collection("Users").document(user_id).collection("todos").get()
