import requests

auth_endpoint = "http://127.0.0.1:8000/api/auth/"
auth_data = {
    "username": "mednson",
    "password": "niyeye"
}

auth_response = requests.post(auth_endpoint, json=auth_data)

if auth_response.status_code == 200:
    print("Logged in successfully")
    token = auth_response.json().get('token')
    
    if token:  # Ensure the token exists
        headers = {
            "Authorization": f"Token {token}",
            "Content-Type": "application/json"  # Set Content-Type
        }
        data = {
            "phone_number": "067880000",
            "bio": "I'm still the admin",
            # Only include the fields you want to update
            # Add other fields if needed, e.g. "email": "new_email@example.com"
        }
        endpoint = "http://127.0.0.1:8000/api/profile/update/"
        
        response = requests.patch(endpoint, headers=headers, json=data)
        print(response.status_code)  # This will show the response status
        print(response.text)  # This will show the response body for additional info
    else:
        print("Token not found in response")
else:
    print(f"Login failed: {auth_response.status_code} - {auth_response.text}")

    