import requests

def test_lead():
    url = "http://localhost:5000/api/lead"
    payload = {
        "name": "Test User",
        "phone": "08012345678",
        "email": "test@example.com",
        "energy_needs": "Full Kit"
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 201:
            print("Lead created successfully:", response.json())
        else:
            print("Failed to create lead:", response.text)
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    test_lead()
