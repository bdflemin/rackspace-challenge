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

parser = argparse.ArgumentParser(description='Challenge 9 usage.')
parser.add_argument('--fqdn', nargs='?', dest='fqdn', required=True, help="The FQDN to use for the challenge")
parser.add_argument('--flavor', nargs='?', dest='flavor', required=True, help="The flavor to us")
parser.add_argument('--img', nargs='?', dest='img', required=True, help="The image id to use")
parser.add_argument('--username', nargs='?', dest='username', required=True, help="Your Cloud Username")
parser.add_argument('--password', nargs='?', dest='password', required=True, help="Your Cloud API Key")
args = parser.parse_args()

pyrax.set_credentials(args.username,args.password)

cs = pyrax.cloudservers
cdns = pyrax.cloud_dns

def cleanup(server):
	print "\nStart the cleaning process..."
	print "Deleting the server", server.name
	server.delete()
	sys.exit()

def challenge9():
	print "Verifying..."
	if [i for i in cs.images.list() if str(i.id) == str(args.img)]:
		if [f for f in cs.flavors.list() if str(f.id) == str(args.flavor)]:
			print "Both the flavor and image ids are good..."
		else:
			print "The flavor id is not correct, please try again."
			sys.exit()
	else:
		print "The image id couldn't be found, please try again."
		sys.exit()

	print "Creating server... ", args.fqdn 
	created = cs.servers.create(args.fqdn, args.img, args.flavor)

	while not cs.servers.get(created.id).accessIPv4:
		sys.stdout.write('.')
		sys.stdout.flush()
		time.sleep(30)
	newPassword = created.adminPass
	newIP = cs.servers.get(created.id).accessIPv4
	print "\nAdmin password: ", str(newPassword)
	print "Server IPs: ", str(newIP)

	print "Adding DNS recorded name:", args.fqdn, "..."
	try:
		dom = cdns.create(name=args.fqdn, emailAddress="challenge9@rackspace.com")
		rec = [{"type": "A", "name": str(args.fqdn), "data": str(newIP), "ttl": 6000}]
		dom.add_records(rec)
		print "The domain and A-Record named", args.fqdn, "has been created successfully."
	except:
		print "Domain creation failed:", sys.exc_info()[0]
		cleanup(cs.servers.get(created.id))
	
challenge9()
