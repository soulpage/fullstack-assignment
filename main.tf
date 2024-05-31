# Define provider (e.g., AWS)
provider "aws" {
  region = "ap-south-1"  # Specify your AWS region
}

# Create a security group
resource "aws_security_group" "example_sg" {
  name        = "example-security-group"
  description = "Allow inbound traffic on ports 3000(frontend), 8000(backend), 8080(jenkins), and 22"

  # Inbound rules
  ingress {
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

}

# Create an EC2 instance
resource "aws_instance" "example_ec2" {
  ami           = "ami-0f58b397bc5c1f2e8"  # Specify your AMI ID
  instance_type = "t2.micro"               # Specify your instance type
  

  security_groups = [aws_security_group.example_sg.name]

  tags = {
    Name = "example-ec2-instance"
  }
}

