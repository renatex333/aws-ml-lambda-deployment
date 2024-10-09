import os
import boto3
import botocore
from dotenv import load_dotenv, set_key, unset_key

def main():
    load_dotenv()

    api_gateway_name = os.getenv("API_GATEWAY_NAME")

    api_gateway_client = boto3.client(
        "apigatewayv2",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    try:
        api_gateway_id = os.getenv("API_GATEWAY_ID")
        api_gateway_client.delete_api(ApiId=api_gateway_id)
        print("API Gateway Deleted!")
        unset_key(".env", "API_GATEWAY_ID")
        unset_key(".env", "API_GATEWAY_URL")
    except (api_gateway_client.exceptions.NotFoundException, botocore.exceptions.ParamValidationError):
        print(f"No existing API Gateway found with ID '{api_gateway_id}'.")

    lambda_function_arn = os.getenv("FUNCTION_ARN")
    api_route = "/predict"
    response = api_gateway_client.create_api(
        Name=api_gateway_name,
        ProtocolType="HTTP",
        Version="1.0",
        RouteKey=f"POST {api_route}",
        Target=lambda_function_arn,
    )

    api_id = response["ApiId"]
    api_endpoint = response["ApiEndpoint"] + api_route
    print("API Endpoint:", api_endpoint)
    set_key(".env", "\nAPI_GATEWAY_ID", api_id)
    set_key(".env", "\nAPI_GATEWAY_URL", api_endpoint)

if __name__ == "__main__":
    main()