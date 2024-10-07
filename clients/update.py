import requests
auth_endpoint = "http://127.0.0.1:8000/api/auth/"

auth_data = {
    "username": "mednson",
    "password": "niyeye"
}

auth_response = requests.post(auth_endpoint, json=auth_data)

if auth_response.status_code == 200:
    print("Logged in successful")
    token = auth_response.json()['token']
    headers = {
        "Authentication": f"Token {token}"
    }
    data = {
        "phonenumber":"0678934242",
        "bio":"I'm still the admin"
    }
    endpoint = "http://127.0.0.1:8000/api/update_profile/"

    response = requests.patch(endpoint, headers=headers, json= data)

    print(response)
    