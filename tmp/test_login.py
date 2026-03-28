import os
import sys

# Add the project root to sys.path to import python_files
project_root = r"c:\Users\pawan\SNPSU\Projects\ReuniteAI"
sys.path.append(project_root)

from python_files.auth_manager import verify_password, login_user
from dotenv import load_dotenv

load_dotenv(os.path.join(project_root, ".env"))

def test_credentials():
    print("--- Testing Admin Credentials ---")
    admin_email = "pawansimha@gmail.com"
    admin_pass = "Hercules"
    
    # Try direct verify first (assuming we have the hash from db_dump)
    admin_hash_from_dump = "$2b$12$vIOAevjBF2tflPIooHVOBeIAclcZZ0Eg1twK4fSL4TXWfI9Gv5wcG"
    is_valid = verify_password(admin_pass, admin_hash_from_dump)
    print(f"Verify 'Hercules' against Admin hash from dump: {is_valid}")
    
    # Try login_user (requires MongoDB running)
    try:
        result = login_user(admin_email, admin_pass)
        print(f"login_user result for Admin: {result}")
    except Exception as e:
        print(f"login_user failed (likely MongoDB not running): {e}")

    print("\n--- Testing Bulk User Credentials ---")
    bulk_email = "monikan@gmail.com"
    bulk_pass = "Temporary@123"
    bulk_hash_from_dump = "$2b$12$gYeVpjLZPc7EHkv1HHNlnOAHRg0Oit6phq7Go8CasG1uKlV5cmhHK"
    is_valid_bulk = verify_password(bulk_pass, bulk_hash_from_dump)
    print(f"Verify 'Temporary@123' against Bulk User hash from dump: {is_valid_bulk}")

    try:
        result_bulk = login_user(bulk_email, bulk_pass)
        print(f"login_user result for Bulk User: {result_bulk}")
    except Exception as e:
        print(f"login_user failed: {e}")

if __name__ == "__main__":
    test_credentials()
