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


import getpass,json, os, pprint,socket,struct,sys,base64,hashlib,hmac,time,urllib

def Select_Network(api,request):
	try:	
		Truee = True
		result = api.call('listNetworks',request)
		if (len(result["network"]) == 0):
			Truee = False
			print ('No Network Found in the Zone, Creating new network')
			c_class = __import__("Create_Network")
			network = getattr(c_class, "Create_Network_Details")(api,request)
			ip = ask_ip(network)
			return [network,ip]
		else:
			if (len(result["network"]) > 0):
				print ( '0 ' + 'Create New Network' )
			count = 1
			for res in result['network']:
        	                print(str(count) + " " + res['displaytext'] + " (" + res['cidr'] + ")")
                	        count = count+1
              	 	while(Truee):
                        	sel_Num = raw_input('Select Network: ')
                       		try:
                                	sel_Num = int(sel_Num)
                                	if (sel_Num < len(result["network"])+1 and sel_Num > 0):
                                        	print("VM Selected: "+ result["network"][sel_Num-1]["name"])
						network = result["network"][sel_Num-1]
						ip = ask_ip(network)
                                        	#return result["network"][sel_Num-1]["id"]
						return [network,ip]
                                       		Truee = False
                                        	break
                                	elif sel_Num == 0:
						c_class = __import__("Create_Network")
                        			network = getattr(c_class, "Create_Network_Details")(api,request)
                        			ip = ask_ip(network)
						return [network,ip]
					else:
                	                        print("Number should be between 0 and " + str(len(result["network"])))
                        	except Exception as e:
                                	print(e)
	except Exception as e:
		print(e)



def Select_Network_Details(api,request):
	v_Network = api.call('listNetworks', req)
	if (len(v_Network["network"]) > 0):
		print ( '0 ' + 'Create New Network' )
	for x in range(1, len(v_Network['network'])+1):
		print(str(x) +" "+ v_Network["network"][x-1]['displaytext'].encode('utf-8')+ " " +v_Network["network"][x-1]['cidr'].encode('utf-8'))
	Truee = True

def ask_ip(network):
	Default_IP = raw_input('DO you want to specify IP of Default Network: (Y/N)' )
	if(Default_IP is "Y" or Default_IP is "y"):
		Truee = True
		while (Truee):
			D_IP = raw_input('Enter IP Address: ')
			cidr = network['cidr'].encode('utf-8')
			net_mask = cidr.split('/')
			isValid = isIpInSubnet(D_IP, net_mask[0], int(net_mask[1]))
			if(isValid):
				Truee = False
				return D_IP
			else:
				print("IP address Doesn't belongs to the Network")
	else:
		return False

def ipToInt(ip):
    o = map(int, ip.split('.'))
    res = (16777216 * o[0]) + (65536 * o[1]) + (256 * o[2]) + o[3]
    return res

def isIpInSubnet(ip, ipNetwork, maskLength):
    ipInt = ipToInt(ip)
    maskLengthFromRight = 32 - maskLength

    ipNetworkInt = ipToInt(ipNetwork)
    binString = "{0:b}".format(ipNetworkInt)

    chopAmount = 0
    for i in range(maskLengthFromRight):
        if i < len(binString):
            chopAmount += int(binString[len(binString)-1-i]) * 2**i

    minVal = ipNetworkInt-chopAmount
    maxVal = minVal+2**maskLengthFromRight -1

    return minVal <= ipInt and ipInt <= maxVal
