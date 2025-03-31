
data "aws_ecs_cluster" "existing_ecs_cluster_innovacion" {
  cluster_name = "ecs-arquitectura-innovacion-sbx"
}

data "aws_subnets" "default" {
    filter{
        name = "vpc-id"
        values = [aws_default_vpc.default.id]
    }
}