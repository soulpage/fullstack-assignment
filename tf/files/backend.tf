terraform {
  backend "s3" {
    bucket         = "custom-chatgpt-project-bucket"
    region         = "ap-south-2"
    key            = "custom-chatgpt/terraform.tfstate"
    dynamodb_table = "Lock-Files"
    encrypt        = true
  }
}
