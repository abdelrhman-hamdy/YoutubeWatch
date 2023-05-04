
<h3 align="center">YoutubeWatch</h3>

## Table of contents :
- [Introuduction](#introduction)
- [Tools](#tools)
- [Diagram](#diagram)
- [Prerequisites](#prerequisites)
- [Run the Application](#run-the-application)

## Introduction 
YoutubeWatch is a serverless application created on AWS that periodically checks a list of favorite YouTube channels for new video uploads. If a new video is detected, it publishes a message to an SNS topic, which in turn sends emails to subscribers notifying them of the new video. Because it is a serverless application, it does not require the provisioning or management of servers, and instead leverages AWS services to handle the necessary infrastructure and scaling.
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
```
Modify YoutupeWatch/terraform/dev/vars.tfvars file with your values 

```bash
terraform apply 
```
A confirmation Email from SNS service will be sent to you. Then you will get notified Every hour If one of your favourites Youtupers Upload a new video

