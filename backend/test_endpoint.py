import requests

# Test if the endpoint exists and returns proper error for unauthorized access
BASE_URL = "http://localhost:8000"

def test_unauthorized_access():
    """Test that the endpoint requires authentication"""
    response = requests.get(f"{BASE_URL}/applications/my-applications")
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Should return 403 Forbidden since no token is provided
    assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    print("OK - Endpoint correctly requires authentication")

if __name__ == "__main__":
    print("Testing the new 'my-applications' endpoint...")
    test_unauthorized_access()
    print("Test completed successfully!")