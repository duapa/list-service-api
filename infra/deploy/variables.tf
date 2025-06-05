variable "region" {
    description = "The AWS region to deploy resources in."
    type        = string
}

variable "env" {
    description = "The environment for the deployment (e.g., dev, staging, prod)."
    type        = string
}

variable "account_id" {
    description = "The AWS account ID where resources will be deployed."
    type        = string
}

variable "ecr_repo_url" {
    description = "The URL of the ECR repository where the Docker image is stored."
    type        = string
}

variable "execution_role_arn" {
    description = "The ARN of the IAM role that Lambda functions will assume."
    type        = string
}