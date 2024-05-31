resource "aws_instance" "nextjs_server" {
  ami                    = "ami-0d5eff06f840b45e9" 
  instance_type          = "t2.micro"
  vpc_security_group_ids = ["sg-0b3600ea379ca4320"]
  subnet_id              = "subnet-0a5fb5dec5e4ac966"
  tags = {
    Name = "NextJS-Server"
  }
}

resource "aws_instance" "django_server" {
  ami                    = "ami-0d5eff06f840b45e9"
  instance_type          = "t2.micro"
  vpc_security_group_ids = ["sg-0b3600ea379ca4320"]
  subnet_id              = "subnet-0a5fb5dec5e4ac966"
  tags = {
    Name = "Django-Server"
  }
}

