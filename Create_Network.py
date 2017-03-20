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


def Create_Network(api,region):
	try:	
		request = {'available': 'true', 'region': region}
		c_class = __import__("Select_Zone")
                zone = getattr(c_class, "Select_Zone")(api,region)
		request["zoneid"]=zone["id"]
		new_Net = Create_Network_Details(api,request)
	except Exception as e:
		print(e)

def Create_Network_Details(api,request):
	NC = True
	c_Network = '' 
	Truee = True
	while(Truee):
		ng_T = ['PrivateWithGatewayServices', 'Isolated - no services']
		for x in range(1, len(ng_T)+1):
			print (str(x)+ ' ' + ng_T[x-1])
	
		dp_num = raw_input('Select Network Type:')
		try:
			dp_num = int(dp_num)
			if (dp_num < len(ng_T)+1 and dp_num > 0):
				#pprint.pprint(": "+ z_result['zone'][z_Num]['name'].encode('utf-8'))
				req={
					'available': 'true',
					'region': request["region"],
					'zoneid': request["zoneid"],
					'displaytext': ng_T[dp_num-1]
				}
				n_Offerings = api.call('listNetworkOfferings', req)
				request["networkofferingid"] = n_Offerings['networkoffering'][0]['id']
				request["name"] = raw_input('Enter Network Name: ')
				request["netmask"] = raw_input('Enter Network Mask: ')
				request["gateway"] = raw_input("Enter default Gateway IP: ")
				request["displaytext"]=request["name"]
				c_Network = api.call('createNetwork',request)
				if (c_Network['errorcode']):
					print ('Error: ' + str(c_Network['errorcode']))
					print ('Discription: ' + str(c_Network['errortext']))
					print ('Please check Network details and try again. ')

									
			else:
				print("Number should be between 1 and " + str(len(ng_T)))
		except:
			
			if (c_Network['network']):
				print("New Network Created ")
				return c_Network['network']
			else:
				print("Invalid Number Try Again")
