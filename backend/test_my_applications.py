import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_login():
    """Test user login to get token"""
    login_data = {
        "email": "applicant@example.com",  # Replace with actual test user
        "password": "securepassword123"   # Replace with actual test password
    }
    
    response = requests.post(f"{BASE_URL}/registration/login", json=login_data)
    
    if response.status_code == 200:
        token = response.json().get("access_token")
        print(f"Login successful. Token: {token}")
        return token
    else:
        print(f"Login failed: {response.status_code} - {response.text}")
        return None

def test_get_my_applications(token):
    """Test getting current user's applications"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(f"{BASE_URL}/applications/my-applications", headers=headers)
    
    if response.status_code == 200:
        applications = response.json()
        print(f"My Applications retrieved successfully:")
        print(json.dumps(applications, indent=2))
        return applications
    else:
        print(f"Getting my applications failed: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    print("Testing the new 'my-applications' endpoint...")
    
    # Login to get token
    token = test_login()
    
    if token:
        # Test the new endpoint
        test_get_my_applications(token)
    else:
        print("Skipping test due to login failure.")