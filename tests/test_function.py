import json
import pytest
import lambda_function

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

def test_no_body_in_request():
    """
    Tests the lambda function with no body in the request
    """
    event = {}

    expected = {
        "created_by": "Renatex",
        "message": "No body in the request",
        "error": "None",
        "prediction": "None"
    }

    # Test if return is as expected
    assert lambda_function.predict(event, None) == expected

def test_invalid_body():
    """
    Tests the lambda function with invalid body in the request
    """
    event = {
        "body": "invalid"
    }

    response = lambda_function.predict(event, None)
    assert response["error"] != "None", f"Error is None. Should be an error message. Message: {response['message']}"

def test_invalid_payload():
    """
    Tests the lambda function with invalid payload in the request
    """
    payload = load_invalid_payload()
    event = {
        "body": payload
    }

    response = lambda_function.predict(event, None)
    assert response["error"] != "None", f"Error is None. Should be an error message. Message: {response['message']}"

def test_valid_payload():
    """
    Tests the lambda function with valid payload in the request
    """
    payload = load_valid_payload()
    event = {
        "body": payload
    }

    response = lambda_function.predict(event, None)
    assert response["prediction"] != "None", f"Prediction is None. Should be a prediction. Error: {response['error']}"

def test_loader_invalid_input():
    """
    Tests the loader function with invalid input
    """
    with pytest.raises(FileNotFoundError):
        lambda_function.loader("invalid_model")

def test_loader_valid_input():
    """
    Tests the loader function with valid input
    """
    model = lambda_function.loader("model")
    encoder = lambda_function.loader("encoder")

    assert model is not None, "Model is None. Should be a model."
    assert encoder is not None, "Encoder is None. Should be an encoder."
