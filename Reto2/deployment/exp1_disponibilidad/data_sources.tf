data "aws_subnets" "default" {
    filter{
        name = "vpc-id"
        values = [aws_default_vpc.default.id]
    }
}