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

import pyrax, sys, argparse, os

parser = argparse.ArgumentParser(description='Challenge 3 usage.')
parser.add_argument('--container', nargs='?', dest='container', required=True, help="Cloud Files Container Name")
parser.add_argument('--username', nargs='?', dest='username', required=True, help="Your Cloud Username")
parser.add_argument('--password', nargs='?', dest='password', required=True, help="Your Cloud API Key")
parser.add_argument('PATH', nargs='?', required=True)
args = parser.parse_args()

pyrax.set_credentials(args.username,args.password)

cf = pyrax.cloudfiles

if os.path.isdir(args.PATH):
	print "Starting the upload of the content in", args.PATH, "to the container", args.container
	upload_key, total_bytes = cf.upload_folder(args.PATH, container=args.container)
	print "Upload key:", upload_key
	print "Total bytes:", total_bytes
else:
	print "Its not a directory... Please select a directory for this challenge"
	sys.exit()
