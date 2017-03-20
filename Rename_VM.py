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


def Rename_VM(api,region):
	id_True = raw_input("Do you have VM ID Y/N: ")
	if (id_True=="Y" or id_True=="y"):
		Rename_by_id(api,region)
	elif (id_True=="N" or id_True=="n"):
		Rename_by_Selection(api,region)
	else:
		print "Invalid selection"
		Rename_VM(api,region)
	
def Rename_by_id(api,region):
	vmID = raw_input("Enter VM ID: ")
	if (len(vmID) == 36):
		Rename(api,region,vmID)
		#request = {'available': 'true', 'region': region }
		#n_name = raw_input("Enter New Name for VM: ")
		#n_displayName = raw_input("Enter New DisplayName for VM: ")
		#request = {'available': 'true', 'region': region, 'id': vmID, 'name': n_name, 'displayname': n_displayName}
		#result = api.call('updateVirtualMachine',request)
		#if ('errorcode' in result):
		#	print("Error Code: "+ str(result['errorcode']))
		#	print("Error: "+ result['errortext'])
		#else:
		#	print("VM Renamed Successfully")

	else:
		print "Invalid VM ID, Please check VM ID and try again"
                Rename_by_id(api,region)
		
def Rename_by_Selection(api,region):
	try:	
		c_class = __import__("Select_Zone")
		zone = getattr(c_class, "Select_Zone")(api,region)
		request = {'available': 'true', 'region': region, 'zoneid': zone["id"]}
		c_class = __import__("Select_VM")
                vm = getattr(c_class, "Select_VM")(api,request)
		Rename(api,region,vm['id'])
	except Exception as e:
		print(e)

def Rename(api,region,vmID):
	n_name = raw_input("Enter New Name for VM: ")
	n_displayName = raw_input("Enter New DisplayName for VM: ")
        request = {'available': 'true', 'region': region, 'id': vmID, 'name': n_name, 'displayname': n_displayName}
        result = api.call('updateVirtualMachine',request)
        if ('errorcode' in result):
		print("Error Code: "+ str(result['errorcode']))
                print("Error: "+ result['errortext'])
	else:
		print("VM Renamed Successfully")
