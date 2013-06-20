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

servers = []
flv = 2
img = "c195ef3b-9195-4474-b6f7-16e5bd86acd0"

parser = argparse.ArgumentParser(description='Challenge 1 usage.')
parser.add_argument('server', nargs='?', default='web')
parser.add_argument('--username', nargs='?', dest='username', required=True, help="Your Cloud Username")
parser.add_argument('--password', nargs='?', dest='password', required=True, help="Your Cloud API Key")
args = parser.parse_args()

for i in range(1,4):
	servers.append(args.server + str(i))

pyrax.set_credentials(args.username,args.password)

cs = pyrax.cloudservers

print "The following servers will be created: " + ", ".join(servers)

for i in servers:
	print "Starting... ", i
	created = cs.servers.create(i, img, flv)

	while not cs.servers.get(created.id).accessIPv4:
		sys.stdout.write('.')
		sys.stdout.flush()
		time.sleep(30)
	newPassword = created.adminPass
	newIP = cs.servers.get(created.id).accessIPv4
	print "\nAdmin password: ", str(newPassword)
	print "Server IPs: ", str(newIP)
