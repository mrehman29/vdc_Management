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
import thread,sys,time,pprint,getpass,json,os
import vdc_api as vdc

global api_url, api_key, sec_key
vol_attached = 0
def Clone_VM(api,region):
	global api_url, api_key, sec_key
	api_url = api[0]
	api_key = api[1]
	sec_key = api[2]
	confirm = raw_input("VM Will be POWERED-OFF during the process do you want to continue y/N: ")
	api = vdc.VDCApiCall(api_url, api_key, sec_key)
	if (confirm=="Y" or confirm=="y"):
		id_True = raw_input("Do you have VM ID Y/N: ")
		if (id_True=="Y" or id_True=="y"):
			Clone_by_id(api,region)
		elif (id_True=="N" or id_True=="n"):
			Clone_by_Selection(api,region)
		else:
			print("Invalid selection")
			Clone_VM(api,region)
	
def Clone_by_id(api,region):
	vmID = raw_input("Enter VM ID: ")
	if (len(vmID) == 36):
		req = {'available': 'true', 'region': region, 'id': vmID}
		c_class = __import__("Select_VM")
                vm_detail = getattr(c_class, "Select_VM_Details")(api,req)
		#print(vm_detail)
		if vm_detail == "error":
			print("Unable to fine VM with ID: "+ vmID+ " in Region:" + region)
			Clone_by_id(api,region)
		else:
			Dest_VM = Clone_VM_Details(api, region, vm_detail)
		#Rename(api,region,vmID)

	else:
		print("Invalid VM ID, Please check VM ID and try again")
                Clone_by_id(api,region)
		
def Clone_by_Selection(api,region):
	try:	
		c_class = __import__("Select_Zone")
		zone = getattr(c_class, "Select_Zone")(api,region)
		request = {'available': 'true', 'region': region, 'zoneid': zone["id"]}
		c_class = __import__("Select_VM")
                vm = getattr(c_class, "Select_VM")(api,request)
		req = {'available': 'true', 'region': region, 'id': vm["id"]}
                c_class = __import__("Select_VM")
                vm_detail = getattr(c_class, "Select_VM_Details")(api,req)
		if vm_detail == "error":
                        print("Unable to fine VM with ID: "+ vmID+ " in Region:" + region)
                        Clone_by_id(api,region)
                else:
                        Dest_VM = Clone_VM_Details(api, region, vm_detail)
	except Exception as e:
		print(e)
def Clone_VM_Details(api,region, VM_Details):
	all_Volumes = []
	print("*******New Clone VM Details**********")
	Dest_VM = {'available': 'true', 'region': region }
	c_class = __import__("Select_Zone")
        zone = getattr(c_class, "Select_Zone")(api,region)
	Dest_VM["zoneid"]=zone["id"]
	Dest_VM["name"]=raw_input("Enter New VM Name: ")
	Dest_VM["displayname"]=Dest_VM["name"]
	Dest_VM["serviceofferingid"]=VM_Details["serviceofferingid"]
	Dest_VM["ostypeid"]=VM_Details["ostypeid"]
	request = {'available': 'true', 'region': region, 'zoneid': zone["id"] }
	c_class = __import__("Select_Network")
	select_network = getattr(c_class, "Select_Network")(api,request)
	if select_network[1] != False:
		Dest_VM["ipaddress"] = select_network[1]
	Dest_VM["networkids"] = (select_network[0])["id"]
	Dest_VM["startvm"]=False
	request = {'available': 'true', 'region': region, 'id': VM_Details['id']}
	c_class = __import__("Stop_VM")
        stopping = getattr(c_class, "Stop_VM_Details")(api,request)
	if stopping =="error":
		print("Unable to Stop VM")
	else:
		req = {	'available': 'true','region' : region, 'virtualmachineid' : VM_Details["id"]}
		c_class = __import__("VM_Volumes")
		volumes = getattr(c_class, "VM_Volumes_Details")(api,req)
		if volumes == "error":
			print("Unable to get Volumes list")
		else:
			for res in volumes:
				if res["type"]=="ROOT":
					temp_name = res["name"]+"-Template"
					print("Creating Template: "+ temp_name)
					req = { 'available': 'true','region' : region, 'volumeid' : res["id"], 'ostypeid': VM_Details["ostypeid"], 'name': temp_name, 'displaytext': temp_name}
					api = vdc.VDCApiCall(api_url, api_key, sec_key)
					c_class = __import__("Create_Template")
					template = getattr(c_class, "Create_Template_Details")(api,req)
					if template == "error":
						print("Unable to Create Template ")
					else:
						Dest_VM["templateid"]= template["id"]
						#print("Copying Template to Destination Zone "+ zone["name"])
						#req ={'available': 'true', 'region': region, 'id': template["id"], 'destzoneid': Dest_VM["zoneid"], 'sourcezoneid': VM_Details["zoneid"]} 
						#c_class = __import__("Copy_Template")
                                        	#copy = getattr(c_class, "Copy_Template_Details")(api,req)
						#Dest_VM["templateid"]= copy["id"]
						#print("Template Copied to Destination, Going to Deploy new VM")	
				else:
					print("Creating Snapshot for Volume "+ res["name"])
					api = vdc.VDCApiCall(api_url, api_key, sec_key)
					req = { 'available': 'true','region' : region, 'volumeid' : res["id"], 'name': res["name"]+"-Snap"}
					c_class = __import__("Create_Snapshot")
					volume = getattr(c_class, "Create_Snapshot_Details")(api,req,True)
					all_Volumes.append(volume)
					
		print("Going to Start Originl VM")
		try:
			time.sleep(5)
			api = vdc.VDCApiCall(api_url, api_key, sec_key)
			c_class = __import__("Start_VM")
			thread.start_new_thread(start_thread, (c_class, "Start_VM_Details", api,request, True ) )
		except:
			print("Error: unable to start thread")
		
		req ={'available': 'true', 'region': region, 'id': template["id"], 'destzoneid': Dest_VM["zoneid"], 'sourcezoneid': VM_Details["zoneid"]}
		api = vdc.VDCApiCall(api_url, api_key, sec_key)
		c_class = __import__("Copy_Template")
                copy = getattr(c_class, "Copy_Template_Details")(api,req)
                #Dest_VM["templateid"]= copy["id"]
		print("Template Copied to Destination, Going to Deploy new VM")
		c_class = __import__("Deploy_VM")
		api = vdc.VDCApiCall(api_url, api_key, sec_key)
		new_VM = getattr(c_class, "Deploy_VM_Details")(api,Dest_VM,True)
		#if len(all_volumes) == 0:
		#	thread.start_new_thread(start_thread, (c_class, "Deploy_VM_Details", api,Dest_VM, False ) )
		#else:
		#	thread.start_new_thread(start_thread, (c_class, "Deploy_VM_Details", api,Dest_VM, True ) )
		req ={'available': 'true', 'region': region, 'zoneid': Dest_VM["zoneid"], 'virtualmachineid': new_VM["id"]}
		count = 1
		if len(all_Volumes) >0:
			for res in all_Volumes:
				time.sleep(5)
				api = vdc.VDCApiCall(api_url, api_key, sec_key)
				print ("Processing volume "+ str(count))
				req["snapshotid"] = res["id"]
				req["name"]=res["name"]
				c_class = __import__("Volume_From_Snapshot")
				#getattr(c_class, "Volume_From_Snapshot_Details")(api,req,True)
				thread.start_new_thread(start_thread, (c_class,"Volume_From_Snapshot_Details", api,req, "Volume"))
				count = count+1
				time.sleep(5)
			wait_for_vol(len(all_Volumes))
		print("New Cloned VM is created, Starting new VM")
                req = {'available': 'true', 'region': region, 'id': new_VM["id"]}
		api = vdc.VDCApiCall(api_url, api_key, sec_key)
                c_class = __import__("Start_VM")
                getattr(c_class, "Start_VM_Details")(api,req,True)	

def Clone(api,region,vmID):
	n_name = raw_input("Enter New Name for VM: ")
	n_displayName = raw_input("Enter New DisplayName for VM: ")
        request = {'available': 'true', 'region': region, 'id': vmID, 'name': n_name, 'displayname': n_displayName}
        result = api.call('updateVirtualMachine',request)
        if ('errorcode' in result):
		print("Error Code: "+ str(result['errorcode']))
                print("Error: "+ result['errortext'])
	else:
		print("VM Renamed Successfully")

def wait_for_vol(total_volumes):
	while(True):
		if total_volumes == vol_attached:
			print("All Volumes are attached")
			return "All Done"
		else:
			to_Process = total_volumes -vol_attached
			print('.', end='')
			sys.stdout.flush()
		time.sleep(4)

def start_thread(c_class, function, api, request, other):
	global vol_attached
	try:
		if other== 0:
			getattr(c_class, function)(api,request)
		elif other=="Volume":
			result = getattr(c_class, function)(api,request,True)
			if (result == "error"):
				print("Problem While processing snapshotid:" + request["snapshotid"])
				vol_attached = vol_attached + 1
			else:
				print("Volume from "+ result["name"] + "created and attached to VM")
				vol_attached = vol_attached + 1
		else:
			getattr(c_class, function)(api,request,other)
	except Exception as e:
		print(e)
