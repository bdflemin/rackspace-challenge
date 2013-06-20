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

import pyrax, sys, argparse, time

domain = ""
complete = []
parser = argparse.ArgumentParser(description='Challenge 4 usage.')
parser.add_argument('--ip', nargs='?', dest='hostip', required=True, help="The ip to use for the DNS A Record")
parser.add_argument('--fqdn', nargs='?', dest='fqdn', required=True, help="Fully Qualified Domain Name")
parser.add_argument('--username', nargs='?', dest='username', required=True, help="Your Cloud Username")
parser.add_argument('--password', nargs='?', dest='password', required=True, help="Your Cloud API Key")
args = parser.parse_args()

pyrax.set_credentials(args.username,args.password)

dns = pyrax.cloud_dns

for dom in dns.list():
	if dom.name == args.fqdn:
		print "Found this domain: ", dom.name
		domain = dom
		break
if not domain:
	print "Couldn't find a domain that matches your A-Record request. Exiting"
	sys.exit()
print "Will now create the A-Record", args.fqdn, "using the ip address", args.hostip
rec = [{"type": "A", "name": str(args.fqdn), "data": str(args.hostip)}]
complete = dns.add_records(domain, rec)
if complete:
	print "Congrats, the new A-Record for", args.fqdn, "has been completed!!"
