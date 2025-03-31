resource "aws_instance" "microservices"{
  ami = var.image_ec2
  instance_type = var.instance_type
  key_name = var.ssh_key
  subnet_id = aws_default_subnet.default_az1.id
  vpc_security_group_ids = [aws_security_group.microservices_instance_sg.id]
  iam_instance_profile = aws_iam_instance_profile.ec2_role_profile.name
  user_data = file(var.user_data_file)
  availability_zone = var.availability_zone

  tags = {
    Name = "arquitecturaSoftwareReto2Microservicios"
  }

  root_block_device {
      volume_size = 2000
  }
}