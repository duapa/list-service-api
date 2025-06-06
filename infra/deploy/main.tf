resource "aws_lambda_function" "list_service_api" {
    function_name = "${var.env}_list_service_api"
    description   = "Lambda function for Strings API"
    role          = replace(var.execution_role_arn, "\"", "")
    package_type  = "Image"
    image_uri     = "${var.ecr_repo_url}:latest"
    timeout       = 10
}

data "aws_caller_identity" "current" {}


resource "aws_api_gateway_rest_api" "api" {
  name          = "list_service_api"
  description   = "HTTP API for list service"
  depends_on = [aws_lambda_function.list_service_api ]
}

# Create /items resource
resource "aws_api_gateway_resource" "items_resource" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  path_part   = "items"
}

# Create /head resource
resource "aws_api_gateway_resource" "head_resource" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  path_part   = "head"
}

# Create /tail resource
resource "aws_api_gateway_resource" "tail_resource" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  path_part   = "tail"
  depends_on = [ aws_api_gateway_rest_api.api]
}


# Create GET method for /items
resource "aws_api_gateway_method" "get_items_method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.items_resource.id
  http_method   = "GET"
  authorization = "NONE"
}


# Create /items/{item_id} resource
resource "aws_api_gateway_resource" "item_id_resource" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_resource.items_resource.id
  path_part   = "{item_id}"
}

# Create GET method for /items{item_id}
resource "aws_api_gateway_method" "get_item_id_method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.item_id_resource.id
  http_method   = "GET"
  authorization = "NONE"
}

# Create POST method for /items{item_id}
resource "aws_api_gateway_method" "post_items_method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.items_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

# Create PUT method for /items{item_id}
resource "aws_api_gateway_method" "put_items_method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.item_id_resource.id
  http_method   = "PUT"
  authorization = "NONE"
}

# Create DELETE method for /items
resource "aws_api_gateway_method" "delete_items_method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.item_id_resource.id
  http_method   = "DELETE"
  authorization = "NONE"
}

# Lambda Integration for GET /items
resource "aws_api_gateway_integration" "get_item_id_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.item_id_resource.id
  http_method             = aws_api_gateway_method.get_item_id_method.http_method
  integration_http_method = "POST"  
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.list_service_api.arn}/invocations"
}

resource "aws_api_gateway_integration" "get_items_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.items_resource.id
  http_method             = aws_api_gateway_method.get_items_method.http_method
  integration_http_method = "POST"  
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.list_service_api.arn}/invocations"
}

# Lambda Integration for POST /items
resource "aws_api_gateway_integration" "post_items_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.items_resource.id
  http_method             = aws_api_gateway_method.post_items_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.list_service_api.arn}/invocations"
}

# Lambda Integration for PUT /items
resource "aws_api_gateway_integration" "put_items_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.item_id_resource.id
  http_method             = aws_api_gateway_method.put_items_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.list_service_api.arn}/invocations"
}

# Lambda Integration for DELETE /items
resource "aws_api_gateway_integration" "delete_items_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.item_id_resource.id
  http_method             = aws_api_gateway_method.delete_items_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.list_service_api.arn}/invocations"
}

resource "aws_api_gateway_method" "get_head_method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.head_resource.id
  http_method   = "GET"
  authorization = "NONE"
  depends_on = [  aws_api_gateway_resource.head_resource]
}


resource "aws_api_gateway_method" "get_tail_method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.tail_resource.id
  http_method   = "GET"
  authorization = "NONE"
  depends_on = [  aws_api_gateway_resource.tail_resource]
}

# Lambda Integration for GET /head
resource "aws_api_gateway_integration" "get_head_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.head_resource.id
  http_method             = aws_api_gateway_method.get_head_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.list_service_api.arn}/invocations"
  depends_on = [ aws_api_gateway_method.get_head_method ]
}

# Lambda Integration for GET /tail
resource "aws_api_gateway_integration" "get_tail_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.tail_resource.id
  http_method             = aws_api_gateway_method.get_tail_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.list_service_api.arn}/invocations"
  depends_on = [ aws_api_gateway_method.get_tail_method ]
}


resource "aws_api_gateway_deployment" "deployment" {
  rest_api_id = aws_api_gateway_rest_api.api.id

  depends_on = [
    aws_api_gateway_resource.head_resource,
    aws_api_gateway_resource.tail_resource,
    aws_api_gateway_method.get_tail_method,
    aws_api_gateway_method.get_head_method,
    aws_api_gateway_integration.get_tail_integration,
    aws_api_gateway_integration.get_head_integration,
    aws_api_gateway_integration.get_items_integration,
    aws_api_gateway_integration.post_items_integration,
    aws_api_gateway_integration.put_items_integration,
    aws_api_gateway_integration.delete_items_integration,
    aws_api_gateway_integration.get_item_id_integration
  ]
}


resource "aws_api_gateway_stage" "deploy_stage" {
  stage_name    = var.env
  rest_api_id   = aws_api_gateway_rest_api.api.id
  deployment_id = aws_api_gateway_deployment.deployment.id
}


resource "aws_lambda_permission" "allow_api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  principal     = "apigateway.amazonaws.com"
  function_name = aws_lambda_function.list_service_api.function_name
}
