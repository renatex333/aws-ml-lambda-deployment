"""
Module to create a new AWS Lambda function from ECR image
"""

import os
import boto3
import random
import string
from dotenv import load_dotenv, set_key

def main():
    load_dotenv()

    function_name = os.getenv("FUNCTION_NAME")

    # Provide Image URI
    version = "latest"
    image_uri = f"{os.getenv('REPOSITORY_URI')}:{version}"

    lambda_role_arn = os.getenv("AWS_LAMBDA_ROLE_ARN")

    lambda_client = boto3.client(
        "lambda",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    try:
        lambda_client.delete_function(FunctionName=function_name)
        print("Existing Function was Deleted!")
    except lambda_client.exceptions.ResourceNotFoundException:
        pass

    response = lambda_client.create_function(
        FunctionName=function_name,
        PackageType="Image",
        Code={"ImageUri": image_uri},
        Role=lambda_role_arn,
        Environment={
            "Variables": {
                "BUCKET_NAME": os.getenv("AWS_BUCKET_NAME"),
                "MODEL_PATH": os.getenv("MODEL_PATH"),
                "ENCODER_PATH": os.getenv("ENCODER_PATH"),
                "AWS_S3_ACCESS_KEY_ID": os.getenv("AWS_S3_ACCESS_KEY_ID"),
                "AWS_S3_SECRET_ACCESS_KEY": os.getenv("AWS_S3_SECRET_ACCESS_KEY"),
            }
        },
        Timeout=30,  # Optional: function timeout in seconds
        MemorySize=128,  # Optional: function memory size in megabytes
    )

    id_num = "".join(random.choices(string.digits, k=7))

    api_gateway_permissions = lambda_client.add_permission(
        FunctionName=function_name,
        StatementId="api-gateway-permission-statement-" + id_num,
        Action="lambda:InvokeFunction",
        Principal="apigateway.amazonaws.com",
    )

    print("Lambda Function Created Successfully!")
    print(f"Function Name: {response['FunctionName']}")
    print(f"Function ARN: {response['FunctionArn']}")
    set_key(".env", "\nFUNCTION_ARN", response["FunctionArn"])

if __name__ == "__main__":
    main()
