#!/usr/bin/python
import string, random, time, argparse, sys, pyrax, os

def rpassword():
	length = 13
	chars = string.ascii_letters + string.digits + '!@#$%^&*()'
	random.seed = (os.urandom(1024))
	return ''.join(random.choice(chars) for i in range(length))

parser = argparse.ArgumentParser(description='Challenge 5 usage.')
parser.add_argument('--dbname', nargs='?', dest='dbname', required=True, help="Database Name To Use")
parser.add_argument('--username', nargs='?', dest='username', required=True, help="Your Cloud Username")
parser.add_argument('--password', nargs='?', dest='password', required=True, help="Your Cloud API Key")
args = parser.parse_args()

pyrax.set_credentials(args.username,args.password)

cdb = pyrax.cloud_databases
print "\nStarting to create the database with the name of", args.dbname+"_instance"

inst = cdb.create(args.dbname+"_instance", flavor=1, volume=2)


while str(cdb.get(inst.id).status) != "ACTIVE":
	sys.stdout.write('.')
	sys.stdout.flush()
	time.sleep(10)

if inst:
	db = inst.create_database(args.dbname)
	print "\n\nThe new instance database was created successfully"
else:
	print "\n\nDatabase instance didn't work, exiting..."
	sys.exit()

print "\nNow I will be creating a user with the name of", args.username,"..."
newpassword = str(rpassword())
newuser = inst.create_user(name=args.username, password=newpassword, database_names=[db])

if newuser:
	print "----\nUser:",newuser.name
	print "Password:",newpassword