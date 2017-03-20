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


import os

def Upload_ISO_Template(api,region):
	try:	
		vdc_api = api[0]
		s3 = api[1]
		client = api[2]
		request = {'available': 'true', 'region': region }
		print("*************Process to Upload ISO/Template***************")
		print("01 Upload ISO/Template from Local drive to Object Storage")
		print("02 Register ISO/Template from Oject Storage to VDC account")
		print("**********************************************************")
		to_call = "Select_Bucket"
		size = sum(1 for _ in s3.buckets.all())
		if (size == 0):
			print("There is no Bucket in your account, creating New Bucket")
			to_call = "Create_Bucket"
		else:
			to_call = "Select_Bucket"
		c_class = __import__(to_call)
               	bucket_name = getattr(c_class, to_call)(s3)
		file_to_upload = raw_input("Enter Local ISO/OVA file path: ")
		file_name = os.path.basename(file_to_upload)
		if os.path.exists(file_to_upload):
			ext = os.path.splitext(file_to_upload)[-1].lower()
			if ext == ".iso":
				#print(ext)
				request = Vdc_Upload_Details(request, vdc_api)
				c_class = __import__("Upload_Object")
				print ("Sit Back and Relax, Uploading " + ext + " to Object Storage")
				upload = getattr(c_class, "u_file")(s3, bucket_name, file_to_upload, file_name)
				print ("ISO Uploaded Getting URL")
				url=client.generate_presigned_url('get_object', Params = {'Bucket': bucket_name, 'Key': file_name}, ExpiresIn = 1500)
				url= url.replace("https://","http://")
				request["url"]=url
				print("Registering ISO")
				c_class = __import__("Register_ISO")
				registerISO = getattr(c_class, "Register")(vdc_api,request)
				#print(registerISO)
				if 'errorcode' in registerISO:
                                        print("Error:")
                                        print("ErrorCode: "+registerISO["errorcode"])
                                        print("ErrorText: "+registerISO["errortext"])
                                else:
                                        print("ISO Registered to VDC")
			elif ext == ".ova":
				#print(ext)
				request["format"]="OVA"
				request["hypervisor"]="VMware"
				request = Vdc_Upload_Details(request, vdc_api)
				#c_class = __import__("Select_OS_Type")
				#os_type = getattr(c_class, "Select_OS_Type")(vdc_api, region)
				#request["ostypeid"] = os_type["id"]
				c_class = __import__("Upload_Object")
				print ("Sit Back and Relax, Uploading " + ext + " to Object Storage")
				upload = getattr(c_class, "u_file")(s3, bucket_name, file_to_upload, file_name)
				url=client.generate_presigned_url('get_object', Params = {'Bucket': bucket_name, 'Key': file_name}, ExpiresIn = 1500)
                                url= url.replace("https://","http://")
                                request["url"]=url
				print("Registring Template to VDC")
				c_class = __import__("Register_Template")
                                registerTemp = getattr(c_class, "Register")(vdc_api,request)
				if 'errorcode' in registerTemp:
					print("Error:")
					print("ErrorCode: "+registerTemp["errorcode"])
					print("ErrorText: "+registerTemp["errortext"])
				else:
					print("Template Registered to VDC")
			else:
				print ("Invalid File Format, file should be ISO or OVA")
		else:
			print(file_to_upload + " doesnot exist")
		#print (reque)
	except Exception as e:
		print(e)

def Vdc_Upload_Details(request, vdc_api):
	request["name"] = raw_input("Enter ISO/Template Name: ")
	request["displaytext"] = raw_input("Enter Display Text: ")
	c_class = __import__("Select_Zone")
        zone = getattr(c_class, "Select_Zone")(vdc_api, request["region"])
	request["zoneid"] = zone["id"]
	c_class = __import__("Select_OS_Type")
	os_type = getattr(c_class, "Select_OS_Type")(vdc_api, request["region"])
	request["ostypeid"] = os_type["id"]
	return request

