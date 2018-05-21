# Clean-up:
#  Configure to take commandline or env args for input / output buckets
#  Configure to take AWS region as an arg or env

import boto3
import json
import os

if __name__ == "__main__":
    inBucket='firefactoryims'
    jsonBucket='firefactoryjson'
    
    rekognition = boto3.client('rekognition','us-east-1')
    s3 = boto3.resource('s3')

    imsBucket = s3.Bucket(inBucket)

    for object in imsBucket.objects.all():
        ext = os.path.splitext(object.key)[1].lower()
        if ext not in ['.jpg', '.jpeg', '.png']:
            # Skip non-image files, folder objects ... etc
            continue
        jsonKey = os.path.splitext(object.key)[0] + '.json'
        print '{0} - {1}'.format(object.bucket_name, object.key)

        # Get labels that have greater than 60% confidence
        labels = rekognition.detect_labels(Image={'S3Object':{'Bucket':inBucket, 'Name':object.key}}, MinConfidence=60.0)
        data = dict()
        data['Labels'] = labels['Labels']

        # Write JSON output to json Bucket
        jsonObject = s3.Object(jsonBucket, jsonKey)
        jsonObject.put(Body=json.dumps(data))
 

