data "aws_caller_identity" "current" {}
data "aws_region" "current" {}



resource "aws_iam_policy" "lambda_polices" {
  name        = "lambda_polices"
  policy = jsonencode(   
{
  "Version": "2012-10-17",
  "Statement":[{
    "Sid":"AllowPublishToYoutupeWatchTopic",
    "Effect":"Allow",
    "Action":["sns:Publish","sns:CreateTopic"],
    "Resource":"arn:aws:sns:${data.aws_region.current.name}:${data.aws_caller_identity.current.id}:*"
  },
  {
      "Effect" : "Allow",
      "Action" : [
        "appconfig:StartConfigurationSession",
        "appconfig:GetLatestConfiguration"
      ],
      "Resource" : [
        "arn:aws:appconfig:${data.aws_region.current.name}:${data.aws_caller_identity.current.id}:*"
      ]
    },

    {
        "Effect": "Allow",
        "Action": [
            "s3:*"
        ],
        "Resource": "arn:aws:s3:::*"
    },

     {
            "Sid": "AllowStartListGetTranscribe",
            "Effect": "Allow",
            "Action": [
                "transcribe:GetTranscriptionJob",
                "transcribe:StartTranscriptionJob",
                "transcribe:ListTranscriptionJobs",
                "transcribe:ListTagsForResource"
            ],
            "Resource": "*"
        }

  ]
}

   )
  }

resource "aws_iam_role" "lambda_exec" {
  name = "YoutubeWatch-lambda"

  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
POLICY
}

resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_acess_ssm_policy" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMReadOnlyAccess"
}

resource "aws_iam_role_policy_attachment" "lambda_polices_attachment" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.lambda_polices.arn
}


resource "aws_lambda_function" "YoutubeWatch-lambda" {
  function_name = "YoutubeWatch"

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_object.YoutubeWatch_object.key

  runtime = "python3.9"
  handler = "app.lambda_handler"
  timeout= 50
  role = aws_iam_role.lambda_exec.arn

    depends_on = [
      aws_s3_object.YoutubeWatch_object
    ]
}
resource "random_pet" "lambda_bucket_name" {
  prefix = "lambda"
  length = 2
}

resource "aws_s3_bucket" "lambda_bucket" {
  bucket        = random_pet.lambda_bucket_name.id
  force_destroy = true
}

resource "aws_s3_bucket_public_access_block" "lambda_bucket" {
  bucket = aws_s3_bucket.lambda_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

variable "lambda_src_path" {
  type        = string
  description = "The relative path to the source of the lambda"
  default     = "../lambda_function_files"
}

resource "null_resource" "install_dependencies" {
  provisioner "local-exec" {
    command = "pip3 install -r ${var.lambda_src_path}/requirements.txt -t ${var.lambda_src_path}/"
  }
    triggers = {
    dependencies_versions = filemd5("${var.lambda_src_path}/requirements.txt")
    source_versions = filemd5("${var.lambda_src_path}/app.py")
  }
}

resource "random_uuid" "lambda_src_hash" {
  depends_on = [null_resource.install_dependencies]
  keepers = {
    for filename in setunion(
      fileset(var.lambda_src_path, "app.py"),
      fileset(var.lambda_src_path, "requirements.txt"),
      fileset(var.lambda_src_path, "youtupeAPI_handler.py"),
      fileset(var.lambda_src_path, "boto3_handler.py")
    ):
        filename => filemd5("${var.lambda_src_path}/${filename}")
  }
  }

data "archive_file" "lambda_source" {
  depends_on = [null_resource.install_dependencies]
  excludes   = [
    "__pycache__",
    "venv",
  ]

  source_dir  = var.lambda_src_path
  output_path = "${random_uuid.lambda_src_hash.result}.zip"
  type        = "zip"
}

resource "aws_s3_object" "YoutubeWatch_object" {
  bucket = aws_s3_bucket.lambda_bucket.id
  key    = "YoutubeWatch-lambda.zip"
  source = "${random_uuid.lambda_src_hash.result}.zip"
  source_hash = filemd5("${random_uuid.lambda_src_hash.result}.zip")
  depends_on = [
    data.archive_file.lambda_source
  ]
}
