resource "aws_db_parameter_group" "reto2_db_pg" {
  name   = "microservices-reto2-db-pg"
  family = "postgres17"

  parameter {
    name  = "log_connections"
    value = "1"
  }
}

resource "aws_db_subnet_group" "default" {
  name       = "microservices-reto2-subnet-group"
  subnet_ids = [aws_default_subnet.default_az1.id, aws_default_subnet.default_az2.id]  // You need at least 2 subnets in different AZs

  tags = {
    Name = "Microservices Reto2 DB subnet group"
  }
}

resource "aws_db_instance" "microservice_db" {
  identifier             = "microservices-reto2-db"
  instance_class         = "db.t3.micro"
  allocated_storage      = 5
  engine                 = "postgres"
  engine_version         = "17.3"
  username               = "arquitectura"
  password               = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.default.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  parameter_group_name   = aws_db_parameter_group.reto2_db_pg.name
  publicly_accessible    = true
  skip_final_snapshot    = true
}