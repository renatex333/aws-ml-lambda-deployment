import os
import io
import json
import boto3
from dotenv import load_dotenv

def main():
    load_dotenv()

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
    test_function_with_payload(lambda_client, function_name)

def test_function_basic_reponse(lambda_client, function_name):

    assert function_exists(lambda_client, function_name) == True, f"Function {function_name} does not exist"

    response = function_invoke(lambda_client, function_name)
    assert response is not None, "Function did not return a response"
    response = json.loads(response)
    print(response)
    assert response["message"] == "No body in the request", "Function did not return the expected message"

def test_function_with_payload(lambda_client, function_name):
    payload = {
        "body": json.dumps({
            "age": 42,
            "job": "entrepreneur",
            "marital": "married",
            "education": "primary",
            "balance": 558,
            "housing": "yes",
            "duration": 186,
            "campaign": 2
        })
    }
    response = function_invoke(lambda_client, function_name, payload)
    assert response is not None, "Function did not return a response"
    response = json.loads(response)
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
            Payload=json.dumps(payload),
        )

        return io.BytesIO(response["Payload"].read()).read().decode("utf-8")

    except Exception as e:
        print(e)
        return None

if __name__ == "__main__":
    main()
