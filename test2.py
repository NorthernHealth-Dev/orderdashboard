#!/usr/bin/python
import cgitb;
import cgi
from collections import defaultdict
import json
import os
import random
import string

current_working_directory = os.getcwd()

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

# write page
tfields = defaultdict(str)
tHTML = ShowPage("main", tfields)
print("Content-type:text/html\r\n\r\n")	
#print("")
#print("Hello")
#print(current_working_directory)
print(tHTML)

