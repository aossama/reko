import boto3
import datetime

from flask import Flask, request, redirect, render_template


app = Flask(__name__)

s3_client = boto3.client('s3')


@app.route("/", methods=["GET"])
def upload_get():
    return render_template('upload.html')


@app.route("/", methods=["POST"])
def upload_post():
    if "user_file" not in request.files:
        return "No user_file key in request.files"

    file = request.files["image"]

    if file.filename == "":
        return "Please select a file"

    bucket_name = 'images.luji.io'
    bucket_key = "uploads/{}".format(datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f-{}".format(file.filename)))

    output = put_object_into_s3(bucket_name, bucket_key, file)

    return redirect("/upload.html")


def put_object_into_s3(bucket_name, bucket_key, body):
    response = s3_client.put_object(Bucket=bucket_name, Key=bucket_key, Body=body)
    status_code = response['ResponseMetadata']['HTTPStatusCode']

    return status_code


if __name__ == "__main__":
    app.run()
