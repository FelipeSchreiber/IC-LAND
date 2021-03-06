import string 
import json
import os
import re
import requests
from bs4 import BeautifulSoup
import _pickle as pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import subprocess

def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except:
    return False
  return True

def transformToJsonList(filename):
	f = open(filename,"r+")
	f2 = open(filename+".txt",'w+')
	pattern = re.compile("(}\s*]\s*}\s*,+)")
	f2.write("[")
	for line in f:
		if not pattern.match(line):
			f2.write(line.replace("}]}","}]},"))
		else:
			f2.write(line)
	f.close()
	f2.close()
	os.system("sed -i '$ s/.$/]/' %s"%filename+".txt")
	if os.path.exists(filename):
		os.remove(filename)
		os.rename(filename+'.txt', filename)
	else:
		print("The file does not exist") 

def getRecords(filename):
	g = open(filename).read()
	if is_json(g):
		f = open(filename).read()
	else:
		transformToJsonList(filename)
		f = open(filename).read()
	records = json.loads(f)
	print ("records length: ",len(records))
	#exDict = {'exDict': records[19]}
	#with open('file.txt', 'w') as file:
	#	file.write(json.dumps(exDict))
	return records
	f.close()

def getIps(filename,app):
	records = getRecords(filename)
	ips = []
	for record in records:
		for i in record["body"]:
			if "appCommunications" in i:
				if i["appCommunications"]["applicationNames"] == app:
					ips.append(i["appCommunications"]["daddr"])
	return ips

def getIpLocations(filename,app):
	ips = set (getIps(filename,app) )
	#ip = ips[len(ips)-1]
	#print ("\n"+ip)
	ipLocations = []
	f = open("ipLocations_"+app+".txt","w+")
	f.write("[\n")
	driver = webdriver.Firefox()
	myPattern = re.compile('({.*?})')
	for ip in ips:
		driver.get("http://ip-api.com/json/%s"%ip)
		html = driver.page_source
		soup = BeautifulSoup(html, 'html.parser')
		Json = soup.find( text=myPattern )
		Json_str = str(Json)
		ipLocation = json.loads(Json_str)
		f.write(Json_str+",")
		ipLocations.append(ipLocation)
	f.close()
	os.system("sed -i '$ s/.$/]/' %s"%"ipLocations_"+app+".txt")#substitui a ultima virgula por "]"
	driver.close()
	return ipLocations
getIpLocations("insane_test-2019-06-13.json","Eyeplus")
#transformToJsonList("insane_test-2019-05-25.json")
