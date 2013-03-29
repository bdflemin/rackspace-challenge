#!/usr/bin/python
import pyrax, sys, argparse, os

parser = argparse.ArgumentParser(description='Challenge 8 usage.')
parser.add_argument('--domain', nargs='?', dest='domain', required=True, help="The Cloud DNS Domain to use")
parser.add_argument('--username', nargs='?', dest='username', required=True, help="Your Cloud Username")
parser.add_argument('--password', nargs='?', dest='password', required=True, help="Your Cloud API Key")
args = parser.parse_args()

pyrax.set_credentials(args.username,args.password)

cf = pyrax.cloudfiles
cdns = pyrax.cloud_dns

print "Checking domain..."
for d in cdns.get_domain_iterator():
	if str(d.name) == args.domain:
		print "... Domain exists, continuing with the challenge\n"
		dnsID = str(d.id)
		break
if
 not dnsID:
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
	rec = dom.add_records({"type": "CNAME", "name": "challenge8."+args.domain, "data": cont.cdn_uri, "ttl": 6000})
	print "... The CNAME", rec[0].name, "has been created without any issues. Challenge is complete."
except pyrax.exceptions.DomainRecordAdditionFailed:
	print "\nThe record of challenge8."+args.domain, "exists. Exiting challenge and please clean up containers and records."
	sys.exit()