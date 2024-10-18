output "nextjs_public_ip" {
  value = aws_instance.nextjs_server.public_ip
}

output "django_public_ip" {
  value = aws_instance.django_server.public_ip
}

