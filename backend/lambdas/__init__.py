import boto3
import os

# Centralized AWS clients
sns_client = boto3.client(
    "sns",
    region_name=os.getenv("AWS_REGION", "us-east-1"),
)

eventbridge_client = boto3.client(
    "events",
    region_name=os.getenv("AWS_REGION", "us-east-1"),
)
