import boto3
import datetime

import requests
from flask import Flask, request, redirect, render_template


app = Flask(__name__)


@app.route("/", methods=["GET"])
def upload_get():
    return render_template('upload.html')


@app.route("/", methods=["POST"])
def upload_post():
    if "image" not in request.files:
        return "No image key in request.files"

    file = request.files["image"]

    if file.filename == "":
        return "Please select a file"

    bucket_name = 'images.luji.io'
    bucket_key = "uploads/{}".format(datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f-{}".format(file.filename)))

    upload_status = put_object_into_s3(bucket_name, bucket_key, file)

    if upload_status == 200:
        # TODO: The placement of detecting the remote IP over here is wrong
        ip = requests.get('http://checkip.amazonaws.com/')
        save_entry_into_dynamodb(ip.text.replace('\n', ''), bucket_key)

    return redirect("/dev")


def put_object_into_s3(bucket_name, bucket_key, body):
    s3 = boto3.client('s3')
    response = s3.put_object(Bucket=bucket_name, Key=bucket_key, Body=body)
    status_code = response['ResponseMetadata']['HTTPStatusCode']

    return status_code


def save_entry_into_dynamodb(uploader_ip, key):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Rekognition')

    table.put_item(
        Item={
            'uploader': str(uploader_ip),
            'key': str(key)
        }
    )


if __name__ == "__main__":
    app.run()
