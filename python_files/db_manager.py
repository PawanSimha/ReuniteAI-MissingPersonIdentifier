from pymongo import MongoClient
from datetime import datetime
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

# ---------------- MONGODB CONFIG ----------------
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "reuniteai_db")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# ---------------- COLLECTIONS ------------------
users_collection = db["users"]
face_encodings_collection = db["face_encodings"]
missing_persons_collection = db["missing_persons"]

# ---------------- USERS ------------------------
def get_all_users():
    """
    Returns all registered users (excluding password).
    """
    return list(users_collection.find({}, {"password_hash": 0, "password": 0}))


# ---------------- CONNECTION TEST ----------------
def test_connection():
    try:
        client.admin.command("ping")
        print("MongoDB connection successful.")
        print(f"Connected to database: {DB_NAME}")
    except Exception as e:
        print(f"MongoDB connection failed: {e}")


# ---------------- MISSING PERSON INSERT ----------------
def insert_new_person(person_id, face_encoding, image_path, person_details):
    """
    Inserts a new missing person and face encoding.
    """
    if face_encoding is not None:
        face_doc = {
            "person_id": person_id,
            "face_encoding": face_encoding.tolist() if isinstance(face_encoding, np.ndarray) else face_encoding,
            "image_path": image_path,
            "created_at": datetime.utcnow()
        }
        face_encodings_collection.insert_one(face_doc)

    person_doc = {
        "person_id": person_id,
        "full_name": person_details["full_name"],
        "guardian_name": person_details["guardian_name"],
        "contact": {
            "phone": person_details["phone"],
            "email": person_details.get("email", "")
        },
        "address": {
            "home_address": person_details.get("home_address", ""),
            "missing_location": person_details["missing_location"],
            "missing_date": person_details.get("missing_date", "")
        },
        "image_path": image_path,
        "case_status": "active",
        "created_at": datetime.utcnow()
    }

    missing_persons_collection.insert_one(person_doc)

    print(f"New missing person registered: {person_id}")


# ---------------- FETCH SINGLE PERSON ----------------
def fetch_person_details(person_id):
    """
    Fetch details of a missing person.
    """
    return missing_persons_collection.find_one(
        {"person_id": person_id},
        {"_id": 0}
    )


# ---------------- FETCH ALL MISSING PERSONS ----------------
def get_all_missing_persons():
    """
    Returns all missing persons.
    """
    return list(missing_persons_collection.find({}, {"_id": 0}))


# ---------------- FETCH ALL FACE ENCODINGS ----------------
def get_all_face_encodings():
    """
    Returns all face encodings from database.
    Returns dict: {person_id: numpy_array}
    """
    encodings_dict = {}
    # Project only required fields to minimize memory/bandwidth
    for encoding_doc in face_encodings_collection.find({}, {"person_id": 1, "face_encoding": 1, "_id": 0}):
        person_id = encoding_doc.get("person_id")
        encoding_list = encoding_doc.get("face_encoding")
        if person_id and encoding_list:
            encodings_dict[person_id] = np.array(encoding_list)
    return encodings_dict


# ---------------- UPDATE CASE STATUS ----------------
def update_case_status(person_id, status):
    """
    Update the case status of a missing person.
    """
    missing_persons_collection.update_one(
        {"person_id": person_id},
        {"$set": {"case_status": status}}
    )
