import os
import sys
from pymongo import MongoClient
from dotenv import load_dotenv

project_root = r"c:\Users\pawan\SNPSU\Projects\ReuniteAI"
sys.path.append(project_root)

from python_files.auth_manager import hash_password

load_dotenv(os.path.join(project_root, ".env"))

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "reuniteai_db")

def update_bulk_passwords():
    # List of names from register_bulk_users.py
    users_list = [
        "MONIKA N", "MUTHU S V", "NANDEESH P B", "NITHIN KUMAR T C",
        "NITHIN M L", "NITHYASHREE A", "PARVATH RAJ R", "PAWAN SIMHA R",
        "POOJA T R", "PRAGATHI K S", "PRAJWAL A P", "PRAJWAL H K",
        "PRAJWAL N", "PRAJWAL R", "PRATHIBHA K R", "R VIVEK KARTHIK PRASAD",
        "RAGHU K N", "RAHUL KATAGERI", "RAHUL R", "RAJASHREE V",
        "RAKSHITH GOWDA", "RASHMI G", "ROHITH V", "ROOPASHREE P",
        "ROOPESH G", "RUCHITHA G", "RUDRESHA B M", "S PUNEETH"
    ]

    new_password = "Temporary@123"
    new_hash = hash_password(new_password)

    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        users_col = db["users"]

        updated_count = 0
        for full_name in users_list:
            email_prefix = full_name.lower().replace(" ", "")
            email = f"{email_prefix}@gmail.com"
            
            result = users_col.update_one(
                {"email": email},
                {"$set": {"password_hash": new_hash}}
            )
            if result.modified_count > 0:
                updated_count += 1
                print(f"Updated: {email}")
            elif result.matched_count > 0:
                print(f"Already set (or no change needed): {email}")
            else:
                print(f"NOT FOUND: {email}")

        print(f"\nSuccessfully updated {updated_count} users to '{new_password}'")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_bulk_passwords()
