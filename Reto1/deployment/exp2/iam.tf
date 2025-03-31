# IAM role for EC2 instance
resource "aws_iam_role" "ec2_sqs_sender_role" {
  name = "ec2-role-sqs-sender"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Principal = {
          Service = "ec2.amazonaws.com"
        },
        Effect = "Allow"
      },
    ]
  })
}

# IAM policy to allow internet access
resource "aws_iam_policy" "ec2_full_sqs_policy" {
  name        = "ec2-full-access-sqs"
  description = "IAM policy for EC2 full access to SQS"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action   = [
          "sqs:*"
        ],
        Effect   = "Allow",
        Resource = "*"
      }
    ]
  })
}

# Attach the policy to the role
resource "aws_iam_role_policy_attachment" "ec2_role_policy_attach_sqs_sender" {
  policy_arn = aws_iam_policy.ec2_full_sqs_policy.arn
  role       = aws_iam_role.ec2_sqs_sender_role.name
}

# Create an instance profile
resource "aws_iam_instance_profile" "ec2_role_sqs_sender_profile" {
  name = "ec2-instance-profile-sqs-sender"
  role = aws_iam_role.ec2_sqs_sender_role.name
}
