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


def Create_Template(api,region):
	try:
		c_class = __import__("Select_Zone")
                zone = getattr(c_class, "Select_Zone")(api,region)
                request = {'available': 'true', 'region': region, 'zoneid': zone["id"]}
		c_class = __import__("Select_VM")
                vm = getattr(c_class, "Select_VM")(api,request)
                request["id"]=vm["id"]
		req = { 'available': 'true','region' : region, 'virtualmachineid' : vm["id"]}
                c_class = __import__("VM_Volumes")
                volume = getattr(c_class, "Select_VM_Volume")(api,req)
		temp_name = volume["name"]+"-Temp"
		req = { 'available': 'true','region' : region, 'volumeid' : volume["id"], 'ostypeid': vm["ostypeid"], 'name': temp_name, 'displaytext': temp_name}
		temp = Create_Template_Details(api,req)	
	except Exception as e:
		print(e)

def Create_Template_Details(api,request):
	#print("Starting Virtual Machine")
	result = api.call('createTemplate', request)
	result = api.wait_for_job(result['jobid'])
	if "errorcode" in result:
		print("ErrorCode: " + str(result["errorcode"]))
		print("ErrorText: "+ result["errortext"])
		return "error"
	else:
		print("Template Created and is ready to use")
		return result["template"]
