import os
import io
import json
import boto3
import requests
import pytest
from dotenv import load_dotenv
import lambda_function

def load_lambda_client():
    """
    Create a new Lambda client and return it.
    """
    load_dotenv()

    lambda_client = boto3.client(
        "lambda",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    return lambda_client

def load_valid_payload():
    """
    Return a payload to test the function and the API.
    """
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
    return payload

def load_invalid_payload():
    """
    Return an invalid payload to test the function and the API.
    """
    payload = json.dumps({
        "age": "42"
    })
    return payload

def load_function_name():
    """
    Return the Lambda function name.
    """
    load_dotenv()
    function_name = os.getenv("FUNCTION_NAME")
    return function_name

def load_api_url():
    """
    Return the API Gateway URL.
    """
    load_dotenv()
    url = os.getenv("API_GATEWAY_URL")
    return url

def function_invoke(lambda_client, function_name, payload="") -> tuple[str, bool]:
    """
    Invoke the function.
    Returns a tuple with:
    - The response (json string or error message);
    - A boolean indicating if the function was successful.
    """
    try:
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType="RequestResponse",
            Payload=payload,
        )

        return io.BytesIO(response["Payload"].read()).read().decode("utf-8"), True

    except Exception as e:
        return e, False

@pytest.mark.local
def test_function_exists():
    """
    Check if the function exists.
    """
    lambda_client = load_lambda_client()
    function_name = load_function_name()

    exists = False
    report = "Function does not exist."
    try:
        lambda_client.get_function(FunctionName=function_name)
        exists = True
    except lambda_client.exceptions.ResourceNotFoundException as not_found:
        report = f"Function {function_name} does not exist. Exception: {not_found}"
    except Exception as exception:
        report = f"Function {function_name} does not exist. Exception: {exception}"
    assert exists, report

@pytest.mark.local
def test_function_basic_reponse():
    """
    Test the function with no payload.
    """
    lambda_client = load_lambda_client()
    function_name = load_function_name()

    response, status = function_invoke(lambda_client, function_name)
    assert status, f"Function did not return a valid response. Response: {response}"

    response = json.loads(response)
    assert response["message"] == "No body in the request", f"Function did not return the expected message. Message: {response['message']}"

@pytest.mark.local
def test_function_with_valid_payload():
    """
    Test the function with a valid payload.
    """
    lambda_client = load_lambda_client()
    function_name = load_function_name()
    payload = load_valid_payload()
    body = json.dumps({"body": payload})
    response, status = function_invoke(lambda_client, function_name, body)
    assert status, f"Function did not return a valid response. Response: {response}"

    response = json.loads(response)
    assert response["prediction"] != "None", f"Function did not return a prediction. Prediction: {response['prediction']}"

@pytest.mark.local
def test_function_with_invalid_payload():
    """
    Test the function with an invalid payload.
    """
    lambda_client = load_lambda_client()
    function_name = load_function_name()
    payload = load_invalid_payload()
    body = json.dumps({"body": payload})
    response, status = function_invoke(lambda_client, function_name, body)
    assert status, f"Function did not return a valid response. Response: {response}"

    response = json.loads(response)
    assert response["prediction"] == "None", f"Function did not return the expected response. Message: {response['message']}"

@pytest.mark.local
def test_api_basic_response():
    """
    Test the API with no payload.
    """
    url = load_api_url()
    response = requests.post(url, timeout=5)
    status_code = response.status_code
    assert status_code == 200, f"Status code is not 200. Status Code: {status_code}"

    response = json.loads(response.text)
    assert response["message"] == "No body in the request", f"API did not return the expected message. Message: {response['message']}"

@pytest.mark.local
def test_api_with_valid_payload():
    """
    Test the API with a valid payload.
    """
    url = load_api_url()
    payload = load_valid_payload()
    response = requests.post(url, json=json.loads(payload), timeout=5)
    status_code = response.status_code
    assert status_code == 200, "Status code is not 200"

    response = json.loads(response.text)
    assert response["prediction"] != "None", f"API did not return a prediction. Response: {response}"

@pytest.mark.local
def test_api_with_invalid_payload():
    """
    Test the API with a invalid payload.
    """
    url = load_api_url()
    payload = load_invalid_payload()
    response = requests.post(url, json=json.loads(payload), timeout=5)
    status_code = response.status_code
    assert status_code == 200, "Status code is not 200"

    response = json.loads(response.text)
    assert response["prediction"] == "None", f"Function did not return the expected response. Message: {response['message']}"
