"""
Unit tests for app/services/logging/gcloud.py GCloudLogger.
Tests initialization, logging methods, sampling, PII sanitization, and error handling.
"""

import os
from unittest.mock import MagicMock

import pytest

from app.services.logging.gcloud import GCP_LOGGING_AVAILABLE, GCloudLogger


def test_gcloud_logger_import_error_when_unavailable(mocker):
    """Test GCloudLogger raises ImportError when google-cloud-logging not available."""
    mocker.patch("app.services.logging.gcloud.GCP_LOGGING_AVAILABLE", False)

    with pytest.raises(ImportError) as exc_info:
        GCloudLogger("test-service")

    assert "Google Cloud Logging dependencies not available" in str(exc_info.value)


@pytest.mark.skipif(
    not GCP_LOGGING_AVAILABLE, reason="google-cloud-logging not installed"
)
def test_gcloud_logger_initialization(mocker):
    """Test GCloudLogger initializes with service name, level, and sample rate."""
    mock_client = MagicMock()
    mock_handler = MagicMock()

    mocker.patch(
        "app.services.logging.gcloud.gcp_logging.Client", return_value=mock_client
    )
    mocker.patch(
        "app.services.logging.gcloud.CloudLoggingHandler", return_value=mock_handler
    )
    mocker.patch("app.services.logging.gcloud.env", return_value="production")

    logger = GCloudLogger("my-service", level="DEBUG", sample_rate=0.5)

    assert logger.service_name == "my-service"
    assert logger.level == "DEBUG"
    assert logger.sample_rate == 0.5
    assert logger.logger is not None


@pytest.mark.skipif(
    not GCP_LOGGING_AVAILABLE, reason="google-cloud-logging not installed"
)
def test_gcloud_logger_setup_fallback_on_exception(mocker):
    """Test GCloudLogger falls back to standard logging when GCP setup fails."""
    # Mock Client to raise exception
    mocker.patch(
        "app.services.logging.gcloud.gcp_logging.Client",
        side_effect=Exception("GCP error"),
    )

    def mock_env(key, default=None):
        return {
            "LOG_SAMPLE_RATE": "1.0",
            "APP_ENVIRONMENT": "test",
            "APP_VERSION": "1.0",
        }.get(key, default)

    mocker.patch("app.services.logging.gcloud.env", side_effect=mock_env)

    # Capture print output
    mock_print = mocker.patch("builtins.print")

    logger = GCloudLogger("test-service")

    # Verify fallback occurred
    assert "gcloud_fallback" in logger.logger.name
    mock_print.assert_any_call(
        "Warning: Failed to setup Google Cloud Logging: GCP error"
    )
    mock_print.assert_any_call("Falling back to standard logging...")


@pytest.mark.skipif(
    not GCP_LOGGING_AVAILABLE, reason="google-cloud-logging not installed"
)
def test_gcloud_logger_sanitize_extra_data(mocker):
    """Test _sanitize_extra_data redacts sensitive fields."""
    mocker.patch("app.services.logging.gcloud.gcp_logging.Client")
    mocker.patch("app.services.logging.gcloud.CloudLoggingHandler")

    def mock_env(key, default=None):
        return {
            "LOG_SAMPLE_RATE": "1.0",
            "APP_ENVIRONMENT": "test",
            "APP_VERSION": "1.0",
        }.get(key, default)

    mocker.patch("app.services.logging.gcloud.env", side_effect=mock_env)

    logger = GCloudLogger("test-service")

    extra = {
        "username": "john",
        "password": "secret123",
        "token": "xyz789",
        "api_key": "abc456",
        "email": "john@example.com",
    }

    sanitized = logger._sanitize_extra_data(extra)

    assert sanitized["username"] == "john"
    assert sanitized["password"] == "[REDACTED]"
    assert sanitized["token"] == "[REDACTED]"
    assert sanitized["api_key"] == "[REDACTED]"
    assert sanitized["email"] == "john@example.com"


@pytest.mark.skipif(
    not GCP_LOGGING_AVAILABLE, reason="google-cloud-logging not installed"
)
def test_gcloud_logger_sanitize_empty_extra(mocker):
    """Test _sanitize_extra_data handles empty/None extra."""
    mocker.patch("app.services.logging.gcloud.gcp_logging.Client")
    mocker.patch("app.services.logging.gcloud.CloudLoggingHandler")

    def mock_env(key, default=None):
        return {
            "LOG_SAMPLE_RATE": "1.0",
            "APP_ENVIRONMENT": "test",
            "APP_VERSION": "1.0",
        }.get(key, default)

    mocker.patch("app.services.logging.gcloud.env", side_effect=mock_env)

    logger = GCloudLogger("test-service")

    assert logger._sanitize_extra_data(None) == {}
    assert logger._sanitize_extra_data({}) == {}


@pytest.mark.skipif(
    not GCP_LOGGING_AVAILABLE, reason="google-cloud-logging not installed"
)
def test_gcloud_logger_should_sample_log(mocker):
    """Test _should_sample_log respects sample rate."""
    mocker.patch("app.services.logging.gcloud.gcp_logging.Client")
    mocker.patch("app.services.logging.gcloud.CloudLoggingHandler")

    def mock_env(key, default=None):
        return {
            "LOG_SAMPLE_RATE": "1.0",
            "APP_ENVIRONMENT": "test",
            "APP_VERSION": "1.0",
        }.get(key, default)

    mocker.patch("app.services.logging.gcloud.env", side_effect=mock_env)

    # Test with 100% sampling
    logger = GCloudLogger("test-service", sample_rate=1.0)
    assert logger._should_sample_log() is True

    # Test with 0% sampling (need to set LOG_SAMPLE_RATE=0
    # via env since sample_rate=0.0 is falsy)
    def mock_env_zero(key, default=None):
        return {
            "LOG_SAMPLE_RATE": "0.0",
            "APP_ENVIRONMENT": "test",
            "APP_VERSION": "1.0",
        }.get(key, default)

    mocker.patch("app.services.logging.gcloud.env", side_effect=mock_env_zero)
    logger = GCloudLogger("test-service")
    assert logger._should_sample_log() is False

    # Test with 50% sampling (mock random to control)
    def mock_env_half(key, default=None):
        return {
            "LOG_SAMPLE_RATE": "0.5",
            "APP_ENVIRONMENT": "test",
            "APP_VERSION": "1.0",
        }.get(key, default)

    mocker.patch("app.services.logging.gcloud.env", side_effect=mock_env_half)
    logger = GCloudLogger("test-service")

    mocker.patch("app.services.logging.gcloud.random.random", return_value=0.3)
    assert logger._should_sample_log() is True

    mocker.patch("app.services.logging.gcloud.random.random", return_value=0.7)
    assert logger._should_sample_log() is False


@pytest.mark.skipif(
    not GCP_LOGGING_AVAILABLE, reason="google-cloud-logging not installed"
)
def test_gcloud_logger_get_caller_location(mocker):
    """Test _get_caller_location returns proper location."""
    mocker.patch("app.services.logging.gcloud.gcp_logging.Client")
    mocker.patch("app.services.logging.gcloud.CloudLoggingHandler")

    def mock_env(key, default=None):
        return {
            "LOG_SAMPLE_RATE": "1.0",
            "APP_ENVIRONMENT": "test",
            "APP_VERSION": "1.0",
        }.get(key, default)

    mocker.patch("app.services.logging.gcloud.env", side_effect=mock_env)

    logger = GCloudLogger("test-service")
    location = logger._get_caller_location()

    # Should return format like "file.py:123"
    assert ":" in location
    parts = location.split(":")
    assert len(parts) == 2
    assert parts[1].isdigit()


@pytest.mark.skipif(
    not GCP_LOGGING_AVAILABLE, reason="google-cloud-logging not installed"
)
def test_gcloud_logger_get_caller_location_outside_project(mocker):
    """Test _get_caller_location handles frames outside project root."""
    mocker.patch("app.services.logging.gcloud.gcp_logging.Client")
    mocker.patch("app.services.logging.gcloud.CloudLoggingHandler")

    def mock_env(key, default=None):
        return {
            "LOG_SAMPLE_RATE": "1.0",
            "APP_ENVIRONMENT": "test",
            "APP_VERSION": "1.0",
        }.get(key, default)

    mocker.patch("app.services.logging.gcloud.env", side_effect=mock_env)

    logger = GCloudLogger(
        "test-service"
    )  # Mock inspect.stack to return frame outside project
    fake_frame = MagicMock()
    fake_frame.filename = "/external/library/module.py"
    fake_frame.lineno = 42

    mocker.patch("app.services.logging.gcloud.inspect.stack", return_value=[fake_frame])

    location = logger._get_caller_location()

    # Should return "unknown:0" when no valid frame found
    assert location == "unknown:0"


@pytest.mark.skipif(
    not GCP_LOGGING_AVAILABLE, reason="google-cloud-logging not installed"
)
def test_gcloud_logger_get_caller_location_relpath_error(mocker):
    """Test _get_caller_location handles relpath errors gracefully."""
    mocker.patch("app.services.logging.gcloud.gcp_logging.Client")
    mocker.patch("app.services.logging.gcloud.CloudLoggingHandler")

    def mock_env(key, default=None):
        return {
            "LOG_SAMPLE_RATE": "1.0",
            "APP_ENVIRONMENT": "test",
            "APP_VERSION": "1.0",
        }.get(key, default)

    mocker.patch("app.services.logging.gcloud.env", side_effect=mock_env)

    logger = GCloudLogger(
        "test-service"
    )  # Mock inspect.stack to return frame inside project
    project_root = logger.project_root
    fake_frame = MagicMock()
    fake_frame.filename = os.path.join(project_root, "app", "test.py")
    fake_frame.lineno = 99

    mocker.patch("app.services.logging.gcloud.inspect.stack", return_value=[fake_frame])

    # Mock os.path.relpath to raise ValueError
    original_relpath = os.path.relpath

    def mock_relpath(path, start):
        if path == fake_frame.filename:
            raise ValueError("Cannot calculate relative path")
        return original_relpath(path, start)

    mocker.patch("os.path.relpath", side_effect=mock_relpath)

    location = logger._get_caller_location()

    # Should return basename:lineno when relpath fails
    assert location == "test.py:99"


@pytest.mark.skipif(
    not GCP_LOGGING_AVAILABLE, reason="google-cloud-logging not installed"
)
def test_gcloud_logger_create_structured_log(mocker):
    """Test _create_structured_log creates proper structure."""
    mocker.patch("app.services.logging.gcloud.gcp_logging.Client")
    mocker.patch("app.services.logging.gcloud.CloudLoggingHandler")

    # Mock env to return fixed values
    def mock_env(key, default=None):
        return {
            "APP_ENVIRONMENT": "test",
            "APP_VERSION": "1.0.0",
            "LOG_SAMPLE_RATE": "1.0",
        }.get(key, default)

    mocker.patch("app.services.logging.gcloud.env", side_effect=mock_env)

    logger = GCloudLogger("test-service")

    structured = logger._create_structured_log(
        "INFO", "Test message", extra={"user_id": 123}
    )

    assert structured["severity"] == "INFO"
    assert structured["service"] == "test-service"
    assert structured["message"] == "Test message"
    assert structured["environment"] == "test"
    assert structured["version"] == "1.0.0"
    assert structured["user_id"] == 123
    assert "timestamp" in structured
    assert "location" in structured


@pytest.mark.skipif(
    not GCP_LOGGING_AVAILABLE, reason="google-cloud-logging not installed"
)
def test_gcloud_logger_info(mocker):
    """Test info logging method."""
    mock_client = MagicMock()
    mock_handler = MagicMock()
    mock_logger = MagicMock()

    mocker.patch(
        "app.services.logging.gcloud.gcp_logging.Client", return_value=mock_client
    )
    mocker.patch(
        "app.services.logging.gcloud.CloudLoggingHandler", return_value=mock_handler
    )
    mocker.patch(
        "app.services.logging.gcloud.logging.getLogger", return_value=mock_logger
    )

    def mock_env(key, default=None):
        return {
            "LOG_SAMPLE_RATE": "1.0",
            "APP_ENVIRONMENT": "test",
            "APP_VERSION": "1.0",
        }.get(key, default)

    mocker.patch("app.services.logging.gcloud.env", side_effect=mock_env)

    logger = GCloudLogger("test-service", sample_rate=1.0)
    logger.info("Info message", extra={"request_id": "abc"})

    # Verify logger.info was called
    assert mock_logger.info.called


@pytest.mark.skipif(
    not GCP_LOGGING_AVAILABLE, reason="google-cloud-logging not installed"
)
def test_gcloud_logger_warning(mocker):
    """Test warning logging method."""
    mock_client = MagicMock()
    mock_handler = MagicMock()
    mock_logger = MagicMock()

    mocker.patch(
        "app.services.logging.gcloud.gcp_logging.Client", return_value=mock_client
    )
    mocker.patch(
        "app.services.logging.gcloud.CloudLoggingHandler", return_value=mock_handler
    )
    mocker.patch(
        "app.services.logging.gcloud.logging.getLogger", return_value=mock_logger
    )

    def mock_env(key, default=None):
        return {
            "LOG_SAMPLE_RATE": "1.0",
            "APP_ENVIRONMENT": "test",
            "APP_VERSION": "1.0",
        }.get(key, default)

    mocker.patch("app.services.logging.gcloud.env", side_effect=mock_env)

    logger = GCloudLogger("test-service", sample_rate=1.0)
    logger.warning("Warning message")

    assert mock_logger.warning.called


@pytest.mark.skipif(
    not GCP_LOGGING_AVAILABLE, reason="google-cloud-logging not installed"
)
def test_gcloud_logger_error(mocker):
    """Test error logging method."""
    mock_client = MagicMock()
    mock_handler = MagicMock()
    mock_logger = MagicMock()

    mocker.patch(
        "app.services.logging.gcloud.gcp_logging.Client", return_value=mock_client
    )
    mocker.patch(
        "app.services.logging.gcloud.CloudLoggingHandler", return_value=mock_handler
    )
    mocker.patch(
        "app.services.logging.gcloud.logging.getLogger", return_value=mock_logger
    )

    def mock_env(key, default=None):
        return {
            "LOG_SAMPLE_RATE": "1.0",
            "APP_ENVIRONMENT": "test",
            "APP_VERSION": "1.0",
        }.get(key, default)

    mocker.patch("app.services.logging.gcloud.env", side_effect=mock_env)

    logger = GCloudLogger("test-service", sample_rate=1.0)
    logger.error("Error message")

    assert mock_logger.error.called


@pytest.mark.skipif(
    not GCP_LOGGING_AVAILABLE, reason="google-cloud-logging not installed"
)
def test_gcloud_logger_debug(mocker):
    """Test debug logging method."""
    mock_client = MagicMock()
    mock_handler = MagicMock()
    mock_logger = MagicMock()

    mocker.patch(
        "app.services.logging.gcloud.gcp_logging.Client", return_value=mock_client
    )
    mocker.patch(
        "app.services.logging.gcloud.CloudLoggingHandler", return_value=mock_handler
    )
    mocker.patch(
        "app.services.logging.gcloud.logging.getLogger", return_value=mock_logger
    )

    def mock_env(key, default=None):
        return {
            "LOG_SAMPLE_RATE": "1.0",
            "APP_ENVIRONMENT": "test",
            "APP_VERSION": "1.0",
        }.get(key, default)

    mocker.patch("app.services.logging.gcloud.env", side_effect=mock_env)

    logger = GCloudLogger("test-service", sample_rate=1.0)
    logger.debug("Debug message")

    assert mock_logger.debug.called


@pytest.mark.skipif(
    not GCP_LOGGING_AVAILABLE, reason="google-cloud-logging not installed"
)
def test_gcloud_logger_exception(mocker):
    """Test exception logging method."""
    mock_client = MagicMock()
    mock_handler = MagicMock()
    mock_logger = MagicMock()

    mocker.patch(
        "app.services.logging.gcloud.gcp_logging.Client", return_value=mock_client
    )
    mocker.patch(
        "app.services.logging.gcloud.CloudLoggingHandler", return_value=mock_handler
    )
    mocker.patch(
        "app.services.logging.gcloud.logging.getLogger", return_value=mock_logger
    )

    def mock_env(key, default=None):
        return {
            "LOG_SAMPLE_RATE": "1.0",
            "APP_ENVIRONMENT": "test",
            "APP_VERSION": "1.0",
        }.get(key, default)

    mocker.patch("app.services.logging.gcloud.env", side_effect=mock_env)

    logger = GCloudLogger("test-service", sample_rate=1.0)
    logger.exception("Exception message")

    assert mock_logger.exception.called


@pytest.mark.skipif(
    not GCP_LOGGING_AVAILABLE, reason="google-cloud-logging not installed"
)
def test_gcloud_logger_critical(mocker):
    """Test critical logging method."""
    mock_client = MagicMock()
    mock_handler = MagicMock()
    mock_logger = MagicMock()

    mocker.patch(
        "app.services.logging.gcloud.gcp_logging.Client", return_value=mock_client
    )
    mocker.patch(
        "app.services.logging.gcloud.CloudLoggingHandler", return_value=mock_handler
    )
    mocker.patch(
        "app.services.logging.gcloud.logging.getLogger", return_value=mock_logger
    )

    def mock_env(key, default=None):
        return {
            "LOG_SAMPLE_RATE": "1.0",
            "APP_ENVIRONMENT": "test",
            "APP_VERSION": "1.0",
        }.get(key, default)

    mocker.patch("app.services.logging.gcloud.env", side_effect=mock_env)

    logger = GCloudLogger("test-service", sample_rate=1.0)
    logger.critical("Critical message")

    assert mock_logger.critical.called


@pytest.mark.skipif(
    not GCP_LOGGING_AVAILABLE, reason="google-cloud-logging not installed"
)
def test_gcloud_logger_sampling_skips_logs(mocker):
    """Test that sampling rate of 0 prevents logs from being written."""
    mock_client = MagicMock()
    mock_handler = MagicMock()
    mock_logger = MagicMock()

    mocker.patch(
        "app.services.logging.gcloud.gcp_logging.Client", return_value=mock_client
    )
    mocker.patch(
        "app.services.logging.gcloud.CloudLoggingHandler", return_value=mock_handler
    )
    mocker.patch(
        "app.services.logging.gcloud.logging.getLogger", return_value=mock_logger
    )

    def mock_env(key, default=None):
        return {
            "LOG_SAMPLE_RATE": "1.0",
            "APP_ENVIRONMENT": "test",
            "APP_VERSION": "1.0",
        }.get(key, default)

    # Use LOG_SAMPLE_RATE=0.0 via env since sample_rate=0.0 is falsy
    def mock_env_zero(key, default=None):
        return {
            "LOG_SAMPLE_RATE": "0.0",
            "APP_ENVIRONMENT": "test",
            "APP_VERSION": "1.0",
        }.get(key, default)

    mocker.patch("app.services.logging.gcloud.env", side_effect=mock_env_zero)

    logger = GCloudLogger("test-service")

    # None of these should actually log
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.debug("Debug message")
    logger.exception("Exception message")

    # Verify no logging methods were called
    assert not mock_logger.info.called
    assert not mock_logger.warning.called
    assert not mock_logger.error.called
    assert not mock_logger.debug.called
    assert not mock_logger.exception.called
