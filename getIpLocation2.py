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
	return records
	f.close()

def getIps(filename):
	records = getRecords(filename)
	ips = []
	for record in records:
		for i in record["body"]:
			if "appCommunications" in i:
				if i["appCommunications"]["applicationNames"] == "Eyeplus":
					ips.append(i["appCommunications"]["daddr"])
	return ips

def getIpLocations(filename):
	ips = getIps(filename)
	ip = ips[len(ips)-1]
	#print ("\n"+ip)
	ipLocations = []
	f = open("ipLocations.txt","w+")
	f.write("[\n")
	driver = webdriver.Firefox()
	for ip in ips:
		driver.get("https://tools.keycdn.com/geo?host=%s"%ip)
		html = driver.page_source
		soup = BeautifulSoup(html, 'html.parser')
		row = soup.find('table', {"class": "table table-sm table-hover mt-4"} )
		tds = row.findChildren("td",recursive=True)
		ths = row.findChildren("th",recursive=True)
		tds[3].span.extract()
		ipLocation = dict()
		count = 0
		for th in ths:
			ipLocation[th.string]=tds[count].string	
			count+=1
		f.write(json.dumps(ipLocation)+",")
		ipLocations.append(ipLocation)
	f.close()
	os.system("sed -i '$ s/.$/]/' %s"%"ipLocations.txt")#substitui a ultima virgula por "]"
	driver.close()
	return ipLocations
getIpLocations("insane_test-2019-05-25.json")
#transformToJsonList("insane_test-2019-05-25.json")
