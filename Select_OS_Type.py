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


def Select_OS_Type(api,region):
	try:	
		request = {'available': 'true', 'region': region}
		#print "****Select OS Category*****"
		keyword = raw_input("Enter OS Type Keywork: ")
		request["keyword"]= keyword
		result = OS_ID(api, request)
		return result
	except Exception as e:
		print(e)

def OS_ID(api, request):
	result = api.call("listOsTypes", request)
	count = 1
	print "****Select OS Type*****"
	for ostype in result['ostype']:
		print(str(count) + " " +ostype['description'])
        	count = count+1
        Truee = True
        while(Truee):
		sel_Num = raw_input('Select OS Type: ')
		try:
			sel_Num = int(sel_Num)
                        if (sel_Num < len(result["ostype"])+1 and sel_Num > 0):
                        	print("OS Type Selected: "+ result["ostype"][sel_Num-1]["description"])
                                return result["ostype"][sel_Num-1]
                                Truee = False
                                break
			else:
                		print("Number should be between 1 and " + str(len(result["ostype"])))
		except Exception as e:
                	print(e)
