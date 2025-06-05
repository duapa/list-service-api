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