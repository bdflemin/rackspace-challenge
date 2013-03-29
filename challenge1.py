#!/usr/bin/python
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

	while not cs.servers.get(created.id).networks:
		sys.stdout.write('.')
		sys.stdout.flush()
		time.sleep(10)
	newPassword = created.adminPass
	newIP = cs.servers.get(created.id).networks['public']
	print "\nAdmin password: ", newPassword
	print "Server IPs: ", str([i for i in newIP if i.find('.') > -1][0])