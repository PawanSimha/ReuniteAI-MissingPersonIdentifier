import requests
import os

def test_image_route():
    base_url = "http://127.0.0.1:5000"
    # Use an existing image from images/temp
    image_name = "06a1efcc-735b-4489-a0d5-c805d407cf64.jpeg"
    url = f"{base_url}/images/temp/{image_name}"
    
    print(f"Testing URL: {url}")
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Successfully reached image route!")
            print(f"Content-Type: {response.headers.get('Content-Type')}")
            print(f"Content-Length: {response.headers.get('Content-Length')}")
        else:
            print(f"Failed to reach image. Status: {response.status_code}")
    except Exception as e:
        print(f"Error connecting to server: {e}")

if __name__ == "__main__":
    test_image_route()
