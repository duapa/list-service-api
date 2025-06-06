resource "aws_ecr_repository" "list_service_repo" {
  name = "${var.env}_list_service_repo"
}

resource "aws_iam_role" "lambda_exec_role" {
  name = "${var.env}_lambda_exec_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/${var.env}_list_service"
  retention_in_days = 14
}


resource "aws_cloudwatch_log_stream" "lambda_log_stream" {
  log_group_name = aws_cloudwatch_log_group.lambda_log_group.name
  name="list_service_log_stream"
}


resource "aws_iam_policy" "lambda_custom_policy" {
  name = "${var.env}_lambda_exec_policy"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "${aws_cloudwatch_log_group.lambda_log_group.arn}:*"
      },
      {
        Effect = "Allow",
        Action = "logs:DescribeLogGroups",
        Resource = "*"
      },
      {
        Effect = "Allow",
        Action = [
          "ecr:GetAuthorizationToken"
        ],
        Resource = "*"
      },
      {
        Effect = "Allow",
        Action = [
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage"
        ],
        Resource = aws_ecr_repository.list_service_repo.arn
      }
    ]
  })

  depends_on = [ aws_cloudwatch_log_group.lambda_log_group, aws_ecr_repository.list_service_repo ]
}

# Role assignment for the Lambda function
resource "aws_iam_role_policy_attachment" "lambda_role_policy_attachment" {
    role       = aws_iam_role.lambda_exec_role.name
    policy_arn = aws_iam_policy.lambda_custom_policy.arn
    depends_on = [ aws_iam_policy.lambda_custom_policy, aws_iam_role.lambda_exec_role ]
}

