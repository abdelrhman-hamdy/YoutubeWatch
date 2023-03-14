
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
You will need to have the following to run the project successfully : 
- AWS account 
- AWS CLI access 
- Installing Terraform, pip3

# Run The Application
 you will need to provide some values when applying the terraform :
 - Youtupe API key, to get one, check this [link](https://www.youtube.com/watch?v=D56_Cx36oGY&t=76s) from 1:16 to 4:45 
 - A username and password of your choice for the created database.
 - Email address to receive notifications. DON'T forget to confirm the subscription that will be sent from SNS
 - List of your favourite youtube channel ids, to know how to get a channel id, check this [link](https://www.youtube.com/watch?v=0oDy2sWPF38)

```bash
 git clone https://github.com/abdelrhman-hamdy/YoutupeWatch.git
 cd YoutupeWatch/terraform/dev
 terraform init  
 export TF_VAR_YoutupeApi="YOUR-YOUTUBE-API-KEY"
 export TF_VAR_db_username="YOUR-DB-USERNAME"
 export TF_VAR_db_password="YOUR-DB-PASSWORD" 
 export TF_VAR_email_address="YOUER-EMAIL" 
 # Exp of passing channel ids: ChannelsID=["UCGPGirOab9EGy7VH4IwmWVQ","UCoOae5nYA7VqaXzerajD0lg","UCJ24N4O0bP7LGLBDvye7oCA"]
 terraform apply
```
