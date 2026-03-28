import requests

def verify_register_page_image():
    base_url = "http://127.0.0.1:5000"
    # Note: We need to be logged in to access /register_missing
    # However, I can try to check if the redirect happens correctly or if I can mock the session.
    # Since I'm running against a live server, I'll try to reach it.
    
    # Test case: Absolute path in query param (common failure case on Windows)
    abs_path = "C:\\Users\\pawan\\SNPSU\\Projects\\ReuniteAI\\images\\temp\\06a1efcc-735b-4489-a0d5-c805d407cf64.jpeg"
    url = f"{base_url}/register_missing?image_path={abs_path}"
    
    print(f"Testing URL with absolute path: {url}")
    # This might redirect to / if not logged in.
    # But let's see what happens.
    try:
        response = requests.get(url, allow_redirects=False)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 302:
            print(f"Redirected to: {response.headers.get('Location')}")
            print("Server is likely protecting the route with login session.")
        elif response.status_code == 200:
            content = response.text
            if '<img src="/images/temp/06a1efcc-735b-4489-a0d5-c805d407cf64.jpeg"' in content:
                print("SUCCESS: Image path was correctly normalized to relative path in HTML!")
            else:
                print("FAILURE: Image path not found or not normalized correctly.")
                # Print a bit of the content for debugging
                if "Uploaded Image:" in content:
                    start = content.find("Uploaded Image:")
                    print("Context:", content[start:start+200])
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_register_page_image()
