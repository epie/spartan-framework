from .database import DatabaseInternalError
from .dynamodb import (
    DynamoDBCapacityExceededError,
    DynamoDBConfigurationError,
    DynamoDBConnectionError,
    DynamoDBInvalidTableNameError,
    DynamoDBItemNotFoundError,
    DynamoDBQueryError,
    DynamoDBTableNotFoundError,
    DynamoDBValidationError,
    DynamoDBWriteError,
)
from .user import DuplicateUserError, InvalidSortFieldError, UserNotFoundError

__all__ = [
    # Database exceptions
    "DatabaseInternalError",
    # User exceptions
    "DuplicateUserError",
    "InvalidSortFieldError",
    "UserNotFoundError",
    # DynamoDB exceptions
    "DynamoDBCapacityExceededError",
    "DynamoDBConfigurationError",
    "DynamoDBConnectionError",
    "DynamoDBInvalidTableNameError",
    "DynamoDBItemNotFoundError",
    "DynamoDBQueryError",
    "DynamoDBTableNotFoundError",
    "DynamoDBValidationError",
    "DynamoDBWriteError",
]
