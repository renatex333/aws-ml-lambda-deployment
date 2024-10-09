import os
import boto3
import botocore
from dotenv import load_dotenv, unset_key

def main():
    load_dotenv()

    # Provide function name
    function_name = os.getenv("AWS_LAMBDA_FUNCTION_NAME")

    # Create a Boto3 client for AWS Lambda
    lambda_client = boto3.client(
        "lambda",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    # Delete the Lambda function
    try:
        lambda_client.delete_function(FunctionName=function_name)
        print(f"Lambda function {function_name} deleted successfully")
        unset_key(".env", "FUNCTION_ARN")
    except (lambda_client.exceptions.ResourceNotFoundException, botocore.exceptions.ParamValidationError) as e:
        print("No existing function found.")

if __name__ == "__main__":
    main()
