import os
import boto3
import botocore
from dotenv import load_dotenv, unset_key

def main():
    load_dotenv()

    api_gateway_name = os.getenv("AWS_API_GATEWAY_NAME")
    api_gateway_id = os.getenv("API_GATEWAY_ID")

    api_gateway_client = boto3.client(
        "apigatewayv2",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    # Delete the API Gateway
    try:
        api_gateway_client.delete_api(ApiId=api_gateway_id)
        print(f"API Gateway '{api_gateway_name}' deleted successfully.")
        unset_key(".env", "API_GATEWAY_ID")
        unset_key(".env", "API_GATEWAY_URL")
    except (api_gateway_client.exceptions.NotFoundException, botocore.exceptions.ParamValidationError):
        print(f"API Gateway '{api_gateway_name}' with ID '{api_gateway_id}'not found.")

if __name__ == "__main__":
    main()
