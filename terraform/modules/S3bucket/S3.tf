 resource "aws_s3_bucket" "S3Bucket" {
  bucket = var.bucketname
  force_destroy=true

}


