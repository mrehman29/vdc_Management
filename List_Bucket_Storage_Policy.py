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


from boto3.session import Session
import requests

from awsauth import S3Auth
import base64
import hashlib


def List_Bucket_Storage_Policy(s3):
	try:
		oapi_key=s3[0]
		osec_key=s3[1]
		oapi_url=s3[2]
		session = Session(aws_access_key_id=oapi_key,aws_secret_access_key=osec_key)
		s3 = session.resource('s3', endpoint_url=oapi_url)
		OSauth = S3Auth(oapi_key, osec_key, service_url='s3-eu.object.vdc.interoute.com')
		#print(OSauth)
		print("Bucket Name: Policy")
		for bucket in s3.buckets.all():
			bucket_name = bucket.name
			r = requests.get('http://'+bucket_name+'.s3-eu.object.vdc.interoute.com', auth=OSauth)
			pID = r.headers["x-gmt-policyid"]
			if pID == 'af465a16f7aac15f6283316b0113057e':
				pID = pID + " (London, Slough, Amsterdam)"
			if pID == 'd06b2c336f4e77ce1e01da4819b77476':
				pID = pID + " (London (2), Slough (1))"
			if pID == '433635bcc26110055a871ded8e775df9':
				pID = pID + " (Amsterdam (2), London (1))"
			if pID == 'fb329ad8180518ffc9e7280d35262535':
				pID = pID + " (London (2), Amsterdam (1))"
				
			print (bucket_name + ": "+pID)
		return bucket_name
	except Exception as e:
		print(e)

