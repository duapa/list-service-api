#!/bin/sh
TF_VAR_account_id=****
TF_VAR_region=****
TF_VAR_env=****

export TF_VAR_account_id
export TF_VAR_env
export TF_VAR_region

terraform -chdir=./infra/prerequisites init

terraform -chdir=./infra/prerequisites apply -auto-approve

TF_VAR_ecr_repo_url=$(terraform -chdir=./infra/prerequisites output -raw ecr_repo_url)
TF_VAR_execution_role_arn=$(terraform -chdir=./infra/prerequisites output -raw  lambda_exec_role_arn)

export TF_VAR_execution_role_arn
export TF_VAR_ecr_repo_url


# Build image and deploy to repo
DOCKER_ENDPOINT="$TF_VAR_account_id.dkr.ecr.$TF_VAR_region.amazonaws.com"
export DOCKER_ENDPOINT

aws ecr get-login-password --region "$TF_VAR_region" | docker login --username AWS --password-stdin "$DOCKER_ENDPOINT"

docker build -t list-service:latest .

docker tag list-service:latest "$TF_VAR_ecr_repo_url:latest"

docker push "$TF_VAR_ecr_repo_url:latest"

terraform -chdir=./infra/deploy init

terraform -chdir=./infra/deploy apply -auto-approve

