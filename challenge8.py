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

import pyrax, sys, argparse, os, urlparse

parser = argparse.ArgumentParser(description='Challenge 8 usage.')
parser.add_argument('--domain', nargs='?', dest='domain', required=True, help="The Cloud DNS Domain to use")
parser.add_argument('--username', nargs='?', dest='username', required=True, help="Your Cloud Username")
parser.add_argument('--password', nargs='?', dest='password', required=True, help="Your Cloud API Key")
args = parser.parse_args()

pyrax.set_credentials(args.username,args.password)

cf = pyrax.cloudfiles
cdns = pyrax.cloud_dns

dnsID = ""
print "Checking domain..."
for d in cdns.get_domain_iterator():
	if str(d.name) == args.domain:
		print "... Domain exists, continuing with the challenge\n"
		dnsID = str(d.id)
		break

if not dnsID:
	print "... Domain doesn't exist, try again"
	sys.exit()

print "Starting this challenge with creating a container..."
cont = cf.create_container("challenge8")
cf.make_container_public(cont.name, ttl=900)
print "... Container Name =", cont.name
print "... CDN Enabled =", cont.cdn_enabled
print "... Setting metadata for container now"
metadata = {'X-Container-Meta-Web-Index': 'index.html'}
cf.set_container_metadata(cont, metadata)
print "... Creating the index.html into the container"
content = "Thanks for completing challenge 8!!"
obj = cf.store_object(cont.name,"index.html", content)
if obj.name:
	print "...... Done"
else:
	print "...... Was not able to create object, please talk to administrator for more details"
	sys.exit()
print "... Creating CNAME named challenge8."+args.domain
try:
	dom = cdns.get(dnsID)
	arecord = urlparse.urlsplit(cont.cdn_uri).netloc
	rec = dom.add_records({"type": "CNAME", "name": "challenge8."+args.domain, "data": arecord, "ttl": 6000})
	print "... The CNAME", rec[0].name, "has been created without any issues. Challenge is complete."
except pyrax.exceptions.DomainRecordAdditionFailed:
	print "\nThe record of challenge8."+args.domain, "exists. Exiting challenge and please clean up containers and records."
	sys.exit()
