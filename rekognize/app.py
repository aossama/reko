import boto3
import json


def rekognize(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    image = event['Records'][0]['s3']['object']['key']

    client = boto3.client('rekognition', 'eu-west-1')

    response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': image}})

    print('Detected labels for ' + image)
    for label in response['Labels']:
        print(label['Name'] + ' : ' + str(label['Confidence']))

    return {
        "statusCode": 200,
        "body": json.dumps({
            'message': 'rekognized'
        })
    }
