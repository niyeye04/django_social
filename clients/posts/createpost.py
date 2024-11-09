import requests

auth_endpoint = ""
auth_data = {
    "username": "test1",
    "password": "kajambembele"
}

auth_response = requests.post(auth_endpoint, data=auth_data)

if auth_response.status_code == 200:
    print("Logged in successfull")
    token = auth_response.json().get("Token")