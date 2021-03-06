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
import boto3

def Bucket_Summary(s3):
	total_size = 0
	total_objects=0
	content_type= []
	content_type_object = []
	content_type_size = []
        try:
                c_class = __import__("Select_Bucket")
                bucket_name = getattr(c_class, "Select_Bucket")(s3)
                bucket = s3.Bucket(bucket_name)
                count = 1
                for object in bucket.objects.all():
			ob = s3.Object(bucket_name,object.key)
			total_size = int(total_size) + int(ob.content_length)
			total_objects= int(total_objects) + 1
			print(ob.content_type)
			print(ob.content_length)
			if content_type_size[ob.content_type]:
				content_type_size[ob.content_type]= int(content_type_size[ob.content_type]) + int(ob.content_length)
			else:
				content_type_object.append(ob.content_type)
				content_type_size[ob.content_type] = int(ob.content_length)
                        #print(str(count)+ ": "+ object.key)
                        #count = count + 1
		print("Total Size: " + str(total_size/(1024*1024)) + " Total Objects: " + str(total_objects))
		print(content_type_object)
		print(content_type_size)
                return bucket_name
        except Exception as e:
                print(e)
