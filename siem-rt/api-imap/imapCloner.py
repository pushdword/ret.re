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


#IMAP of Office 365 route
@app.route('/imapO365',methods=['POST'])
def imapO365():
    content = request.get_json(silent=True)

    return "OK"

#IMAP of Google route
@app.route('/imapGoogle',methods=['POST'])
def imapGoogle():
    content = request.get_json(silent=True)

    return "OK"

#IMAP of Others
@app.route('/imapTry',methods=['POST'])
def imapTry():
    content = request.get_json(silent=True)

    return "OK"



# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
