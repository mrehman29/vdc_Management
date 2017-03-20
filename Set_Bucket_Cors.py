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

def Set_Bucket_Cors(s3, bucket_name):
	try:
		#c_class = __import__("Select_Bucket")
                #bucket_name = getattr(c_class, "Select_Bucket")(s3)
		bucket = s3.Bucket(bucket_name)
		bucket_cors = bucket.Cors()
		print (bucket_cors)
		bucket_cors = s3.BucketCors(bucket_name)
		response = bucket_cors.put(CORSConfiguration={'CORSRules': [{'AllowedHeaders': ['*'], 'ExposeHeaders': ['ETag'], 'AllowedMethods': ['GET', 'PUT', 'POST', 'DELETE'], 'MaxAgeSeconds': 3000, 'AllowedOrigins': ['*']}]})
	except Exception as e:
		print(e)

