import os
import json
import pickle
import pandas as pd

def loader(object_name: str):
    if not isinstance(object_name, str):
        raise ValueError("Object path is not a string")
    models_folder = os.path.relpath("models", os.getcwd())
    object_path = f"{models_folder}/{object_name}.pkl"
    try:
        with open(object_path, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Invalid object name.")

def predict(event, context):
    """
    Handler function to make predictions
    """
    if "body" not in event:
        return {
            "created_by": "Renatex",
            "message": "No body in the request",
            "error": "None",
            "prediction": "None"
        }

    try:
        body = json.loads(event["body"])
    except Exception as e:
        return {
            "created_by": "Renatex",
            "message": "Invalid body in the request",
            "error": f"{type(e).__name__}: {str(e)}",
            "prediction": "None"
        }
    
    try:
        model = loader("model")
        encoder = loader("encoder")
    except Exception as e:
        return {
            "created_by": "Renatex",
            "message": f"Error loading the model",
            "error": f"{type(e).__name__}: {str(e)}",
            "prediction": "None"
        }

    try:
        df_person = pd.DataFrame([body])
        person_t = encoder.transform(df_person)
        pred = model.predict(person_t)[0]
    except Exception as e:
        return {
            "created_by": "Renatex",
            "message": f"Invalid body in the request",
            "error": f"{type(e).__name__}: {str(e)}",
            "prediction": "None"
        }

    return {
        "created_by": "Renatex",
        "message": "Prediction made successfully",
        "error": "None",
        "prediction": str(pred)
    }
