output "rds_hostname" {
  description = "RDS instance hostname"
  value       = aws_db_instance.microservice_db.address
  sensitive   = true
}

output "rds_port" {
  description = "RDS instance port"
  value       = aws_db_instance.microservice_db.port
  sensitive   = true
}

output "rds_username" {
  description = "RDS instance root username"
  value       = aws_db_instance.microservice_db.username
  sensitive   = true
}

output "instance_public_ips" {
  value = aws_instance.microservices.public_ip
}