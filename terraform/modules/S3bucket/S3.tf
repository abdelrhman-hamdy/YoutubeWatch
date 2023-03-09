 resource "aws_s3_bucket" "S3Bucket" {
  bucket = var.bucketname
  
  provisioner "file" {
    source      = var.src
    destination = var.dest
   
  }

}

resource "aws_s3_bucket_acl" "s3_acl" {
  bucket = aws_s3_bucket.YoutubeWtachBucket.id
  acl    = var.acl 
}

