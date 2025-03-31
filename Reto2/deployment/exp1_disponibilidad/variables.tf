variable "image_ec2" {
  description = "AMI ID for the EC2 instance"
  type        = string
}

variable "instance_type" {
  description = "Instance type for the EC2 instance"
  type        = string
}

variable "ssh_key" {
  description = "SSH key name"
  type        = string
}

variable "region" {
  description = "AWS region"
  type        = string
}

variable "availability_zone" {
  description = "AWS availability zone"
  type        = string
}

variable "user_data_file" {
  description = "User data file for instance"
  type        = string
}

variable "db_password" {
  description = "Database password"
  type        = string
}