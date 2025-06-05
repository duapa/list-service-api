output "ecr_repo_url" {
  value = "${aws_ecr_repository.list_service_repo.repository_url}"
  sensitive = false
}

output "lambda_exec_role_arn" {
  value = aws_iam_role.lambda_exec_role.arn
  sensitive = false
}