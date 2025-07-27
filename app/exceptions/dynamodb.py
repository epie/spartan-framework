class DynamoDBConnectionError(Exception):
    """
    Exception raised when unable to connect to DynamoDB.

    This exception should be used when there are connectivity issues
    with DynamoDB, such as network problems, invalid endpoints,
    or authentication failures.

    Attributes:
        message (str): Explanation of the error.
    """


class DynamoDBTableNotFoundError(Exception):
    """
    Exception raised when a DynamoDB table is not found.

    This exception should be used when attempting to access a table
    that does not exist in the DynamoDB instance.

    Attributes:
        message (str): Explanation of the error.
        table_name (str): The name of the table that was not found.
    """

    def __init__(self, message: str, table_name: str = None):
        super().__init__(message)
        self.table_name = table_name


class DynamoDBInvalidTableNameError(Exception):
    """
    Exception raised when an invalid table name is provided.

    This exception should be used when the table name is empty,
    None, or contains invalid characters.

    Attributes:
        message (str): Explanation of the error.
        table_name (str): The invalid table name that was provided.
    """

    def __init__(self, message: str, table_name: str = None):
        super().__init__(message)
        self.table_name = table_name


class DynamoDBConfigurationError(Exception):
    """
    Exception raised when DynamoDB configuration is invalid.

    This exception should be used when there are issues with
    DynamoDB configuration such as invalid region names,
    missing environment variables, or invalid endpoint URLs.

    Attributes:
        message (str): Explanation of the error.
    """


class DynamoDBItemNotFoundError(Exception):
    """
    Exception raised when a DynamoDB item is not found.

    This exception should be used when querying for a specific
    item that does not exist in the table.

    Attributes:
        message (str): Explanation of the error.
        key (dict): The key used to search for the item.
    """

    def __init__(self, message: str, key: dict = None):
        super().__init__(message)
        self.key = key


class DynamoDBQueryError(Exception):
    """
    Exception raised when a DynamoDB query fails.

    This exception should be used when there are issues with
    query operations such as invalid query parameters,
    malformed conditions, or query execution failures.

    Attributes:
        message (str): Explanation of the error.
    """


class DynamoDBWriteError(Exception):
    """
    Exception raised when a DynamoDB write operation fails.

    This exception should be used when there are issues with
    write operations such as put_item, update_item, or delete_item.

    Attributes:
        message (str): Explanation of the error.
    """


class DynamoDBCapacityExceededError(Exception):
    """
    Exception raised when DynamoDB capacity is exceeded.

    This exception should be used when operations fail due to
    exceeding the provisioned or on-demand capacity limits.

    Attributes:
        message (str): Explanation of the error.
    """


class DynamoDBValidationError(Exception):
    """
    Exception raised when DynamoDB validation fails.

    This exception should be used when data validation fails
    before or after DynamoDB operations, such as invalid
    attribute types or constraint violations.

    Attributes:
        message (str): Explanation of the error.
    """
