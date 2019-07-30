from scapy.all import *
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

def getIps(filename):
	ips = []
	pkts = rdpcap(filename)
	for pkt in pkts:
		ip = pkt.sprintf("%IP.dst%")
		ips.append(ip)
	print(len(ips))
	return ips

def getIpLocations(filename):
	ips = set (getIps(filename) )
	ipLocations = []
	f = open("ipLocations_from_pcap_file_.txt","w+")
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
	os.system("sed -i '$ s/.$/]/' %s"%"ipLocations_from_pcap_file_.txt")#substitui a ultima virgula por "]"
	driver.close()
	return ipLocations

getIpLocations("camera_capture3.pcapng")    
