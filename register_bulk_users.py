import os
import sys
from python_files.auth_manager import signup_user

def register_bulk_users():
    users_list = [
        "MONIKA N",
        "MUTHU S V",
        "NANDEESH P B",
        "NITHIN KUMAR T C",
        "NITHIN M L",
        "NITHYASHREE A",
        "PARVATH RAJ R",
        "PAWAN SIMHA R",
        "POOJA T R",
        "PRAGATHI K S",
        "PRAJWAL A P",
        "PRAJWAL H K",
        "PRAJWAL N",
        "PRAJWAL R",
        "PRATHIBHA K R",
        "R VIVEK KARTHIK PRASAD",
        "RAGHU K N",
        "RAHUL KATAGERI",
        "RAHUL R",
        "RAJASHREE V",
        "RAKSHITH GOWDA",
        "RASHMI G",
        "ROHITH V",
        "ROOPASHREE P",
        "ROOPESH G",
        "RUCHITHA G",
        "RUDRESHA B M",
        "S PUNEETH"
    ]

    password = os.getenv("BULK_REG_PASSWORD", "Temporary@123")

    
    print(f"Starting registration of {len(users_list)} users...")
    
    for full_name in users_list:
        # Generate email: lower case, no spaces, @gmail.com
        email_prefix = full_name.lower().replace(" ", "")
        email = f"{email_prefix}@gmail.com"
        
        # Split name for first and last name
        name_parts = full_name.split(" ")
        first_name = name_parts[0]
        last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
        
        # Username can be the email prefix
        username = email_prefix
        
        print(f"Registering: {full_name} ({email})...", end=" ")
        
        result = signup_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password
        )
        
        if result["status"] == "success":
            print("SUCCESS")
        else:
            print(f"FAILED: {result['message']}")

if __name__ == "__main__":
    register_bulk_users()
