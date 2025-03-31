resource "aws_instance" "sender_sqs"{
  ami = var.image_sender_sqs
  instance_type = var.instance_type_sender_sqs
  key_name = var.ssh_key_sender_sqs
  subnet_id = aws_default_subnet.default_az1.id
  vpc_security_group_ids = [aws_security_group.sender_sqs_instance_sg.id]
  iam_instance_profile = aws_iam_instance_profile.ec2_role_sqs_sender_profile.name
  user_data = file(var.user_data_file)
  availability_zone = var.availability_zone

  tags = {
    Name = "arquitecturaSoftwareSQSSender"
  }

  root_block_device {
      volume_size = 2000
  }
}

output "instance_public_ips" {
  value = aws_instance.sender_sqs.public_ip
}