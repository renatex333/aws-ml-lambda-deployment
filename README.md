# Machine Learning on AWS

Welcome to this ML + AWS project!

This project integrates Machine Learning (ML) with AWS services to deploy a model as a Lambda function using Docker containers. The project automates the creation of AWS resources such as an Elastic Container Registry (ECR) repository, Lambda functions, and an API Gateway. The ML model is trained, stored in an S3 bucket, and predictions are made using an API endpoint exposed through the Lambda function.

The project structure is modular, including source code, models and unit tests to ensure stability. It utilizes the AWS CLI for configuration management and Docker for local testing and deployment.

## Installing Dependencies

To install the project dependencies, use the `requirements.txt` file:

```sh
pip install -r requirements.txt
```

## Project Structure

- `models`: Contains the machine learning models and encoders.
- `src`: Contains the main source code to deploy the function and API on the AWS.
- `tests`: Contains unit and integration tests to guarantee code stability.

## Usage

### Configure your AWS CLI

Having [AWS CLI installed](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html), configure your credentials on a profile:
```bash
aws configure --profile mlops
```

To set it as deafult profile:

Linux:
```bash
export AWS_PROFILE=mlops
```

Windows CMD:
```bash
set AWS_PROFILE=mlops
```

Windows PowerShell:
```bash
$env:AWS_PROFILE = "mlops"
```

### Create and Configure ECR repository

To set up the project, let's build the Docker image from the `Dockerfile` with the `test` tag.
```bash
docker build --platform linux/amd64 -t lambda-predict-image:test .
```

Testing Container Application locally:
```bash
docker run -p 9500:8080 lambda-predict-image:test
curl "http://localhost:9500/2015-03-31/functions/function/invocations" -d "{}"
curl -X POST -H "Content-Type: application/json" -d '{"body": "{\"age\": 42, \"job\": \"entrepreneur\", \"marital\": \"married\", \"education\": \"primary\", \"balance\": 558, \"housing\": \"yes\", \"duration\": 186, \"campaign\": 2}"}' "http://localhost:9500/2015-03-31/functions/function/invocations"
```

Then run the following script to create a repository in AWS ECR:

> [!NOTE]  
> Save the `REPOSITORY_URI`.

```bash
python3 src/create_repository.py
```

Then login to ECR using the Docker CLI:

> [!IMPORTANT]  
> Substitute `AWS_ACCOUNT_ID` for your AWS Account ID.

```bash
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin AWS_ACCOUNT_ID.dkr.ecr.us-east-2.amazonaws.com
```

Rebuild your Docker image (if needed), tag your local Docker image (`Dockerfile`) into the repository as the latest version and push the image:

> [!IMPORTANT]  
> Substitute `REPOSITORY_URI` for the correct repository's URI.

```bash
docker build --platform linux/amd64 -t lambda-predict-image:test .

docker tag lambda-predict-image:test REPOSITORY_URI:latest

docker push REPOSITORY_URI:latest
```

### Create Lambda Function

To create a Lambda function from the ECR image, run:

```bash
python3 src/create_function.py
```

### Create API Gateway

To create an API Gateway that exposes the Lambda function, run:

```bash
python3 src/create_api.py
```

#### Local Testing

To test the function locally, use:

```bash
pytest
```

#### Remote Testing

After deploying the Lambda function and API Gateway, you can verify the setup by running:

```bash
pytest --local
```

The `--local` flag ensures that tests requiring local resources, such as environment variables, are executed.

# References

- [AWS Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [AWS Lambda Layers Documentation](https://docs.aws.amazon.com/lambda/latest/dg/chapter-layers.html)
- [API Gateway Documentation](https://docs.aws.amazon.com/apigateway/)
- [Pytest Documentation](https://docs.pytest.org/en/stable/)
