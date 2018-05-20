# Rekognition

This repository contains the source code for an image analysis system based on AWS Rekognition service.

The idea behind this MVP is:
* Have an S3 bucket hosting a simple HTML page with a form to upload an image
* When the form is submitted it sends a POST action to AWS API Gateway
* The API calls a lambda function "upload", which uploads the image to the same S3 bucket under "uploads" key
* Another lambda function "rekognize", is triggered whenever an S3 object is uploaded to the bucket under "uploads/"
* The "rekognize" lambda function sends the image object to AWS Rekognition

## Setup

To get started and setup this (it's still manual), you'll need:

1. Create an S3 bucket with static web hosting enabled, or host the upload.html page on a webserver
2. Under the bucket create a key called "uploads/"

## TODO

* Document this in a better way to that it can be reproduced
* Find a way to store the images with links
* Rekognized images should be viewed in an album along with the labels