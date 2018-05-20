import boto3
import json


def rekognize(event, context):
    """Sample pure Lambda function

    Arguments:
        event LambdaEvent -- Lambda Event received from Invoke API
        context LambdaContext -- Lambda Context runtime methods and attributes

    Returns:
        dict -- {'statusCode': int, 'body': dict}
    """
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
