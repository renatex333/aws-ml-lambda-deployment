"""
Module to create a repository in ECR
"""

import os
import boto3
from dotenv import load_dotenv, set_key

def main():
    load_dotenv()

    repository_name = os.getenv("REPOSITORY_NAME")

    ecr_client = boto3.client(
        "ecr",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )

    response = ecr_client.create_repository(
        repositoryName=repository_name,
        imageScanningConfiguration={"scanOnPush": True},
        imageTagMutability="MUTABLE",
    )

    print(response)

    print(f"\nrepositoryArn: {response['repository']['repositoryArn']}")
    print(f"repositoryUri: {response['repository']['repositoryUri']}")
    set_key(".env", "\nREPOSITORY_URI", response["repository"]["repositoryUri"])

if __name__ == "__main__":
    main()
