
import requests
res = requests.post('http://localhost:5000/test',
json={
    "client":"O365",
    "email":"something@example.com",
    "pass" : "testing123"
    })

print(res.text)