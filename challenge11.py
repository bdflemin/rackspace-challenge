#!/usr/bin/python
import pyrax, sys, argparse, time

parser = argparse.ArgumentParser(description='Challenge 11 usage.')
parser.add_argument('--certfile', nargs='?', dest='cert', required=True, help="Self Signed Cert File")
parser.add_argument('--pkfile', nargs='?', dest='pk', required=True, help="Private Key File")
parser.add_argument('--username', nargs='?', dest='username', required=True, help="Your Cloud Username")
parser.add_argument('--password', nargs='?', dest='password', required=True, help="Your Cloud API Key")
args = parser.parse_args()

pyrax.set_credentials(args.username,args.password)

cs = pyrax.cloudservers
clb = pyrax.cloud_loadbalancers
cdns = pyrax.cloud_dns
cbs = pyrax.cloud_blockstorage
cnw = pyrax.cloud_networks

flv = 2
img = "c195ef3b-9195-4474-b6f7-16e5bd86acd0"
cert = open(args.cert,'r').read()
pk = open(args.pk,'r').read()
private_net = cnw.create("challenge_priv", cidr="192.168.0.0/24")

print "Creating 3 servers named server1, server2, and server3"
server1 = cs.servers.create("server1", img, flv, networks=private_net.get_server_networks(public=True, private=True))
server2 = cs.servers.create("server2", img, flv, networks=private_net.get_server_networks(public=True, private=True))
server3 = cs.servers.create("server3", img, flv, networks=private_net.get_server_networks(public=True, private=True))

while cs.servers.get(server1.id).accessIPv4 and not cs.servers.get(server2.id).accessIPv4 and not cs.servers.get(server3.id).accessIPv4:
	sys.stdout.write('.')
	sys.stdout.flush()
	time.sleep(30)

print "\n--------\nServer1 Admin password: ", str(server1.adminPass)
print "Server1 Public IP: ", str(cs.servers.get(server1.id).accessIPv4)
print "--------\nServer2 Admin password: ", str(server2.adminPass)
print "Server2 Public IP: ", str(cs.servers.get(server2.id).accessIPv4)
print "--------\nServer3 Admin password: ", str(server3.adminPass)
print "Server3 Public IP: ", str(cs.servers.get(server3.id).accessIPv4)

# Create cloud storage for the three servers
print "--------\nAttaching cloud block storage to server1, server2, and server3"
try:
	vol1 = cbs.create(name="server1_vol", size=100, volume_type="SATA")
	vol2 = cbs.create(name="server1_vol", size=100, volume_type="SATA")
	vol3 = cbs.create(name="server1_vol", size=100, volume_type="SATA")
	vol1.attach_to_instance(server, mountpoint="/dev/xvdb")
	vol2.attach_to_instance(server, mountpoint="/dev/xvdb")
	vol3.attach_to_instance(server, mountpoint="/dev/xvdb")
except:
	print "Problem with making the volumes:", sys.exc_info()[0]
	sys.exit()

# Create the nodes and vip for the LB
server1_ip = cs.servers.get(server1.id).networks["private"][0]
server2_ip = cs.servers.get(server2.id).networks["private"][0]
server3_ip = cs.servers.get(server3.id).networks["private"][0]
node1 = clb.Node(address=server1_ip, port=80, condition="ENABLED")
node2 = clb.Node(address=server2_ip, port=80, condition="ENABLED")
node3 = clb.Node(address=server3_ip, port=80, condition="ENABLED")
vip = clb.VirtualIP(type="PUBLIC")

# Create LB using nodes from above
lb = clb.create("challenge10", port=80, protocol="HTTP", nodes=[node1,node2,node3], virtual_ips=[vip])
while str(clb.get(lb.id).status) != "ACTIVE":
	time.sleep(10)

# Enable SSL Traffic on LB (see above variables)
lb.add_ssl_termination(securePort=443, enabled=True, secureTrafficOnly=False, certificate=cert, privatekey=pk,)