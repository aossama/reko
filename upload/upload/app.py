import json
import boto3
import datetime
import base64


s3_client = boto3.client('s3')


def upload(event, context):
    # bucket_name = event['bucket_name']
    bucket_name = 'images.luji.io'
    # bucket_key = event['bucket_key']
    bucket_key = "uploads/{}".format(datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f"))
    image = event['body']
    i = base64.b64decode(image)

    upload_status = put_object_into_s3(bucket_name, bucket_key, image)

    current_time = datetime.datetime.now().time()
    body = {
        "message": "Hello, the current time is " + str(current_time),
        "length": i
    }

    return {
        "statusCode": upload_status,
        "body": json.dumps(body)
    }


def put_object_into_s3(bucket_name, bucket_key, body):
    response = s3_client.put_object(Bucket=bucket_name, Key=bucket_key, Body=body)
    status_code = response['ResponseMetadata']['HTTPStatusCode']

    return status_code
