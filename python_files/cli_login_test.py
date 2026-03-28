import requests
from bs4 import BeautifulSoup
import argparse

def test_login(email, password, base_url="http://127.0.0.1:5000"):
    print(f"--- Attempting Login for {email} ---")
    session = requests.Session()
    
    # 1. Get the login page to fetch CSRF token
    try:
        response = session.get(base_url)
        if response.status_code != 200:
            print(f"Error: Unable to reach {base_url} (Status: {response.status_code})")
            return
            
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
        print(f"Fetched CSRF Token: {csrf_token[:10]}...")
        
        # 2. Perform the POST login
        login_url = f"{base_url}/login"
        payload = {
            "csrf_token": csrf_token,
            "email": email,
            "password": password
        }
        
        # The app redirects on success
        login_response = session.post(login_url, data=payload, allow_redirects=True)
        
        if "/user/home" in login_response.url or "/admin/dashboard" in login_response.url:
            print(f"SUCCESS: Logged in successfully. Redirected to: {login_response.url}")
        else:
            # Check for generic error messages in the HTML
            if "Invalid password" in login_response.text:
                print("FAILED: Invalid password.")
            elif "User not found" in login_response.text:
                print("FAILED: User not found.")
            else:
                print(f"FAILED: Login unsuccessful. (URL: {login_response.url})")
                
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test ReuniteAI login from command line.")
    parser.add_argument("--email", default="pawansimha@gmail.com", help="Email to login with")
    parser.add_argument("--password", default="Hercules", help="Password to login with")
    parser.add_argument("--url", default="http://127.0.0.1:5000", help="Base URL of the app")
    
    args = parser.parse_args()
    test_login(args.email, args.password, args.url)
