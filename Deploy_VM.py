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


d_options= ["Template", "ISO"]
d_temp = ["Interoutes Templates", "Templates Imported to VDC"]
os_Type = ["ALL", "Windows", "CentOS", "DEBIAN", "Ubuntu", "pfSense", "Fedora", "FreeBSD", "OpenSUSE", "CoreOS", "COREOS"]
def Deploy_VM(api,region):
	try:
		c_class = __import__("Select_Zone")
                zone = getattr(c_class, "Select_Zone")(api,region)
                VM_Request = {'available': 'true', 'region': region, 'zoneid': zone["id"]}
		print("*****Select Deployment Method*******")
		count =1 
		Truee = True
		req={'available': 'true', 'region': region, 'zoneid': zone["id"]}
		for res in d_options:
                        print(str(count) + " " + res )
                        count = count+1
		while(Truee):
                        sel_Num = raw_input('Select Deployment: ')
                        try:
                                sel_Num = int(sel_Num)
				if sel_Num == 1:
					print("VM to be deployed from Template")
					count = 1
					for res in d_temp:
			                        print(str(count) + " " + res )
			                        count = count+1
					while(Truee):
			                        tmp_Num = raw_input('Select Template Category: ')
			                        try:
							tmp_Num = int(tmp_Num)
							if tmp_Num == 1:
								req["templatefilter"]="featured"
								keywork = Select_Fetured_Template_Category()
								req["keyword"]=keywork.lower()
								Truee = False
							elif tmp_Num == 2:
								req["templatefilter"]="self"
								Truee = False
							else:
								print("Number should be between 1 and 2" )
							c_class = __import__("Select_Templates")
							temp = getattr(c_class, "Select_Templates")(api,req)
							VM_Request["templateid"]=temp["id"]
						except Exception as e:
							print(e)	
				elif sel_Num == 2:
					VM_Request["hypervisor"]="VMware"
					c_class = __import__("Select_Isos")
                                        iso = getattr(c_class, "Select_Isos")(api,req)
					VM_Request["templateid"]=iso["id"]
					reqq={'available': 'true', 'region': region, 'zoneid': zone["id"]}
					c_class = __import__("Select_Disk_Offering")
                                        diskOffering = getattr(c_class, "Select_Disk_Offering")(api,reqq)
					VM_Request["size"]=10
					if diskOffering["disksize"]==0:
						while(True):
							size=raw_input("Enter Root Disk Size in GB: ")
							try:
								size=int(size)
								if (size > 10 and size < 1945):
									VM_Request["size"]=size
									break
								else:
									print("Invalid Disk Size try again")
							except:

								print("Invalid root Disk Size Should be greater then 10GB and less then 1945GB")
						
					VM_Request["diskofferingid"]=diskOffering["id"]
					Truee = False
                                else:
                                        print("Number should be between 1 and 2" )
			
                        except Exception as e:
                                print(e)
		req={'available': 'true', 'region': region, 'zoneid': zone["id"]}
		Truee = True
		while(Truee):
			cpus = raw_input("Enter Number of CPUs required: ")
			try:
				#cpus = int(cpus)
				req['keyword']=" "+cpus+"x2.0 GHz"
				c_class = __import__("Select_Service_Offering")
                		serviceoffering = getattr(c_class, "Select_Service_Offering")(api,req)
				if (serviceoffering=="error"):
					print("Unable to find Service Offering with "+ cpus + " enter number from 1 to 12")	
				else:
					Truee = False
					VM_Request["serviceofferingid"]=serviceoffering["id"]
			except Exception as e:
				print(e)
		req = {'available': 'true', 'region': region, 'zoneid': zone["id"] }
        	c_class = __import__("Select_Network")
        	select_network = getattr(c_class, "Select_Network")(api,req)
		if select_network[1] != False:
                	VM_Request["ipaddress"] = select_network[1]
        	VM_Request["networkids"] = (select_network[0])["id"]
		VM_Request["name"]=raw_input("Enter VM Name: ")
		VM_Request["displayname"]=VM_Request["name"]
		deploy = Deploy_VM_Details(api,VM_Request, False)
		if (deploy=="error"):
			print("Unable to Deploy VM")
		else:
			deploy["password"]
		print(VM_Request)
	except Exception as e:
		print(e)

def Deploy_VM_Details(api,request,background):
	print("Starting Virtual Machine Deployment")
	result = api.call('deployVirtualMachine', request)
	if "errorcode" in result:
                print("ErrorCode: " + str(result["errorcode"]))
                print("ErrorText: "+ result["errortext"])
                return "error"
	else:
		if background:
			result = api.wait_for_job_background(result['jobid'])
		else:
			result = api.wait_for_job(result['jobid'])
		if "errorcode" in result:
			print("ErrorCode: " + str(result["errorcode"]))
			print("ErrorText: "+ result["errortext"])
			return "error"
		else:
			#print(result)
			print("VM "+ result["virtualmachine"]["name"]+ " Started Successfully")
			return result["virtualmachine"]

def Select_Fetured_Template_Category():
	os_Type = ["ALL", "Windows", "CentOS", "DEBIAN", "Ubuntu", "pfSense", "Fedora", "FreeBSD", "OpenSUSE", "CoreOS", "COREOS"]
	count =1
	Truee = True
	for res in os_Type:
		print(str(count) + " " + res )
                count = count+1
	while(Truee):
		sel_Num = raw_input('Select VM Category: ')
                try:
                	sel_Num = int(sel_Num)
                        if (sel_Num < len(os_Type)+1 and sel_Num > 0):
                        	print("VM Category Selected: "+ os_Type[sel_Num-1])
				if sel_Num == 1:
					return ""
                                else:
					return os_Type[sel_Num-1]
                                Truee = False
                                break
			else:
                		print("Number should be between 1 and " + str(len(result["virtualmachine"])))
                except Exception as e:
                	print(e)	
