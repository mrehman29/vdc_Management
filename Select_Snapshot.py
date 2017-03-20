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


def Select_Snapshot(api,request):
	try:	
		result = api.call('listSnapshots',request)
		count = 1
		Truee = True
                if len(result['snapshot'])==0:
                        print("No Disk Snapshot in this Zone")
                        Truee=False
                        c_class = __import__("Interoute_API")
                        zone = getattr(c_class, "Interoute_API")()
			exit
                print "****Select Snapshot*****"
                for res in result['snapshot']:
                        print(str(count) + " " + res['name'] + " (volumename: " + res['volumename'] + ")")
                        count = count+1
	        while(Truee):
        	        sel_Num = raw_input('Select Snapshot: ')
                	try:
                        	sel_Num = int(sel_Num)
	                        if (sel_Num < len(result["snapshot"])+1 and sel_Num > 0):
        	                        print("Snapshot Selected: "+ result["snapshot"][sel_Num-1]["name"])
                	                return result["snapshot"][sel_Num-1]
                        	        Truee = False
	                                break
        	                else:
                	                print("Number should be between 1 and " + str(len(result["snapshot"])))
			except Exception as e:
				print(e)
	except Exception as e:
		print(e)

def Select_Snapshot_Details(api,request):
	result = api.call('listSnapshots',request)
	if "errorcode" in result:
		print("ErrorCode: " + result["errorcode"])
		print("ErrorText: "+ result["errortext"])
		return "error"
	elif len(result["listSnapshots"]) == 0:
		print ("NO Snapshots in this Zone")
		c_class = __import__("Interoute_API")
                zone = getattr(c_class, "Interoute_API")()
	else:
		return result["snapshot"][0]
