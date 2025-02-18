# IAM role for EC2 instance
resource "aws_iam_role" "ec2_role" {
  name = "ec2-role-internet-access"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Principal = {
          Service = "ec2.amazonaws.com"
        },
        Effect = "Allow",
        Sid = ""
      },
    ]
  })
}

# IAM policy to allow internet access
resource "aws_iam_policy" "ec2_policy" {
  name        = "ec2-policy-internet-access"
  description = "IAM policy for EC2 instance to access internet"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action   = [
          "ec2:*"
        ],
        Effect   = "Allow",
        Resource = "*"
      }
    ]
  })
}

# Attach the policy to the role
resource "aws_iam_role_policy_attachment" "ec2_role_policy_attach" {
  policy_arn = aws_iam_policy.ec2_policy.arn
  role       = aws_iam_role.ec2_role.name
}

# Create an instance profile
resource "aws_iam_instance_profile" "ec2_role_profile" {
  name = "ec2-instance-profile-internet-access"
  role = aws_iam_role.ec2_role.name
}
