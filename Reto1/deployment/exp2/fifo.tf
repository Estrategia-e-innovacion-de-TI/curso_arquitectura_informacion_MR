resource "aws_sqs_queue" "terraform_queue" {
  name                        = "matching-queue.fifo"
  fifo_queue                  = true
  content_based_deduplication = true
}

resource "aws_sqs_queue_policy" "example" {
  queue_url = aws_sqs_queue.terraform_queue.id

  policy = jsonencode({
    Version = "2012-10-17" # !! Important !!
    Statement = [{
      Sid    = "arqsoft-sqs-s3"
      Effect = "Allow"
      Principal = {
        Service = "s3.amazonaws.com"
      }
      Action   = "sqs:*"
      Resource = aws_sqs_queue.terraform_queue.arn
      Condition = {
        ArnLike = {
          "aws:SourceArn" = aws_instance.sender_sqs.arn
        }
      }
    }]
  })
}