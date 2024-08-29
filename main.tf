

# Create a VPC
resource "aws_vpc" "dev_vpc" {
  cidr_block = "10.0.0.0/16"
}

# Create a Public Subnet
resource "aws_subnet" "dev_subnet" {
  vpc_id            = aws_vpc.dev_vpc.id
  cidr_block        = "10.0.1.0/24"
  map_public_ip_on_launch = true  # Enable public IP assignment
}

# Create an Internet Gateway
resource "aws_internet_gateway" "dev_igw" {
  vpc_id = aws_vpc.dev_vpc.id
}

# Create a Route Table and Route
resource "aws_route_table" "dev_rt" {
  vpc_id = aws_vpc.dev_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.dev_igw.id
  }
}

# Associate the Route Table with the Subnet
resource "aws_route_table_association" "dev_rta" {
  subnet_id      = aws_subnet.dev_subnet.id
  route_table_id = aws_route_table.dev_rt.id
}

# Create a Security Group
resource "aws_security_group" "dev_sg" {
  vpc_id = aws_vpc.dev_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Allow SSH from anywhere
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

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
    from_port   = 9000
    to_port     = 9000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Generate an SSH Key Pair
resource "tls_private_key" "rsa" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "TF_key" {
  key_name   = "TF_key_1"
  public_key = tls_private_key.rsa.public_key_openssh
}

# Save the private key to a local file
resource "local_file" "TF-key" {
  content  = tls_private_key.rsa.private_key_pem
  filename = "tfkey1.pem"
}

# Create an EC2 Instance
resource "aws_instance" "Frontend" {
  ami             = "ami-04cdc91e49cb06165"  # Ubuntu 20.04 LTS AMI
  instance_type   = "t3.micro"
  subnet_id       = aws_subnet.dev_subnet.id
  vpc_security_group_ids = [aws_security_group.dev_sg.id]

  key_name = aws_key_pair.TF_key.key_name

  tags = {
    Name = "Frontend"
  }

  user_data = base64encode(file("requirements.sh"))
}


resource "aws_instance" "Backend" {
  ami             = "ami-04cdc91e49cb06165"  # Ubuntu 20.04 LTS AMI
  instance_type   = "t3.micro"
  subnet_id       = aws_subnet.dev_subnet.id
  vpc_security_group_ids = [aws_security_group.dev_sg.id]

  key_name = aws_key_pair.TF_key.key_name

  tags = {
    Name = "Backend"
  }

  user_data = base64encode(file("requirements.sh"))
}

resource "aws_instance" "Monitoring" {
  ami             = "ami-04cdc91e49cb06165"  # Ubuntu 20.04 LTS AMI
  instance_type   = "t3.micro"
  subnet_id       = aws_subnet.dev_subnet.id
  vpc_security_group_ids = [aws_security_group.dev_sg.id]

  key_name = aws_key_pair.TF_key.key_name

  tags = {
    Name = "Monitoring"
  }

  user_data = base64encode(file("Monitoring.sh"))
}

resource "aws_instance" "Runner" {
  ami             = "ami-04cdc91e49cb06165"  # Ubuntu 20.04 LTS AMI
  instance_type   = "t3.medium"
  subnet_id       = aws_subnet.dev_subnet.id
  vpc_security_group_ids = [aws_security_group.dev_sg.id]

  key_name = aws_key_pair.TF_key.key_name

  tags = {
    Name = "Runner"
  }

  user_data = base64encode(file("Runner.sh"))
}



# Output the public IP of the instance
# Existing Terraform resources...

# Outputs for public IPs
output "Frontend_public_ip" {
  value = aws_instance.Frontend.public_ip
}

output "Backend_public_ip" {
  value = aws_instance.Backend.public_ip
}

output "Monitoring_public_ip" {
  value = aws_instance.Monitoring.public_ip
}

output "Runner_public_ip" {
  value = aws_instance.Runner.public_ip
}

# Save public IPs to a local file
resource "local_file" "public_ips" {
  content = <<EOT
Frontend: ${aws_instance.Frontend.public_ip}
Backend: ${aws_instance.Backend.public_ip}
Monitoring: ${aws_instance.Monitoring.public_ip}
Runner: ${aws_instance.Runner.public_ip}
EOT
  filename = "${path.module}/ips.txt"
}
