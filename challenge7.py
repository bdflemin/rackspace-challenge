#!/usr/bin/python
import pyrax, sys, argparse, time

servers = []
flv = 2
img = "c195ef3b-9195-4474-b6f7-16e5bd86acd0"

parser = argparse.ArgumentParser(description='Challenge 7 usage.')
parser.add_argument('--server', nargs='?', dest="server", required=True, help="The Cloud Server Name")
parser.add_argument('--lb', nargs='?', dest="lb", required=True, help="The Cloud Server Name")
parser.add_argument('--username', nargs='?', dest='username', required=True, help="Your Cloud Username")
parser.add_argument('--password', nargs='?', dest='password', required=True, help="Your Cloud API Key")
args = parser.parse_args()

for i in range(1,3):
	servers.append(args.server + str(i))

pyrax.set_credentials(args.username,args.password)

cs = pyrax.cloudservers
clb = pyrax.cloud_loadbalancers

lbid = [i.id for i in clb.list() if str(i.name) == args.lb]

if not lbid:
	print "The loadbalancer you requested doesn't exist. Please try again."
	sys.exit()
else:
	lb = clb.get(lbid[0])

print "The following servers will be created: " + ", ".join(servers)

for i in servers:
	print "Starting... ", i
	created = cs.servers.create(i, img, flv)

	while cs.servers.get(created.id).status != "ACTIVE":
		sys.stdout.write('.')
		sys.stdout.flush()
		time.sleep(10)
	private_ip = str(cs.servers.get(created.id).networks["private"][0])
	if lb.add_nodes(clb.Node(address=private_ip, port=80, condition="ENABLED")):
		print "\nThe server", i, "has been created and added to the loadbalancer", args.lb