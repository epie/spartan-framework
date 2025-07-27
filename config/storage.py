from app.helpers.environment import env


class StorageSettings:
    enabled: bool = env("STORAGE_ENABLED", False)
    type: str = env("STORAGE_TYPE", "local")
    bucket: str = env("STORAGE_BUCKET", "")
    path: str = env("STORAGE_PATH", "storage/core")
