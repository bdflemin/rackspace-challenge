#!/usr/bin/python
import sys, time, os, requests
from werkzeug import MultiDict

def create_route(apiKey):
    return requests.post(
        "https://api.mailgun.net/v2/routes",
        auth=("api", apiKey),
        data=MultiDict([("priority", 1),
                        ("description", "Challenge 12 route"),
                        ("expression", "match_recipient('brya5376@apichallenges.mailgun.org')"),
                        ("action", "forward('http://cldsrvr.com/challenge1')"),
                        ("action", "start()")]))

try:
	homedir = os.getenv("HOME")
	apiKey = open(homedir+"/.mailgunapi",'r').read()
except:
	print "Must have a file called ~/.mailgunapi... Try again when you have that file"
	sys.exit()

create_route(apiKey)