from boto.s3.connection import S3Connection
from boto.s3.key import Key
import boto
import os.path
import sys



def s3_upload():
    #Variables 
    access_key = "AKIAIBFJ7RU324OVTREA"
    access_secret = "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"
    bucket_name = "collegemenusdryrun"

    # test dir
    test_data = "../dates"
    final_dest = ""

    conn = S3Connection(access_key, access_secret)

    mybucket = conn.get_bucket(bucket_name)


    # delete all keys in mybucket
    for key in mybucket.list(prefix=''):
        key.delete()

    uploadFolder = []
    for (test_data, dirname, filename) in os.walk(test_data):
        uploadFolder.extend(dirname)
        break

    uploadDict = {}


    # makes uploadDict, which is
    for dates in uploadFolder:
        temp_dict = {}
        path_to_json = os.path.join(test_data, dates)
        for (path_to_json, dirname, filename) in os.walk(path_to_json):
            uploadDict[dates] = filename
            break

    # creates sourcepath on computer and destpath for s3, uploads them to mybucket
    for folder in uploadDict:
        for filename in uploadDict[folder]:
            sourcepath = os.path.join(test_data, folder, filename)
            destpath = os.path.join(final_dest, folder, filename)
            print 'Uploading %s to Amazon S3 bucket %s' % \
               (sourcepath, bucket_name)

            k = boto.s3.key.Key(mybucket)
            k.key = destpath
            k.set_contents_from_filename(sourcepath, policy='public-read')
    
