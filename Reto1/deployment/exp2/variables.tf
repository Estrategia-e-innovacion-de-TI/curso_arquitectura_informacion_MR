variable "image_sender_sqs" {
  description = "AMI ID for the EC2 instance"
  type        = string
}

variable "instance_type_sender_sqs" {
  description = "Instance type for the EC2 instance"
  type        = string
}

variable "ssh_key_sender_sqs" {
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