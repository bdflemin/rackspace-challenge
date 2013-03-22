#!/usr/bin/python
import pyrax, sys, argparse, os

parser = argparse.ArgumentParser(description='Challenge 3 usage.')
parser.add_argument('--container', nargs='?', dest='container', required=True, help="Cloud Files Container Name")
parser.add_argument('--username', nargs='?', dest='username', required=True, help="Your Cloud Username")
parser.add_argument('--password', nargs='?', dest='password', required=True, help="Your Cloud API Key")
parser.add_argument('PATH', nargs='?')
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