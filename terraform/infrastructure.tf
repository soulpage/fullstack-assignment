resource "aws_instance" "nextjs_server" {
  ami           = "ami-0d5eff06f840b45e9"  # Ubuntu Server 20.04 LTS AMI
  instance_type = "t2.micro"
  tags = {
    Name = "NextJS-Server"
  }

  provisioner "remote-exec" {
    inline = [
      "sudo apt-get update -y",
      "sudo apt-get install -y docker.io",
      "sudo systemctl start docker",
      "sudo usermod -aG docker ubuntu",
      "sudo docker run -d -p 80:3000 your_dockerhub_username/nextjs:latest"
    ]
  }
}

resource "aws_instance" "django_server" {
  ami           = "ami-0d5eff06f840b45e9"  # Ubuntu Server 20.04 LTS AMI
  instance_type = "t2.micro"
  tags = {
    Name = "Django-Server"
  }

  provisioner "remote-exec" {
    inline = [
      "sudo apt-get update -y",
      "sudo apt-get install -y docker.io",
      "sudo systemctl start docker",
      "sudo usermod -aG docker ubuntu",
      "sudo docker run -d -p 81:8000 your_dockerhub_username/django:latest"
    ]
  }
}

