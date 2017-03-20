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

def Empty_Bucket(s3):
	try:
		c_class = __import__("Select_Bucket")
                bucket_name = getattr(c_class, "Select_Bucket")(s3)
		bucket = s3.Bucket(bucket_name)
		c = raw_input("Are you sure you want to delete all Object from the Bucket N/y ")
		if (c=="Y" or c=="y"):
			for object in bucket.objects.all():
				c_key = object.key
				print "Deleting Object: " + c_key
				object = s3.Object(bucket_name,c_key)
				object.delete()
			cb = raw_input("Bucket is Empty do you want to delete the Bucket Y/N: ")
			if (cb=="Y" or cb=="y"):
				print(bucket.delete())
				print("Bucket Deleted")
	except Exception as e:
		print(e)

