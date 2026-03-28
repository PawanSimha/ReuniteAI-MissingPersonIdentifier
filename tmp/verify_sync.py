import os
import sys

project_root = r"c:\Users\pawan\SNPSU\Projects\ReuniteAI"
sys.path.append(project_root)

from python_files.auth_manager import verify_password, login_user
from dotenv import load_dotenv

load_dotenv(os.path.join(project_root, ".env"))

def verify_sync():
    print("--- Verifying Bulk Sync ---")
    bulk_email = "monikan@gmail.com"
    bulk_pass = "Temporary@123"
    
    try:
        result = login_user(bulk_email, bulk_pass)
        print(f"login_user for {bulk_email}: {result['status']}")
        if result['status'] == "success":
            print("SUCCESS: Bulk sync confirmed.")
        else:
            print(f"FAILED: {result.get('message')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_sync()
