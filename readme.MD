# List Service API

This demo creates a dockerized web application for managing of strings, deploys it to AWS Lambda and makes the API available using AWS API Gateway.

## Specifications for the API
1. Show the head(top n elements) of a list of strings
1. Show the tail(bottom n elements) of a list of strings
1. Allow API user to add update and delete items in the list

## API Design
The following details the design of the API

* /items : GET : Gets all elements in the list without ordering
* /item/{item_id}: GET: 

| Endpoint| Method | Comment | Returns
|----------|----------|----------|---|
|/head?num_samples=n|GET|Gets the top `n` elements|List of json objects with attributes {id:value}|
|/tail?num_samples=n|GET|Gets the bottom `n` elements|List of json objects with attributes {id:value}|
|/items         |GET          | Gets all elements without ordering|List of json objects with attributes {id:value} 
|/items/{item_id}          |GET          |Get one particular item |Json object with attributes {id:value}|
|/items/{item_id}          |PUT         |Updates an item|Accepts `item_id` and  data of the format `{"value": "some_string"}`|
|/items/{item_id}          |DELETE         |Deletes an item|Accepts `item_id`|
|/items          |POST          |Inserts data into the list   | Data must be of the format `{"value": "some_string"}`|

The full openapi spec is available at [./openapi.yaml](./openapi.yaml)

# Solution Design
In order to minimize boilerplate code especially when it comes to managing routes, I decided to go with a dockerized FastAPI solution which is a familiar and performant python api framework. The solution can be easily dockerized and deployed to any containerization platform. The application is divied into **routes** and a **service** which serves as a domain object, sitting between the routing system and the database

## On choice for an In Memory Database
For a simple project like this, an in memory database can facilitate development and testing. The database persistence layer is built around the **Repository Pattern** which ensures that changes in database technology can handled in the future. This allows us to focus on the core ideas of the solution and not get too bogged down in the details. Because of the use of a supporting interface, the move to any specific database technology can easily be handled by adding a new Repository for say 'DyanamoDB' or 'Postgres'

## Local development
This package uses Python v3.12.3
* In the root folder create a python virtual environment using `python -m venv venv`
* Activate the virtual environment using `source venv/bin/activate`
* Install the python dependencies in [./requirements-dev.txt](./requirements-dev.txt) and [./requirements.txt](./requirements.txt)
* For building the docker images an installation of Docker will be required
* For terraform install v1.12.1 or a compatible version


# Testing
The solution is supported by a set of unit tests for the service layer and integration tests for the API. 

Tests on the local machine can be run using Pytest
```sh
$ pytest . 
```

# Deploying to AWS
The application deploys the following to AWS
- An ECR Repo
- A Lambda Execution Role which gives the application rights within AWS to CloudWatch, Pull images from ECR among others
- An AWS lambda function which runs the dockerized version of our artifact
- An AWS API Gateway which routes public web requests to the lambda function

See [terraform templates for supporting resources](./infra/prerequisites/) and [terraform templates for lambda function and API Gateway](./infra/deploy/)

This assumes that you have setup AWS Credentials with enough rights to deploy the above mentioned resources and have configured your AWS CLI

* Modify the [./deploy_aws_resources.sh](./deploy_aws_resources.sh) to update your account id, region and environment(loca|dev|test|prod)
* Run the script using `./deploy_aws_resources.sh` to deploy the resources to AWS
* In API Gateway deploy the stage(local|dev|test|prod) of the to launch the resulting endpoints across the internet
* You can use Postman(the openapi spec may help here), or AWS API Gateway to test the endpoints

# Some thoughts
This was a generally fulfilling exercise for Cloud based development, I got to build  a testable API in a dockerized Python environment. Being that I am quite new to terraform, I spent a considerable amount of time figuring out its kinks but the experience was rewarding. GitHub actions was a bit of a disappointment. Eventhough I enjoyed working with it I was not able to use it as I had hoped. I intended to have a CICD pipeline (see [workflows](/.github/workflows/)) in GHA deploy the resources using terraform to AWS, but the terraform related tasks just took too long and I had to abandon it due to practicality reasons. Between the routes, docker and API Gateway, making the final deploy to a website was also quite challenging, but I am happy to have completed it.
## Improvements
* Metrics to CW Metrics could be added to this solution
* Github Action to automate CICD
* Could have added a real database to persist the string data


