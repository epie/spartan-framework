from typing import Optional

import boto3

from app.exceptions.dynamodb import DynamoDBInvalidTableNameError
from app.helpers.environment import env


def ddb(
    table_name: str,
    region_name: Optional[str] = None,
    endpoint_url: Optional[str] = None,
):
    """
    Create and return a DynamoDB table resource.
    """

    if not table_name:
        raise DynamoDBInvalidTableNameError(
            "Table name must be a non-empty string", table_name
        )

    kwargs = {
        "service_name": "dynamodb",
        "region_name": region_name or env("DDB_REGION", "ap-southeast-1"),
    }

    if env("DDB_TYPE") == "local":
        kwargs["endpoint_url"] = endpoint_url or env(
            "DDB_ENDPOINT_URL", "http://localhost:8000"
        )

    return boto3.resource(**kwargs).Table(table_name)
