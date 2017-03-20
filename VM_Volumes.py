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


def VM_Volumes(api,region):
	try:
		#print("in Stop VM")
		c_class = __import__("Select_Zone")
                zone = getattr(c_class, "Select_Zone")(api,region)
		
                request = {'available': 'true', 'region': region, 'zoneid': zone["id"]}
		c_class = __import__("Select_VM")
                vm = getattr(c_class, "Select_VM")(api,request)
                request["virtualmachineid"]=vm["id"]
		volume = VM_Volumes_Details(api,request)
		print ("****** Volumes Attached to VM are ******")
		count = 1
		for res in volume:
                        print(str(count) + " " + res['name'] + " (" + str(res['size']/(1024*1024*1024)) + "GB)")
                        count = count+1
		
	except Exception as e:
		print(e)
def Select_VM_Volume(api,request):
	result = VM_Volumes_Details(api,request)
	count = 1
        for res in result:
		print(str(count) + " " + res['name'] + " (" + str(res['size']/(1024*1024*1024)) + "GB)")
		count = count+1
	Truee = True
        while(Truee):
		sel_Num = raw_input('Select Volume: ')
		try:
			sel_Num = int(sel_Num)
                        if (sel_Num < len(result)+1 and sel_Num > 0):
				print("volume Selected: "+ result[sel_Num-1]["name"])
                                return result[sel_Num-1]
                                Truee = False
                                break
			else:
                        	print("Number should be between 1 and " + str(len(result)))
		except Exception as e:
                	print(e)

	
def VM_Volumes_Details(api,request):
	result = api.call('listVolumes', request)
	
	if "errorcode" in result:
		print("ErrorCode: " + result["errorcode"])
		print("ErrorText: "+ result["errortext"])
		return "error"
	else:
		return result["volume"]
