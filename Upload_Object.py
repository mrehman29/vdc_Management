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

def Upload_Object(s3):
        try:
                c_class = __import__("Select_Bucket")
                bucket_name = getattr(c_class, "Select_Bucket")(s3)

                file_to_upload = raw_input("Enter Local file path: ")
                file_name = os.path.basename(file_to_upload)
                if os.path.exists(file_to_upload):
                        if os.path.isdir(file_to_upload):
                                folder = raw_input("Enter Bucket Folder Name/Path, press enter to opload in bucket root: ")
                                if (len(folder)>0):
                                        if folder.endswith("/"):
                                                folder = folder
                                        else:
                                                folder = folder +"/"
                                        u_folder(s3, bucket_name, file_to_upload, folder, "")
                                else:
                                        print("Invalid Folder")
                        else:
                                folder = raw_input("Enter Bucket Folder Name/Path, press enter to opload in bucket root: ")
                                if (len(folder)>0):
                                        if folder.endswith("/"):
                                                folder = folder
                                        else:
                                                folder = folder +"/"
                                        u_file(s3, bucket_name, file_to_upload, folder+file_name)
                                        #bucket = s3.Bucket(bucket_name).upload_file(file_to_upload, folder+file_name)
                                elif (folder == ""):
					u_file(s3, bucket_name, file_to_upload, file_name)
				else:
                                        print("Invalid Folder")

                else:
                        print(file_to_upload + " does not exist")
                #file = raw_input("Enter File Name to be called default["+ +"]")
                #bucket = s3.Bucket(bucket_name).upload_file(file_to_uplaod, )
        except Exception as e:
                print(e)

def u_file(s3, bucket_name, file_to_upload, object):
        try:
                bucket=s3.Bucket(bucket_name).upload_file(file_to_upload, object)
                print("Object Uploaded")
        except Exception as e:
                print(e)

def u_folder(s3, bucket_name, folder_to_upload, folder, current):
        for filename in os.listdir(folder_to_upload):
                file_to_upload = folder_to_upload+"/"+filename
                if os.path.isdir(file_to_upload):
                        d_folder = folder+"/"+filename
                        u_folder(s3, bucket_name,file_to_upload, d_folder , filename+"/")
                        print("Processing Folder "+ filename)
                else:
                        file = filename
                        if(len(current)>0):
                                file = current + file
                        print("Uploading "+ file)
                        u_file(s3, bucket_name, file_to_upload, file)
