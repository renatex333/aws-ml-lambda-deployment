import os
import boto3
from dotenv import load_dotenv, set_key

def main():
    load_dotenv()

    api_gateway_name = os.getenv("API_GATEWAY_NAME")

    api_gateway_client = boto3.client(
        "apigatewayv2",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    api_gateway_id = os.getenv("API_GATEWAY_ID")
    if api_gateway_id:
        try:
            api_gateway_client.delete_api(ApiId=api_gateway_id)
            print("API Gateway Deleted!")
        except api_gateway_client.exceptions.NotFoundException as e:
            print("Error deleting API Gateway:", e)

    lambda_function_arn = os.getenv("FUNCTION_ARN")
    api_route = "/predict"
    api_gateway_create = api_gateway_client.create_api(
        Name=api_gateway_name,
        ProtocolType="HTTP",
        Version="1.0",
        RouteKey=f"POST {api_route}",
        Target=lambda_function_arn,
    )

    print("API Endpoint:", api_gateway_create["ApiEndpoint"] + api_route)
    set_key(".env", "\nAPI_GATEWAY_ID", api_gateway_create["ApiId"])
    set_key(".env", "\nAPI_GATEWAY_URL", api_gateway_create["ApiEndpoint"] + api_route)

if __name__ == "__main__":
    main()