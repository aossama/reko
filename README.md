# Rekognition

This repository contains the source code for an image analysis system based on AWS Rekognition service.

The idea behind this MVP is:
* ~~Have an S3 bucket hosting a simple HTML page with a form to upload an image~~
* Two serverless functions
* The "upload" serverless function is a Flask application proxied using API Gateway
* The function has one endpoint and two actions (GET and POST)
* When landing on the function, the GET action renders a form in the browser for uploading a picture
* When the form is submitted it sends a POST action to the same page, which:
  * Uploads the picture to S3 Bucket
  * When the upload is successful, the entry is saved in DynamoDB
* ~~The API calls a lambda function "upload", which uploads the image to the same S3 bucket under "uploads" key~~
* Another lambda function "rekognize", is triggered whenever an S3 object is uploaded to the bucket under "uploads/" prefix
* The "rekognize" lambda function sends the image object to AWS Rekognition

## Setup

To get started and setup this (it's still manual), you'll need:

### Prepare AWS
1. Create an S3 bucket ~~with static web hosting enabled, or host the upload.html page on a webserver~~
2. Under the bucket create a directory called "uploads/"

### Prepare dev environment
Zappa is used to manage the lifecycle of the serverless functions. In order to prepare a development environment you'll need:
* Python 3.6
* Virtualenv

This can be achieved using a docker container:
```bash
$ cd workspace/rekognition/
$ docker run -it --name rekognition-dev -v `pwd`:/apps -w /apps python:3.6 /bin/bash
root@d690b38df861:/apps# pip install virtualenv
root@d690b38df861:/apps# virtualenv .venv
root@d690b38df861:/apps# source .venv/bin/activate
(.venv) root@d690b38df861:/apps# pip install -r requirements.txt
(.venv) root@d690b38df861:/apps# aws configure
AWS Access Key ID [None]: THIS-IS-NOT-MY-ACCESS-KEY
AWS Secret Access Key [None]: TRUST-ME-WHEN-I-TELL-YOU-THIS-IS-NOT-MY-ACCESS-KEY
Default region name [None]: eu-west-1
Default output format [None]: 
(.venv) root@d690b38df861:/apps# cd upload/
(.venv) root@d690b38df861:/apps/upload# zappa deploy dev
(.venv) root@d690b38df861:/apps/upload# zappa deploy dev
Calling deploy for stage dev..
Downloading and installing dependencies..
 - sqlite==python36: Using precompiled lambda package
Packaging project as zip.
Uploading upload-dev-1526864169.zip (7.2MiB)..
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7.59M/7.59M [01:09<00:00, 88.7KB/s]
Scheduling..
Scheduled upload-dev-zappa-keep-warm-handler.keep_warm_callback with expression rate(4 minutes)!
Uploading upload-dev-template-1526864244.json (1.6KiB)..
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1.60K/1.60K [00:00<00:00, 2.47KB/s]
Waiting for stack upload-dev to create (this can take a bit)..
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:09<00:00,  2.52s/res]
Deploying API Gateway..
Deployment complete!: https://4nb09lrj4h.execute-api.eu-west-1.amazonaws.com/dev
(.venv) root@140a414247a9:/apps/upload# cd ../rekognize/
(.venv) root@d690b38df861:/apps/upload# zappa deploy dev
```

A demonstration of the installation can be found in this asciinema https://asciinema.org/a/SF7KALvbw27cWSoRT1bxhK7ip

## TODO

* ~~Document this in a better way to that it can be reproduced~~
* ~~Find a way to store the images with links~~
  * Already started implementing DynamoDB integration
* Rekognized images should be viewed in an album along with the labels