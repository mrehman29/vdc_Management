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


def Select_Service_Offering(api,request):
	try:	
		result = api.call('listServiceOfferings',request)
		count = 1
		Truee = True
                if len(result['serviceoffering'])==0:
			return "error"
                print "****Select ISO*****"
                for res in result['serviceoffering']:
                        print(str(count) + " " + res['displaytext'] )
                        count = count+1
	        while(Truee):
        	        sel_Num = raw_input('Select Service Offering: ')
                	try:
                        	sel_Num = int(sel_Num)
	                        if (sel_Num < len(result["serviceoffering"])+1 and sel_Num > 0):
        	                        print("Select Service Offering: "+ result["serviceoffering"][sel_Num-1]["displaytext"])
                	                return result["serviceoffering"][sel_Num-1]
                        	        Truee = False
	                                break
        	                else:
                	                print("Number should be between 1 and " + str(len(result["serviceoffering"])))
			except Exception as e:
				print(e)
	except Exception as e:
		print(e)

def Select_Service_Offering_Details(api,request):
	result = api.call('listServiceOfferings',request)
	if "errorcode" in result:
		print("ErrorCode: " + result["errorcode"])
		print("ErrorText: "+ result["errortext"])
		return "error"
	elif len(result["serviceoffering"]) == 0:
		print ("NO Service Offering found")
		c_class = __import__("Interoute_API")
                zone = getattr(c_class, "Interoute_API")()
	else:
		return result["serviceoffering"][0]
