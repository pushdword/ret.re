
import requests
res = requests.post('http://localhost:5000/test',
json={
    "client":"Other",
    "email":"something@example.com",
    "pass" : "testing123"
    })

print(res.text)