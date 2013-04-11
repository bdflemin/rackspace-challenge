#!/usr/bin/python
import pyrax, sys, argparse, time

parser = argparse.ArgumentParser(description='Challenge 10 usage.')
parser.add_argument('--sshkey', nargs='?', dest='sshkey', required=True, help="The public key file")
parser.add_argument('--errorpage', nargs='?', dest='errorpage', required=True, help="Custom Error Page")
parser.add_argument('--username', nargs='?', dest='username', required=True, help="Your Cloud Username")
parser.add_argument('--password', nargs='?', dest='password', required=True, help="Your Cloud API Key")
args = parser.parse_args()

pyrax.set_credentials(args.username,args.password)

cs = pyrax.cloudservers
clb = pyrax.cloud_loadbalancers
cdns = pyrax.cloud_dns
cf = pyrax.cloudfiles

flv = 2
img = "c195ef3b-9195-4474-b6f7-16e5bd86acd0"
ssh = open(args.sshkey,'r').read()
error = open(args.errorpage,'r').read()
sshFile = {"/root/.ssh/authorized_keys": str(ssh)}

print "Creating 2 servers named server1 and server2"
server1 = cs.servers.create("server1", img, flv, files=sshFile)
server2 = cs.servers.create("server2", img, flv, files=sshFile)
while not cs.servers.get(server1.id).accessIPv4 and not cs.servers.get(server2.id).accessIPv4:
	sys.stdout.write('.')
	sys.stdout.flush()
	time.sleep(30)
print "\nserver1 =", server1.adminPass
print "server2 =", server2.adminPass

### After servers are done, make LB nodes using server's private IPs
print ".........."
print "Starting the Loadbalancer process"
server1_ip = cs.servers.get(server1.id).networks["private"][0]
server2_ip = cs.servers.get(server2.id).networks["private"][0]
node1 = clb.Node(address=server1_ip, port=80, condition="ENABLED")
node2 = clb.Node(address=server2_ip, port=80, condition="ENABLED")
vip = clb.VirtualIP(type="PUBLIC")
### Create LB with new nodes
lb = clb.create("challenge10", port=80, protocol="HTTP", nodes=[node1,node2], virtual_ips=[vip])
while str(clb.get(lb.id).status) != "ACTIVE":
	time.sleep(10)
### Create a health check
print "\nCreating a LB health monitor"
lb.add_health_monitor(type="CONNECT", delay=10, timeout=10, attemptsBeforeDeactivation=3)
### Make customer error page
time.sleep(30)
print "Updating the error page"
lb.set_error_page(error)
### Make a new FQDN/A-Record for new VIP
print "Making a new A-Record using the vip"
lbip = str(clb.get(lb.id).virtual_ips[0].address)
dom = cdns.create(name="rackspace-challenge.com",emailAddress="challenge10@rackspace.com",ttl=600)
dom.add_record([{"type": "A", "name": "rackspace-challenge.com", "data": lbip, "ttl": 6000}])
### Backup error file to files
print "Backing up the error page in cloud files"
cf.create_container("challenge10_bk")
obj = cf.store_object("challenge10_bk", "error.html", error)
print "\nChallenge Complete\n"