resource "aws_lambda_function" "list_service_api" {
    function_name = "${var.env}_list_service_api"
    description   = "Lambda function for Strings API"
    role          = replace(var.execution_role_arn, "\"", "")
    package_type  = "Image"
    image_uri     = "${var.ecr_repo_url}:latest"
    timeout       = 10
}

