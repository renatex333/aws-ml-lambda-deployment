import os
import io
import json
import boto3
import requests
from dotenv import load_dotenv

def main():
    load_dotenv()

    # Payload
    payload = json.dumps({
        "age": 42,
        "job": "entrepreneur",
        "marital": "married",
        "education": "primary",
        "balance": 558,
        "housing": "yes",
        "duration": 186,
        "campaign": 2
    })

    # Create a Boto3 client for AWS Lambda
    lambda_client = boto3.client(
        "lambda",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    # Lambda function name
    function_name = os.getenv("FUNCTION_NAME")

    # Test the function
    test_function_basic_reponse(lambda_client, function_name)
    test_function_with_payload(lambda_client, function_name, payload)

    # Close the Lambda client
    lambda_client.close()

    # API Gateway URL
    url = os.getenv("API_GATEWAY_URL")
    test_api_basic_response(url)
    test_api_with_payload(url, payload)

def test_function_basic_reponse(lambda_client, function_name):

    assert function_exists(lambda_client, function_name) == True, f"Function {function_name} does not exist"

    response = function_invoke(lambda_client, function_name)
    assert response is not None, "Function did not return a response"
    response = json.loads(response)
    print("Test function basic response")
    print(response)
    assert response["message"] == "No body in the request", "Function did not return the expected message"

def test_function_with_payload(lambda_client, function_name, payload):
    payload = json.dumps({"body": payload})
    response = function_invoke(lambda_client, function_name, payload)
    assert response is not None, "Function did not return a response"
    response = json.loads(response)
    print("Test function with payload")
    print(response)
    assert response["prediction"] != "None", "Function did not return a prediction"

def function_exists(lambda_client, function_name) -> bool:
    """
    Check if the function exists
    """
    try:
        lambda_client.get_function(FunctionName=function_name)
        return True
    except lambda_client.exceptions.ResourceNotFoundException:
        return False
    
def function_invoke(lambda_client, function_name, payload="") -> dict:
    """
    Invoke the function
    """
    try:
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType="RequestResponse",
            Payload=payload,
        )

        return io.BytesIO(response["Payload"].read()).read().decode("utf-8")

    except Exception as e:
        print(e)
        return None

def test_api_basic_response(url):
    response = requests.post(url)
    status_code = response.status_code
    response = json.loads(response.text)
    print("Test API basic response")
    print(response)
    assert status_code == 200, "Status code is not 200"
    assert response["message"] == "No body in the request", "API did not return the expected message"

def test_api_with_payload(url, payload):
    response = requests.post(url, json=json.loads(payload))
    status_code = response.status_code
    response = json.loads(response.text)
    print("Test API with payload")
    print(response)
    assert status_code == 200, "Status code is not 200"
    assert response["prediction"] != "None", "API did not return a prediction"    

if __name__ == "__main__":
    main()
