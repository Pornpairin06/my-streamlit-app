import requests

API_KEY = "AIzaSyB_W3qfjxNQuEZgDbbxfi-l-p9WJ1MZvZs"

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

data = {
    "contents": [{
        "parts": [{"text": "ทดสอบ"}]
    }]
}

response = requests.post(url,json=data)

print("STATUS:", response.status_code)
print("TEXT:", response.text)