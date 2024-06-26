provider "aws" {
  region = "ap-south-1"
}


resource "aws_security_group" "nextjs-django-sg" {
  name        = "nexjs-django-sg"
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


resource "aws_instance" "nextjs-django" {
  ami           = "ami-0f58b397bc5c1f2e8"
  instance_type = "t2.micro"


  security_groups = [aws_security_group.nextjs-django-sg.name]

  tags = {
    Name = "nextjs-django"

  
  }

}
