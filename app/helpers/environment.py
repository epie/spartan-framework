from functools import lru_cache
from typing import Optional

from dotenv import load_dotenv
from pydantic import ConfigDict, field_validator
from pydantic_settings import BaseSettings

load_dotenv(dotenv_path=".env")


class EnvironmentVariables(BaseSettings):
    """
    EnvironmentVariables is a configuration class for managing application environment variables.
    Attributes:
        APP_NAME (str): The name of the application.
        APP_ENVIRONMENT (str): The current environment (e.g., development, production).
        APP_DEBUG (bool): Flag to enable or disable debug mode.
        APP_MAINTENANCE (bool): Flag to enable or disable maintenance mode. Defaults to False.
        ALLOWED_ORIGINS (str): Comma-separated list of allowed CORS origins.
        LOG_LEVEL (str): Logging level (e.g., INFO, DEBUG).
        LOG_CHANNEL (str): Logging channel or handler.
        LOG_DIR (str): Directory path for storing log files.
        DB_TYPE (str): Database type (e.g., postgres, mysql).
        DB_DRIVER (str): Database driver.
        DB_HOST (str): Database host address.
        DB_PORT (Optional[int]): Database port number. Defaults to None.
        DB_NAME (str): Database name.
        DB_USERNAME (str): Database username.
        DB_PASSWORD (str): Database password.
        DB_SSL_CA (Optional[str]): Path to the SSL CA certificate for the database. Defaults to None.
        DB_SSL_VERIFY_CERT (Optional[bool]): Whether to verify the database SSL certificate. Defaults to None.
        STORAGE_ENABLED (bool): Flag to enable or disable storage. Defaults to False.
        STORAGE_TYPE (str): Type of storage backend. Defaults to "local".
        STORAGE_BUCKET (Optional[str]): Storage bucket name (if applicable). Defaults to None.
        STORAGE_PATH (str): Path for storage. Defaults to "storage/core".
    Class Attributes:
        model_config (ConfigDict): Configuration for environment file and encoding.
    Methods:
        default_db_port(cls, v): Validator to ensure DB_PORT is an integer or None.
    """

    APP_NAME: str
    APP_ENVIRONMENT: str
    APP_DEBUG: bool
    APP_MAINTENANCE: bool = False
    ALLOWED_ORIGINS: str

    LOG_LEVEL: str
    LOG_CHANNEL: str
    LOG_DIR: str

    DB_TYPE: str
    DB_DRIVER: str
    DB_HOST: str
    DB_PORT: Optional[int] = None
    DB_NAME: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_SSL_CA: Optional[str] = None
    DB_SSL_VERIFY_CERT: Optional[bool] = None

    STORAGE_ENABLED: bool = False
    STORAGE_TYPE: str = "local"
    STORAGE_BUCKET: Optional[str] = None
    STORAGE_PATH: str = "storage/core"

    DDB_TYPE: Optional[str] = "local"
    DDB_HOST: Optional[str] = "localhost"
    DDB_PORT: Optional[int] = 8000
    DDB_REGION: Optional[str] = "ap-southeast-1"
    DDB_TABLE_NAME: Optional[str] = "spartan"

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")

    @field_validator("DB_PORT", mode="before")
    def default_db_port(cls, v):
        try:
            return int(v)
        except (TypeError, ValueError):
            return None


@lru_cache()
def env(
    var_name: Optional[str] = None, default: Optional[str] = None
) -> Optional[str]:
    """
    Create and return an instance of EnvironmentVariables or a specific environment variable.

    This function initializes and returns an EnvironmentVariables object,
    which is used to manage and access environment variables for the application.
    If a variable name is provided, it returns the value of that specific environment variable.
    If the variable is not found, it returns the provided default value.

    Args:
        var_name (Optional[str]): The name of the environment variable to retrieve.
        default (Optional[str]): The default value to return if the variable is not found.
        Defaults to None.

    Returns:
        EnvironmentVariables or Optional[str]: An instance of the EnvironmentVariables
        class or the value of the specified environment variable, or the default value if not found.
    """
    env_vars = EnvironmentVariables()
    if var_name:
        return getattr(env_vars, var_name, default)
    return env_vars
