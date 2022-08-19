#!/usr/bin/env python3
import boto3
import argparse
import string

parser = argparse.ArgumentParser('Find duplicate objects in an aws s3 bucket')
parser.add_argument('--bucket', dest='myBucket', default='yourBucketName', help='S3 Bucket to search')

cliArgs = parser.parse_args() 

myBucket = cliArgs.myBucket

# each list_objects_v2 request will return up to 1000 objects.
# We will loop for every 1000, make another list_objects_v2 until end of bucket is reached
lastReqLength = 1000

# at the end of each 1000, know the last key so we can get the next 1000 after it
lastKey = ""

existing = {}

s3 = boto3.client('s3')

print('searching for duplicate objects')
print('')

while lastReqLength == 1000:
    if (lastKey == ""):
        myObjects = s3.list_objects_v2(Bucket=myBucket)
    else:
        myObjects = s3.list_objects_v2(Bucket=myBucket,StartAfter=lastKey)
    lastReqLength = len(myObjects['Contents'])
    for obj in myObjects['Contents']:
        lastKey = obj['Key']
        thisKey = obj['Key']
        thisSize = obj['Size']
        thisEtag = obj['ETag']
        if  thisSize > 0:
            if thisEtag in existing:
                #duplicate found:
                print('!!Duplicate: - %s - %s' % (existing[thisEtag], thisKey))
            else:
                existing[thisEtag] = thisKey
                
print('... The End.')
