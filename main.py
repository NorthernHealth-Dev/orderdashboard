#!/usr/bin/python
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
tdata = ""
tid = ""
sessionid = ""
if "mode" in form:
	tmode = form.getvalue("mode")
if "data" in form:
	tdata = form.getvalue("data")
if "id" in form:
	tid = form.getvalue("id")

if tmode == "test":
	print("Content-type: text/html")
	print()
	print("<br>Hello.")
	print("<br>Mode: " + tmode)
	
if tmode == "savedata":

	# convert data from URI encoding
	uridata = [' ', '!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@']
	uricodes = ['%20', '%21', '%22', '%23', '%24', '%25', '%26', '%27', '%28', '%29', '%2A', '%2B', '%2C', '%2D', '%2E', '%2F', '%3A', '%3B', '%3C', '%3D', '%3E', '%3F', '%40']
	for x in range(0, len(uridata)):
		tdata = tdata.replace(uricodes[x], uridata[x])

	ndata = json.loads(tdata)
	tid = ndata['ID']

	# Opening JSON file
	idfound = False
	f = open("maindata.js", "r")
	data = json.load(f)
	for i in range(0, len(data)):		
		if data[i]['ID'] == tid:
			idfound = True
			for tid in ndata:
				data[i][tid] = ndata[tid]
	f.close()
	
	if idfound == False:
		data.append(ndata)

	# update content in main file
	f = open("maindata.js", "w")
	f.write(json.dumps(data))
	f.close()

	print("Content-type: text/html\r\n\r\n")
	print(json.dumps(data, indent=1))

if tmode == "download":

	# Opening JSON file
	f = open("maindata.js", "r", encoding="utf-8")
	data = json.load(f)
	f.close()

	collist = defaultdict(int)
	tcsv = ""
	for x in range(0, len(data)):
		for tcol in data[x]:
			collist[tcol] = 1
			
	tsep = ','
	tline = ""
	for tcol in collist:
		tline += tcol + tsep
	tline = tline.strip() + "\n"
	tcsv += tline
	for x in range(0, len(data)):
		tline = ""
		for tcol in collist:
			tline += data[x][tcol] + tsep
		tline = tline.strip() + "\n"
		tcsv += tline

	print("Content-Type: text/csv\n")
	#print("Content-Disposition: attachment; filename=electronic_orders.csv\n")
	#print('"Content-Transfer-Encoding": "bytes"' + "\n")
	print(tcsv)
	#print(json.dumps(data, indent=1))
	#print('{"result": "' + str(idfound) + '"}')
	#print('{"result": "' + str(idfound) + '"}' + "<br>" + tstr)
	
if tmode == "del":

	# Opening JSON file
	f = open("maindata.js", "r")
	data = json.load(f)
	f.close()

	# delete record
	idfound = False
	nid = 0
	tstr = ""
	tdel = 0
	for x in range(0, len(data)):
		#tstr += '<br>' + data[x]['ID'] + "\t" + tid
		if data[x]['ID'] == tid:
			idfound = True
			tdel = nid
			#data.pop(nid)
		nid += 1

	if idfound == True:
		data.pop(tdel)

	# update content in main file
	f = open("maindata.js", "w")
	f.write(json.dumps(data, indent=1))
	f.close()

	print("Content-type: text/html\r\n\r\n")
	#print('{"result": "' + true + '"}')

	print(json.dumps(data, indent=1))
	#print('{"result": "' + str(idfound) + '"}')
	#print('{"result": "' + str(idfound) + '"}' + "<br>" + tstr)

if tmode == "showdata":

	ojson = ''
	with open("maindata.js", "r") as infile:
		for line in infile:
			ojson += ojson + line
	infile.close()

	print("Content-type: text/html")	
	print()
	print(ojson)
		
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
	