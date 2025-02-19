resource "aws_lb" "cursoArqSoft_lb" {
  name               = "cursoArqSoft-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.sg_alb_internet.id]
  subnets            = data.aws_subnets.default.ids
  enable_deletion_protection = false
}

resource "aws_lb_target_group" "cursoArqSoft_lb_tg" {
  name     = "cursoArqSoft-lb-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_default_vpc.default.id
  target_type = "ip"
  health_check {
    path                = "/health"
    protocol            = "HTTP"
    port                = "traffic-port"
    interval            = 60
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

resource "aws_lb_listener" "cursoArqSoft_listener" {
  load_balancer_arn = aws_lb.cursoArqSoft_lb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"`
    target_group_arn = aws_lb_target_group.cursoArqSoft_lb_tg.arn
    }
}
