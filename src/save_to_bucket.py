import os
import boto3
from hashlib import sha256
from dotenv import load_dotenv, set_key

def main():
    load_dotenv()
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_S3_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_S3_SECRET_ACCESS_KEY"),
    )
    bucket_name = os.getenv("AWS_BUCKET_NAME")
    models_dir = os.path.relpath("models", os.getcwd())
    for file in os.listdir(models_dir):
        if file.endswith(".pkl"):
            file_name = file.split(".")[0]
            local_model_path = os.path.join(models_dir, file)
            remote_model_path = f"renatolf1/{file}"
            with open(local_model_path, "rb") as f:
                model_hash = sha256(f.read()).hexdigest()
            print(f"Saving {file} to bucket {bucket_name} on {remote_model_path}...")
            s3.upload_file(
                Filename=local_model_path,
                Bucket=bucket_name,
                Key=remote_model_path,  # Key (path on bucket)
            )

            obj = s3.get_object(
                Bucket=bucket_name,
                Key=remote_model_path,
            )
            if sha256(obj["Body"].read()).hexdigest() == model_hash:
                print(f"Model {file} saved successfully!")
                set_key(".env", f"{file_name.upper()}_PATH", remote_model_path)
            else:
                print(f"Error saving {file}!")
    
if __name__ == "__main__":
    main()
