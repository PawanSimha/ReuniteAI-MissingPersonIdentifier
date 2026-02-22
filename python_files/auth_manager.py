from pymongo import MongoClient
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from datetime import datetime

import os
from dotenv import load_dotenv

load_dotenv()

# ---------------- MongoDB ----------------
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "reuniteai_db")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
users_collection = db["users"]

# ---------------- Password Hashing ----------------
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    """Generate bcrypt hash"""
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Safely verify password against hash"""
    try:
        return pwd_context.verify(password, hashed_password)
    except UnknownHashError:
        # Handles legacy / corrupted hashes
        return False

# ==================================================
# SIGN UP
# ==================================================
def signup_user(first_name, last_name, username, email, password, role="user"):
    if users_collection.find_one({"email": email}):
        return {
            "status": "error",
            "message": "User already exists"
        }

    users_collection.insert_one({
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "email": email,
        "password_hash": hash_password(password),  # ✅ single source of truth
        "role": role,
        "created_at": datetime.utcnow()
    })

    return {
        "status": "success",
        "message": "User registered successfully"
    }

# ==================================================
# LOGIN
# ==================================================
def login_user(email, password):
    user = users_collection.find_one({"email": email})

    if not user:
        return {
            "status": "error",
            "message": "User not found"
        }

    # 🔐 Support both old and new users
    hashed_password = user.get("password_hash") or user.get("password")

    if not hashed_password:
        return {
            "status": "error",
            "message": "Password not set for this user"
        }

    if verify_password(password, hashed_password):
        return {
            "status": "success",
            "email": user["email"],
            "username": user.get("username", ""),
            "role": user.get("role", "user")
        }

    return {
        "status": "error",
        "message": "Invalid password"
    }

# ==================================================
# ADMIN HELPERS
# ==================================================
def get_all_users():
    """Return all users (excluding password hashes)"""
    return list(
        users_collection.find(
            {},
            {"password_hash": 0, "password": 0}
        )
    )

# ==================================================
# INITIALIZE ADMIN ACCOUNT
# ==================================================
def initialize_admin_account():
    """Ensure admin account exists with fixed credentials"""
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")
    
    if not admin_email or not admin_password:
        print("[CRITICAL] ADMIN_EMAIL or ADMIN_PASSWORD not set in environment. Skipping admin initialization.")
        return

    
    admin_user = users_collection.find_one({"email": admin_email})
    
    if not admin_user:
        users_collection.insert_one({
            "first_name": "Admin",
            "last_name": "User",
            "username": "admin",
            "email": admin_email,
            "password_hash": hash_password(admin_password),
            "role": "admin",
            "created_at": datetime.utcnow()
        })
        print(f"Admin account created: {admin_email}")
    elif admin_user.get("role") != "admin":
        # Update existing user to admin role if needed
        users_collection.update_one(
            {"email": admin_email},
            {"$set": {"role": "admin", "password_hash": hash_password(admin_password)}}
        )
        print(f"Admin account updated: {admin_email}")