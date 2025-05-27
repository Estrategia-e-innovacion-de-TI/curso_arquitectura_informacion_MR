resource "aws_ecs_service" "service" {
  name            = "backend-service-score-procesamiento"
  cluster         = data.aws_ecs_cluster.existing_ecs_cluster_innovacion.id
  task_definition = aws_ecs_task_definition.task_cursoArqSoft.arn
  desired_count   = var.ecs_min_task_count
  launch_type     = "FARGATE"

#TODO change assign_public_ip to false, which implies to change the VPC to a private one
  network_configuration {
    subnets = data.aws_subnets.default.ids
    security_groups = [aws_security_group.sg_ecs.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.cursoArqSoft_lb_tg.arn
    container_name   = "backend-procesamiento-score-container"
    container_port   = 80
  }
}




resource "aws_ecs_task_definition" "task_cursoArqSoft" {
  family                = "backend-procesamiento-score"
  network_mode          = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                    = tostring(1024*var.ecs_cpu_task)
  memory                 = tostring(1024*var.ecs_memory_task)
  execution_role_arn     = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn          = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      "name": "backend-procesamiento-score-container",
      "image": "538430999815.dkr.ecr.us-east-1.amazonaws.com/curso-arquitectura-software/score-crediticio:latest",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 80,
          "hostPort": 80
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-create-group": "true",
          "awslogs-group": "/ecs/backend-procesamiento-score-curso-arq-soft",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ])

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "X86_64"
  }
}


