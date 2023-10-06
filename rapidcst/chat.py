#!/usr/bin/python
import cgitb;
import cgi
from collections import defaultdict
import json
import os
import random
import string
form = cgi.FieldStorage()

current_working_directory = os.getcwd()

def LoadChatData(tid):

	tfile = tid + '.chat.json'
	if not os.path.isfile(tfile):
		tjson = {"chat": [ {"title": "Hello", "type": "message", "id": 1, "from": "Andrew", "to": "Andrew", "message": "This is a test message", "date": "2023-04-27"} ]}

		f = open(tfile, "w")
		f.write(json.dumps(tjson))
		f.close()

	ojson = ''
	with open(tfile, "r") as infile:
		ojson = infile.read()
		#for line in infile:
		#	ojson += ojson + line
	infile.close()

	return ojson

def LoadAllergy():

	ojson = ""
	tfile = 'allergy.chat.json'
	with open(tfile, "r") as infile:
		ojson = infile.read()
	infile.close()
	#ojson = ojson.replace("\\u00a0", "");
	tfile = "file missing"

	return ojson

def ShowPage(tpage, tfields):

	tfile = "chatpage.html"
	if tpage == "login":
		tfile = "index.html"
		
	tHTML = ""
	with open(tfile, "r") as infile:
		tHTML = infile.read()
		#for line in infile:
		#	tHTML += line
	infile.close()
	
	for tid in tfields:
		tHTML = tHTML.replace('{%' + tid + '%}', tfields[tid])
	
	return tHTML

def SaveChatData(tdata, tid):

	tfile = tid + '.chat.json'
	uridata = [' ', '!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@']
	uricodes = ['%20', '%21', '%22', '%23', '%24', '%25', '%26', '%27', '%28', '%29', '%2A', '%2B', '%2C', '%2D', '%2E', '%2F', '%3A', '%3B', '%3C', '%3D', '%3E', '%3F', '%40']
	for x in range(0, len(uridata)):
		tdata = tdata.replace(uricodes[x], uridata[x])

	odata = tdata
	ojdata = json.loads(odata)

	ojson = ''
	with open(tfile, "r") as infile:
		for line in infile:
			ojson += ojson + line
	infile.close()
	jdata = json.loads(ojson)
	jdata["chat"].append(ojdata)

	print("Content-type:text/html\r\n\r\n")	
	print(tfile)

	f = open(tfile, "w")
	f.write(json.dumps(jdata))
	f.close()
	

# main
tmode = "test"
tuser = ""
tpass = ""
sessionid = ""
ttitle = ""
tid = ""
tdata = ''
if "mode" in form:
	tmode = form.getvalue("mode")
if "title" in form:
	ttitle = form.getvalue("title")
if "id" in form:
	tid = form.getvalue("id")
if "data" in form:
	tdata = form.getvalue("data")

if tmode == "test":
	tfields = defaultdict(str)
	tHTML = ShowPage("main", tfields)
	print("Content-type:text/html\r\n\r\n")	
	print(current_working_directory)

if tmode == "chat":
	tfields = defaultdict(str)
	tfields["title"] = ttitle
	tfields["id"] = tid
	tHTML = ShowPage("chat", tfields)
	print("Content-type:text/html\r\n\r\n")	
	print(tHTML)

if tmode == "show":
	tjson = LoadChatData(tid)
	print("Content-type:text/html\r\n\r\n")	
	print(tjson)

if tmode == "save":
	SaveChatData(tdata, tid)

if tmode == "allergy":
	tjson = LoadAllergy()
	print("Content-type:text/html\r\n\r\n")	
	print(tjson)

