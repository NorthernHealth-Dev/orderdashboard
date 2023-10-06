#!/Python311/python.exe
import cgitb;
cgitb.enable(display=1)
import cgi
from collections import defaultdict
import json
import os
import random
import string
#from urllib.parse import unquote
form = cgi.FieldStorage()

def ShowPage(tpage, tfields):

	tfile = "main.html"
	if tpage == "login":
		tfile = "index.html"
		
	tHTML = ""
	with open(tfile, "r") as infile:
		for line in infile:
			tHTML += line
	infile.close()
	
	for tid in tfields:
		tHTML = tHTML.replace(tid, tfields[tid])
	
	return tHTML

def GetRandomID(N):

	#N = 20
	res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
	
	return res

# Main
tmode = ""
tuser = ""
tpass = ""
sessionid = ""
if "mode" in form:
	tmode = form.getvalue("mode")
if "data" in form:
	tdata = form.getvalue("data")
if "id" in form:
	tid = form.getvalue("id")
if "username" in form:
	tuser = form.getvalue("username")
if "password" in form:
	tpass = form.getvalue("password")
if "sessionid" in form:
	sessionid = form.getvalue("sessionid")

if tmode == "test":
	print("Content-type: text/html")
	print()
	print("<br>Hello.")
	print("<br>Mode: " + tmode)

if tmode == "showchat":

	tfile = tid + '.chat.json'
	if not os.path.isfile(tfile):
	
		# showMsg(tid, ttitle, ttype, tby, tto, tdate, tmessage)
		tjson = {"chat": [ {"title": "Hello", "type": "message", "id": 1, "from": "Andrew", "to": "everyone", "message": "this is a test message", "date": "2023-4-27"} ]}
		
		f = open(tfile, "w")
		f.write(json.dumps(tjson))
		f.close()
	
	ojson = ''
	with open(tfile, "r") as infile:
		for line in infile:
			ojson += ojson + line
	infile.close()

	print("Content-type: text/html")	
	print()
	print(ojson)

if tmode == "savechat":

	tfile = tid + '.chat.json'
	odata = unquote(tdata)
	ojdata = json.loads(odata)

	# load data and append json
	ojson = ''
	with open(tfile, "r") as infile:
		for line in infile:
			ojson += ojson + line
	infile.close()
	jdata = json.loads(ojson)
	jdata["chat"].append(ojdata)
	
	# write out appended json
	f = open(tfile, "w")
	f.write(json.dumps(jdata))
	f.close()
	
if tmode == "savedata":
	print("Content-type: text/html")
	print()
	print("<br>Display JSON")
	print("<br>JSON: " + tdata)
	ndata = json.loads(tdata)
	tid = ndata['id']

	# Opening JSON file
	f = open('order.json')
	data = json.load(f)
	for i in range(0, len(data['ordersets'])):		
		if data['ordersets'][i]['id'] == tid:
			for tid in ndata:
				data['ordersets'][i][tid] = ndata[tid]
	f.close()

	# update content in main file
	f = open("order.json", "w")
	f.write(json.dumps(data))
	f.close()

if tmode == "showdata":

	ojson = ''
	with open("order.json", "r") as infile:
		for line in infile:
			ojson += ojson + line
	infile.close()

	print("Content-type: text/html")	
	print()
	print(ojson)

if tmode == "login":

	print("Content-type: text/html")	
	print()
	print("Logged In")
	

if tmode == "loginold":

	tfields = defaultdict(str)
	f = open('users.json.py', 'r')
	data = json.load(f)
	f.close()

	uname = ""
	login_status = False
	tread_only = False
	for i in range(0, len(data['users'])):		
		if data['users'][i]['username'] == tuser:
			if data['users'][i]['password'] == tpass:
				uname = data['users'][i]['name']
				login_status = True
				if data['users'][i]['usertype'] == "true":
					tread_only = True
	f.close()

	if (login_status == False):
		tHTML = ShowPage("login")

		# write page
		print("Content-type: text/html")	
		print()
		print(tHTML)

	if (login_status == True):
	
		# update users
		sessionid = GetRandomID(20)
		f2 = open('sessions.json.py', 'r')
		data2 = json.load(f2)
		f2.close()

		newsession = {}
		tfound = False
		for i in range(0, len(data2['sessions'])):
			if data2['sessions'][i]['username'] == tuser:
				data2['sessions'][i]['id'] = sessionid
				tfound = True
		if (tfound == False):
			newsession = {"username": tuser, "id": sessionid}
			data2['sessions'].append(newsession)

		# update content in main file
		f = open("sessions.json.py", "w")
		f.write(json.dumps(data2))
		f.close()
		
		# write page
		#tHTML = "<html><meta http-equiv=\"Refresh\" content=\"0; url=\'main.py?mode=showmain&sessionid=" + sessionid + "\'\" /></html>"
		#tHTML = "Login: success"
		#print("Content-type: text/html")	
		#print()
		#print(tHTML)

		# write out page
		tfields = defaultdict(str)
		tfields['[sessionid]'] = sessionid
		tfields['[name]'] = uname
		tHTML = ShowPage("main", tfields)

		# write page
		print("Content-type: text/html")	
		print()
		print(tHTML)
		#print("Mode: " + tmode)
		#print("Session ID: " + sessionid)
		
if tmode == "showmain":

	# write out page
	tfields = defaultdict(str)
	tfields['[sessionid]'] = sessionid
	tHTML = ShowPage("main", tfields)

	# write page
	print("Content-type: text/html")	
	print()
	print(tHTML)
	#print("Mode: " + tmode)
	#print("Session ID: " + sessionid)
	

if tmode == "logout":

	f = open('sessions.json.py')
	data = json.load(f)
	tfound = False
	tindex = -1
	for i in range(0, len(data['sessions'])):
		if data['sessions'][i]['id'] == sessionid:
			tfound = True
			tindex = i
	if (tfound == True):
		data['sessions'].pop(i)

	# update content in main file
	f = open("sessions.json.py", "w")
	f.write(json.dumps(data))
	f.close()

	# write page
	#tHTML = "<html><meta http-equiv=\"Refresh\" content=\"1; url=\'main.py?mode=showlogin\'\" /></html>"
	tHTML = "<html><body><script>window.location = 'main.py?mode=showlogin';</script></body></html>"
	#tHTML = "Login: success"
	print("Content-type: text/html")	
	print()
	print(tHTML)
	
	
if tmode == "showlogin":

	# write out page
	tfields = defaultdict(str)
	tfields['[sessionid]'] = "logout"
	tHTML = ShowPage("login", tfields)

	print("Content-type: text/html")	
	print()
	print(tHTML)

if tmode == "userlist":

	tfields = defaultdict(str)
	f = open('users.json.py', 'r')
	data = json.load(f)
	f.close()

	user_list = {"users": []}
	login_status = False
	tread_only = False
	for i in range(0, len(data['users'])):		
		name_item = {"name": data['users'][i]['name']}
		user_list["users"].append(name_item)
	f.close()

	tjson = json.dumps(user_list)
	print("Content-type: text/html")	
	print()
	print(tjson)

if tmode == "checksession":

	f = open('sessions.json.py')
	data = json.load(f)
	tfound = False
	tindex = -1
	for i in range(0, len(data['sessions'])):
		if data['sessions'][i]['id'] == sessionid:
			tfound = True
			tindex = i

	print("Content-type: text/html")	
	print()
	tjson = '{"sessionid": "na"}'
	if tfound == True:
		tjson = '{"sessionid": "' + sessionid + '"}'
	print(tjson)
	
	