---
layout: post
title:  "SIEM for redteam - Architecture for test01 scenario - Phishing event"
date:   2019-01-15 01:10:00 +0000
categories: phishing siem redteam
---
## Architecture what?
Yes. "SIEM"-like for red teaming. I've thinking about doing this a long time ago but I've never did it.
I admit that must be there some tools that do this but, who knows. Let's do it.

## Requirements
Ok, so the idea is that once phishing framework is running and a victim is catched there is just a problem:
* Delayed response to the event of successful compromise
* User puts wrong credentials and then gives up because phishing system shows "error, try again later" and then redirects to the valid page.

The task here is to try on the fly if the credentials works. If it works hacks in ;) calls REST API for the context (gmail or office 365, ...) then calls internal service to clone the mailbox via IMAP. Redirects the user to a valid page if the credential are ok and deletes the physhing instances. If creds are wrong refresh the phishing page :) easy?.



## Architecture design
I used google cloud platform layout but this can be achived on prem or using other cloud services. The only part here that must be in the cloud is the "Cloud CDN" in order to abuse the trusted domain for example aws cloudfront.

![Test01 - phishing event](/images/post01/SIEM_for_RT_-_Test01_scenario.png)

All traffic is recorded in a database in order to be consulted by our future "SIEM" for RT. This is a draft version. It's missing a lot of things that I'll add later.

When sucessful it triggers a general API. I don't know if it's good idea to put this behind a CDN or not. We'll see that later.
This General API will lookup what calls is. At the moment we are just designing the IMAP credentials stealing. We can at this moment inform our future SIEM of compromised client via email, syslog, cef, or whatever. Forwards the call to the IMAP API that will then invoke a job on a instance running a IMAP cloner/client. For example: OfflineIMAP.

## Future development
What I think we will use:
* CloudFront from AWS
* Instances from digital ocean or AWS.
* Python3 scripts to deal with all rest API's
* OfflineIMAP module for python
* MySQL to store history of traffic and events
* Prelude SIEM - To be reviewed later
* Gophish or FiercePhish

Wait and see what is coming! 

[pushdword-gh]:   https://github.com/pushdword
