import os
import sys
from pymongo import MongoClient
from dotenv import load_dotenv

project_root = r"c:\Users\pawan\SNPSU\Projects\ReuniteAI"
load_dotenv(os.path.join(project_root, ".env"))

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "reuniteai_db")

def check_live_db():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        db = client[DB_NAME]
        users_col = db["users"]
        
        print(f"Connected to {MONGO_URI}, DB: {DB_NAME}")
        
        admin_email = os.getenv("ADMIN_EMAIL", "pawansimha@gmail.com")
        admin = users_col.find_one({"email": admin_email})
        
        if admin:
            print(f"Admin found: {admin['email']}")
            print(f"Admin Hash in DB: {admin.get('password_hash')}")
        else:
            print(f"Admin {admin_email} NOT FOUND in live DB.")
            
        # Check first 5 users
        print("\nOther users in DB:")
        for user in users_col.find().limit(5):
            print(f"- {user['email']}: {user.get('password_hash')[:20]}...")
            
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")

if __name__ == "__main__":
    check_live_db()
