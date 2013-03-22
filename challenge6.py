#!/usr/bin/python
import pyrax, sys, argparse, os

parser = argparse.ArgumentParser(description='Challenge 3 usage.')
parser.add_argument('--container', nargs='?', dest='container', required=True, help="Cloud Files Container Name")
parser.add_argument('--username', nargs='?', dest='username', required=True, help="Your Cloud Username")
parser.add_argument('--password', nargs='?', dest='password', required=True, help="Your Cloud API Key")
args = parser.parse_args()

pyrax.set_credentials(args.username,args.password)

cf = pyrax.cloudfiles

if [i for i in cf.list_containers() if i == args.container]:
	cont = cf.get_container(args.container)
	cont.make_public(ttl=900)
	print "The container", cont.name, "is now public."
	print "TTL = 900"
else:
	print "The container doesn't exist.. please try again"
