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

INTEROUTE_S3_KEY = '00f45eaf0d7afd66a507'
INTEROUTE_S3_SECRET = 'b31KjQ5A549TVsrOB5w7a+Con6w3R1d82Q/wabHV'

OSauth = S3Auth(INTEROUTE_S3_KEY, INTEROUTE_S3_SECRET, service_url='s3-eu.object.vdc.interoute.com')

def Create_Bucket(s3):
	try:
		bucket_name = raw_input("Enter New Bucket Name: ")
		s3.create_bucket(Bucket=bucket_name)
		print("Bucket Created, ")
		c_class = __import__("Set_Bucket_Cors")
                cors = getattr(c_class, "Set_Bucket_Cors")(s3, bucket_name)
		#result = requests.put('http://bucket00000001.s3-eu.object.vdc.interoute.com/', auth=OSauth, headers={'x-gmt-policyid': '433635bcc26110055a871ded8e775df9'})
		#print (result.headers)
		#bucket_cors = s3.BucketCors(bucket_name)
		#bucket_cors.reload()
		return bucket_name
	except Exception as e:
		print(e)

