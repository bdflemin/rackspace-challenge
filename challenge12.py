#!/usr/bin/python
# Copyright 2013 Rackspace
#
# All Rights Reserved.
#    Licensed under the Apache License, Version 2.0 (the "License"); you may    
#    not use this file except in compliance with the License. You may obtain    
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#                  
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT  
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the  
#    License for the specific language governing permissions and limitations    
#    under the License.

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
