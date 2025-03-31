resource "aws_default_vpc" "default" {
  tags = {
    Name = "Default VPC"
  }
}

resource "aws_default_subnet" "default_az1" {
  availability_zone = var.availability_zone
}

resource "aws_default_subnet" "default_az2" {
  availability_zone = "us-east-1b"  // Change this to a different AZ in your region
}