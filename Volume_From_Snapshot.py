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


def Volume_From_Snapshot(api,region):
	try:
		print("Select Zone where source Snapshot is ")
		c_class = __import__("Select_Zone")
                zone = getattr(c_class, "Select_Zone")(api,region)
                request = {'available': 'true', 'region': region, 'zoneid': zone["id"]}
		c_class = __import__("Select_Snapshot")
                snapshot = getattr(c_class, "Select_Snapshot")(api,request)
                request["snapshotid"]=snapshot["id"]
		print ("Select zone where to create new Volume: ")
		c_class = __import__("Select_Zone")
                zone = getattr(c_class, "Select_Zone")(api,region)
		request["zoneid"]=zone["id"]
		request["name"]=raw_input("New Volume Name: ")
		result = Volume_From_Snapshot_Details(api,request, False)	
	except Exception as e:
		print(e)

def Volume_From_Snapshot_Details(api,request,background):
	print("Creating Volume")
	result = api.call('createVolume', request)
	if background:
		result = api.wait_for_job_background(result['jobid'])
	else:
		result = api.wait_for_job(result['jobid'])
	if "errorcode" in result:
		print("ErrorCode: " + str(result["errorcode"]))
		print("ErrorText: "+ result["errortext"])
		return "error"
	else:
		print("Successfully Created "+ result["volume"]["name"])
		return result["volume"]
