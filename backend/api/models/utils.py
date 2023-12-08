import random
import string

from firebase_admin import credentials, firestore, initialize_app

def generate_id() -> str:
    return "".join(random.choices(string.ascii_uppercase, k=6))

cred = credentials.Certificate('key.json')
firebase_app = initialize_app(cred)
db = firestore.client()