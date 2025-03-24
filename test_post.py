import requests

url = "http://127.0.0.1:5000/log-ticket"
headers = {"Content-Type": "application/json"}
data = {
    "ticket_id": "TIC-TEST-123",
    "title": "Test Ticket",
    "resolution_notes": "Resolved in testing."
}

response = requests.post(url, json=data, headers=headers)
print("Status Code:", response.status_code)
print("Response:", response.text)
