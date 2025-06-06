from aws_lambda_powertools import Logger, Metrics

service_name = "ListService"
logger = Logger(service=service_name)
metrics = Metrics(service=service_name)
