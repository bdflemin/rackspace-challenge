#!/usr/bin/python
import pyrax, sys, argparse, time

parser = argparse.ArgumentParser(description='Challenge 2 usage.')
parser.add_argument('--uuid', nargs='?', dest='uuid', required=True, help="Servers UUID Information")
parser.add_argument('--username', nargs='?', dest='username', required=True, help="Your Cloud Username")
parser.add_argument('--password', nargs='?', dest='password', required=True, help="Your Cloud API Key")
args = parser.parse_args()

pyrax.set_credentials(args.username,args.password)

cs = pyrax.cloudservers
try:
	server = cs.servers.get(args.uuid)
except:
	print "The uuid doesn't exist, please try again."
	sys.exit()

status = ""
epoch = int(time.time())
sName = str(server.name)
sFlavor = str(server.flavor['id'])
imgID = cs.servers.create_image(args.uuid, sName+"_"+str(epoch))

print "Starting challenge 2 now..."
while str(status) != "ACTIVE":
	sys.stdout.write('.')
	sys.stdout.flush()
	status = "".join([i.status for i in cs.images.list() if str(i.id) == imgID])
	time.sleep(30)
print "\nThe new image has been created.\nImage ID: ", imgID, "\n"
print "Creating a new server named",sName+"_img"

created = cs.servers.create(sName+"_img", imgID, sFlavor)
while cs.servers.get(created.id).status != "ACTIVE":
	sys.stdout.write('.')
	sys.stdout.flush()
	time.sleep(30)
print "\nThe new server has been created successfully named", str(created.name)