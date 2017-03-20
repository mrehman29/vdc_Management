#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Copyright (c) 2017-2018 Muhammad Rehman <muhammad@rehman.cf> All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

  1. Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.
   
  2. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in
     the documentation and/or other materials provided with the
     distribution.

  3. Neither the name of Infrae nor the names of its contributors may
     be used to endorse or promote products derived from this software
     without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL INFRAE OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''


from __future__ import print_function
import os
try:
	from boto3.session import Session
	import boto3
except:
	print("Installing and Updating Libs.")
	os.system("python get-pip.py")
	os.system("pip install boto3")
	os.system("pip install requests")
	from boto3.session import Session
        import boto3	
import vdc_api as vdc
import getpass
import json
import os

global region, api_key, sec_key, oapi_key, osec_key

api_url="https://myservices.interoute.com/myservices/api/vdc"
oapi_url="https://s3-eu.object.vdc.interoute.com/"

home = os.getenv("HOME")
file_name = home+"/.API_MGMT"

function_list = ["Clone VM", "Deploy VM", "Rename VM", "Upload ISO/Template", "Stop VM", "Start VM", "VM Volumes", "Create Template", "Create Snapshot", "Create Network", "Copy Template", "Volume From Snapshot", "Other VDC"]
function_with_s3 = [3, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0]
def List_Functions():
	c_class = __import__("Select_Region")
	global region
        region = getattr(c_class, "Select_Region")("")
	for x in range(1, len(function_list)+1):
		print(str(x) + " " + function_list[x-1])
	Truee = True
	while(Truee):
		sel_Fun = raw_input('Select Function ')
		try:
			sel_Fun = int(sel_Fun)
			if (sel_Fun < len(function_list)+1 and sel_Fun > 0):
				print("Function Selected: "+ function_list[sel_Fun-1])
				Truee = False
				return sel_Fun-1
				break
			else:
				print("Number should be between 1 and " + str(len(function_list)) )
		except:
			print("Invalid Number Try Again")

def Exec_Function(f_num):
	#print("to call function " + function_list[f_num])
	process_to_call = function_list[f_num].replace(" ","_")
	process_to_call = process_to_call.replace("/","_")
	api = vdc.VDCApiCall(api_url, api_key, sec_key)
	if (function_with_s3[f_num]==1):
		session = Session(aws_access_key_id=oapi_key,aws_secret_access_key=osec_key)
        	s3 = session.resource('s3', endpoint_url=oapi_url)
		api = [api, s3]
	if(function_with_s3[f_num]==2):
		session = Session(aws_access_key_id=oapi_key,aws_secret_access_key=osec_key)
                s3 = session.resource('s3', endpoint_url=oapi_url)
		client = session.client('s3', endpoint_url=oapi_url)
                api = [api, s3, client]
	if(function_with_s3[f_num]==3):
		api = [api_url, api_key, sec_key]
	c_class = __import__(process_to_call)
        call = getattr(c_class, process_to_call)(api,region)
	#print (call)
	#request = {'available': 'true'}
	#result = api.listZones(request)
	#for zone in result['zone']:
        #	print('%s: %s' % (zone['id'], zone['name']))
	c =raw_input("Do you want to call another function Y/N: ")
	if (c == "Y" or c=="y"):
		Exec_Function(List_Functions())
def Read_API():
	global api_key, sec_key, oapi_key, osec_key
	file = open(file_name,"r")
        api_key=((file.readline()).replace("\n","")).split("=")[1]
        sec_key=((file.readline()).replace("\n","")).split("=")[1]
        oapi_key=((file.readline()).replace("\n","")).split("=")[1]
        osec_key=((file.readline()).replace("\n","")).split("=")[1]
	function = List_Functions()
        Exec_Function(function)

def Interoute_VDC():
	if (os.path.exists(file_name)):
		Read_API()
	else:
		print ("**********API Keys Not Set**********")
		print ("*****Use api_setup to set APIs******")
		print ("************************************")
		#api_key=raw_input("Enter VDC API Key: ")
		#sec_key=raw_input("Enter VDC Secret Key: ")
		#function = List_Functions()
		#Exec_Function(function)
		os.system("api_setup")
		Read_API()

