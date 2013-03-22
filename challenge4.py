#!/usr/bin/python
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