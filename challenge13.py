#!/usr/bin/python
import pyrax, sys, argparse, time

parser = argparse.ArgumentParser(description='Challenge 13 usage.')
parser.add_argument('--username', nargs='?', dest='username', required=True, help="Your Cloud Username")
parser.add_argument('--password', nargs='?', dest='password', required=True, help="Your Cloud API Key")
args = parser.parse_args()

try:
	pyrax.set_credentials(args.username,args.password)
except:
	print "username or apikey doesn't work, try again."
	sys.exit()

cs = pyrax.cloudservers
clb = pyrax.cloud_loadbalancers
cbs = pyrax.cloud_blockstorage
cf = pyrax.cloudfiles
cn = pyrax.cloud_networks
cdb = pyrax.cloud_databases

def cleanServers():
	for img in cs.images.list():
		if str(img.metadata["image_type"]) == "snapshot":
			print "Deleting saved image:", img.name
			img.delete()

	for server in cs.servers.list():
		print "Deleting server:", server
		server.delete()
		time.sleep(5)

def cleanFiles():
	for cont in cf.get_all_containers():
		print "Deleting all objects in", cont.name
		cont.delete_all_objects()
		print "Deleting the container", cont.name
		cont.delete()
		time.sleep(5)

def cleanDatabases():
	for db in cdb.list():
		print "Deleting database:", db.name
		db.delete()
		time.sleep(5)

def cleanNetworks():
	for net in cn.list():
		if str(net.name) != "public" and str(net.name) != "private":
			print "Deleting Network:", net.name
			net.delete()

	for lb in clb.list():
		print "Deleting Loadbalancer:", lb.name
		lb.delete()

def cleanBlockStorage():
	for vol in cbs.list():
		print "Detaching Block Storage:", vol.name
		vol.detach()
		print "Deleting Block Storage:", vol.name
		vol.delete()
		time.sleep(5)

print "Starting cleanup..."
cleanBlockStorage()
cleanServers()
cleanFiles()
cleanDatabases()
cleanNetworks()