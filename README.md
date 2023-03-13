
<h3 align="center">YoutubeWatch</h3>

## Table of contents :
- [Introuduction](#introduction)
- [Tools](#tools)
- [Diagram](#diagram)
- [Prerequisites](#prerequisites)
- [Run the Application](#run-the-application)

## Introduction 
YoutubeWatch is a serverless application created on AWS. It simply checks every hour a list of given favourite youtube channels and see if a new video has been uploaded, if any , it publish a message to a SNS topic, which as a result sends emails for each new uploaded video to its subscribers
<p align="center">
<img  src="https://user-images.githubusercontent.com/69608603/224564330-b8d91840-f17f-4da9-88fb-e41a149c95b9.png" alt="centered image" height="400">
</p>

## Tools 
- AWS 
- Terraform 
- Python

## Diagram
 ![YoutupeWatch](https://user-images.githubusercontent.com/69608603/224564562-e6b72d23-3208-4127-a832-7adda9f1b238.png)

## Prerequisites 
you will need to have the following to run the project successfully : 
- AWS account 
- AWS CLI access 
- Youtupe API key, to learn more how to get it check this [link](https://www.youtube.com/watch?v=D56_Cx36oGY&t=76s) from 1:16 to 4:45 

# Run The Application
```bash
$ git clone https://github.com/abdelrhman-hamdy/YoutupeWatch.git
$ cd YoutupeWatch/terraform/dev
$ terraform init 
# in this step , you will need to provide, youtupe API key,also choose a username and password that the mysql database will have
$ terraform apply
```
