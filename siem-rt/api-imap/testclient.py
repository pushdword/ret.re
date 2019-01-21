
import requests
res = requests.post('http://localhost:5000/test',
json={
    "client":"O365",
    "email":"test@msn.com",
    "pass" : ""
    })

print(res.text)