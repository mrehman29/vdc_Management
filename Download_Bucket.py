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
import os

def Download_Bucket(s3):
        try:
                c_class = __import__("Select_Bucket")
                bucket_name = getattr(c_class, "Select_Bucket")(s3)
                folder_name = raw_input("Enter Lcoal folder Path where you want to downlaod objects: ")
		check_download(s3, bucket_name, folder_name)
                #file = object.download_file(file_name)

        except Exception as e:
                print(e)

def check_download(s3, bucket_name, folder_name):
	if os.path.exists(folder_name):
		if os.path.isdir(folder_name):
			bucket = s3.Bucket(bucket_name)
               		for object in bucket.objects.all():
				#print(object)
				c_key = object.key
				print("Downloading " + c_key)
				if (c_key.find("/") != -1):
					fix_subfolder(c_key, folder_name)
				file = s3.Object(bucket_name, c_key)
				down = file.download_file(folder_name+"/"+c_key)
		else:
			print "Invalid Local Directory"
			Download_Bucket(s3)

	else:
		print "Invalid Destination Path"
		Download_Bucket(s3)

def fix_subfolder(c_key, base):
	if not os.path.exists(base + "/"+os.path.dirname(c_key)):
		print "Creating Directory "+c_key
		os.makedirs(base + "/"+os.path.dirname(c_key))
	
	
