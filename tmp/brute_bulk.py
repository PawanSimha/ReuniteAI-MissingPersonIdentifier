import os
import sys

project_root = r"c:\Users\pawan\SNPSU\Projects\ReuniteAI"
sys.path.append(project_root)

from python_files.auth_manager import verify_password
from dotenv import load_dotenv

load_dotenv(os.path.join(project_root, ".env"))

def brute_force_bulk():
    bulk_hash = "$2b$12$gYeVpjLZPc7EHkv1HHNlnOAHRg0Oit6phq7Go8CasG1uKlV5cmhHK" # monikan@gmail.com
    
    candidates = [
        "Temporary@123",
        "temporary@123",
        "Monika@123",
        "monika@123",
        "monikan",
        "monikan@123",
        "Admin@123",
        "admin123",
        "password",
        "12345678",
        "ReuniteAI@123",
        "reuniteai123"
    ]
    
    print(f"Testing candidates against hash: {bulk_hash}")
    for c in candidates:
        if verify_password(c, bulk_hash):
            print(f"FOUND MATCH: {c}")
            return
    print("No match found in candidates.")

if __name__ == "__main__":
    brute_force_bulk()
