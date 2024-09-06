import os
import json
import boto3
import pickle
import pandas as pd

S3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_S3_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_S3_SECRET_ACCESS_KEY"),
    )

def loader(object_path: str):
    """
    Load the object from S3 Bucket
    """
    bucket_name = os.getenv("BUCKET_NAME")
    key = os.getenv(object_path)

    # Make sure bucket_name and key are valid
    if not isinstance(bucket_name, str) or not isinstance(key, str):
        raise ValueError("Bucket name or key is not a string")

    obj = S3.get_object(
        Bucket=bucket_name,
        Key=key,
    )
    file_content = obj["Body"].read()
    file = pickle.loads(file_content)
    return file

def predict(event, context):
    """
    Handler function to make predictions
    """
    if "body" not in event:
        return {
            "created_by": "Renatex",
            "message": "No body in the request",
            "prediction": "None"
        }
    # Load data
    body = json.loads(event["body"])
    # Load the model and encoder from S3
    model = loader("MODEL_PATH")
    encoder = loader("ENCODER_PATH")
    # Make predictions
    df_person = pd.DataFrame([body])
    person_t = encoder.transform(df_person)
    pred = model.predict(person_t)[0]
    
    return {
        "created_by": "Renatex",
        "message": "Prediction made successfully",
        "prediction": str(pred)
    }
