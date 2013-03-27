#!/usr/bin/python
import pyrax, sys, argparse, time

servers = []
nodes = []
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

print "The following servers will be created: " + ", ".join(servers)

for i in servers:
	print "\nStarting... ", i
	created = cs.servers.create(i, img, flv)

	while cs.servers.get(created.id).status != "ACTIVE":
		sys.stdout.write('.')
		sys.stdout.flush()
		time.sleep(30)
	private_ip = str(cs.servers.get(created.id).networks["private"][0])
	nodes.append(clb.Node(address=private_ip, port=80, condition="ENABLED"))

vip = clb.VirtualIP(type="PUBLIC")
newlb = clb.create(args.lb, port=80, protocol="HTTP", nodes=[nodes[0], nodes[1]], virtual_ips=[vip])
print "\nStarting the loadbalancer named", args.lb

while str(clb.get(newlb.id).status) != "ACTIVE":
	sys.stdout.write('.')
	sys.stdout.flush()
	time.sleep(30)
print "\nLoadbalancer is now active and ready to use."