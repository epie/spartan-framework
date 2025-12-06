"""
Unit tests for app/services/tracing/gcloud.py GCloudTracer.
Tests initialization, decorators, and context managers.
"""

import pytest

from app.services.tracing.gcloud import GCP_TRACING_AVAILABLE, GCloudTracer


def test_gcloud_tracer_import_error_when_unavailable(mocker):
    """Test GCloudTracer raises ImportError when google-cloud-trace not available."""
    # Temporarily patch GCP_TRACING_AVAILABLE to False
    mocker.patch("app.services.tracing.gcloud.GCP_TRACING_AVAILABLE", False)

    with pytest.raises(ImportError) as exc_info:
        GCloudTracer("test-service")

    assert "Google Cloud Tracing dependencies not available" in str(exc_info.value)


@pytest.mark.skipif(
    not GCP_TRACING_AVAILABLE, reason="google-cloud-trace not installed"
)
def test_gcloud_tracer_initialization(mocker):
    """Test GCloudTracer initializes with service name and client."""
    mock_client = mocker.Mock()
    mocker.patch(
        "app.services.tracing.gcloud.trace_v1.TraceServiceClient",
        return_value=mock_client,
    )

    tracer = GCloudTracer("my-service")

    assert tracer.service_name == "my-service"
    assert tracer.client is mock_client


@pytest.mark.skipif(
    not GCP_TRACING_AVAILABLE, reason="google-cloud-trace not installed"
)
def test_gcloud_tracer_capture_lambda_handler(mocker):
    """Test capture_lambda_handler decorator wraps function."""
    mock_client = mocker.Mock()
    mock_client.patch_traces = mocker.Mock()
    mocker.patch(
        "app.services.tracing.gcloud.trace_v1.TraceServiceClient",
        return_value=mock_client,
    )

    tracer = GCloudTracer("test-service")

    @tracer.capture_lambda_handler
    def handler(event, context):
        return {"statusCode": 200, "body": "ok"}

    result = handler({"key": "value"}, {"request_id": "123"})

    assert result == {"statusCode": 200, "body": "ok"}


@pytest.mark.skipif(
    not GCP_TRACING_AVAILABLE, reason="google-cloud-trace not installed"
)
def test_gcloud_tracer_capture_lambda_handler_without_patch_traces(mocker):
    """Test capture_lambda_handler when client doesn't have patch_traces."""
    mock_client = mocker.Mock(spec=[])  # No patch_traces attribute
    mocker.patch(
        "app.services.tracing.gcloud.trace_v1.TraceServiceClient",
        return_value=mock_client,
    )

    tracer = GCloudTracer("test-service")

    @tracer.capture_lambda_handler
    def handler(event, context):
        return {"statusCode": 200, "body": "no patch"}

    result = handler({"test": "data"}, {"req": "456"})

    assert result == {"statusCode": 200, "body": "no patch"}


@pytest.mark.skipif(
    not GCP_TRACING_AVAILABLE, reason="google-cloud-trace not installed"
)
def test_gcloud_tracer_capture_lambda_handler_exception(mocker):
    """Test capture_lambda_handler catches exceptions in tracing code."""
    mock_client = mocker.Mock()
    mock_client.patch_traces = mocker.Mock(side_effect=Exception("Trace error"))
    mocker.patch(
        "app.services.tracing.gcloud.trace_v1.TraceServiceClient",
        return_value=mock_client,
    )

    tracer = GCloudTracer("test-service")

    @tracer.capture_lambda_handler
    def handler(event, context):
        return {"statusCode": 200, "body": "still works"}

    # Should not raise, exception is caught
    result = handler({"key": "value"}, {"request_id": "789"})

    assert result == {"statusCode": 200, "body": "still works"}


@pytest.mark.skipif(
    not GCP_TRACING_AVAILABLE, reason="google-cloud-trace not installed"
)
def test_gcloud_tracer_capture_method(mocker):
    """Test capture_method decorator wraps instance methods."""
    mock_client = mocker.Mock()
    mock_client.patch_traces = mocker.Mock()
    mocker.patch(
        "app.services.tracing.gcloud.trace_v1.TraceServiceClient",
        return_value=mock_client,
    )

    tracer = GCloudTracer("test-service")

    class MyClass:
        @tracer.capture_method
        def my_method(self, arg1, arg2=None):
            return f"arg1={arg1}, arg2={arg2}"

    instance = MyClass()
    result = instance.my_method("value1", arg2="value2")

    assert result == "arg1=value1, arg2=value2"


@pytest.mark.skipif(
    not GCP_TRACING_AVAILABLE, reason="google-cloud-trace not installed"
)
def test_gcloud_tracer_capture_method_without_patch_traces(mocker):
    """Test capture_method when client doesn't have patch_traces."""
    mock_client = mocker.Mock(spec=[])  # No patch_traces attribute
    mocker.patch(
        "app.services.tracing.gcloud.trace_v1.TraceServiceClient",
        return_value=mock_client,
    )

    tracer = GCloudTracer("test-service")

    class MyClass:
        @tracer.capture_method
        def compute(self, x):
            return x * 2

    instance = MyClass()
    result = instance.compute(10)

    assert result == 20


@pytest.mark.skipif(
    not GCP_TRACING_AVAILABLE, reason="google-cloud-trace not installed"
)
def test_gcloud_tracer_capture_method_exception(mocker):
    """Test capture_method catches exceptions in tracing code."""
    mock_client = mocker.Mock()
    mock_client.patch_traces = mocker.Mock(side_effect=RuntimeError("Tracing failed"))
    mocker.patch(
        "app.services.tracing.gcloud.trace_v1.TraceServiceClient",
        return_value=mock_client,
    )

    tracer = GCloudTracer("test-service")

    class MyClass:
        @tracer.capture_method
        def process(self, data):
            return f"processed: {data}"

    instance = MyClass()
    result = instance.process("test")

    assert result == "processed: test"


@pytest.mark.skipif(
    not GCP_TRACING_AVAILABLE, reason="google-cloud-trace not installed"
)
def test_gcloud_tracer_create_segment(mocker):
    """Test create_segment context manager."""
    mock_client = mocker.Mock()
    mocker.patch(
        "app.services.tracing.gcloud.trace_v1.TraceServiceClient",
        return_value=mock_client,
    )

    tracer = GCloudTracer("test-service")

    executed = False
    with tracer.create_segment("test-segment", metadata={"key": "value"}):
        executed = True

    assert executed


@pytest.mark.skipif(
    not GCP_TRACING_AVAILABLE, reason="google-cloud-trace not installed"
)
def test_gcloud_tracer_create_segment_exception_handling(mocker):
    """Test create_segment handles exceptions in user code."""
    mock_client = mocker.Mock()
    mocker.patch(
        "app.services.tracing.gcloud.trace_v1.TraceServiceClient",
        return_value=mock_client,
    )

    tracer = GCloudTracer("test-service")

    with pytest.raises(ValueError) as exc_info:
        with tracer.create_segment("error-segment"):
            raise ValueError("User code error")

    assert str(exc_info.value) == "User code error"


@pytest.mark.skipif(
    not GCP_TRACING_AVAILABLE, reason="google-cloud-trace not installed"
)
def test_gcloud_tracer_create_subsegment(mocker):
    """Test create_subsegment context manager."""
    mock_client = mocker.Mock()
    mocker.patch(
        "app.services.tracing.gcloud.trace_v1.TraceServiceClient",
        return_value=mock_client,
    )

    tracer = GCloudTracer("test-service")

    executed = False
    with tracer.create_subsegment("sub-segment"):
        executed = True

    assert executed


@pytest.mark.skipif(
    not GCP_TRACING_AVAILABLE, reason="google-cloud-trace not installed"
)
def test_gcloud_tracer_create_subsegment_exception_handling(mocker):
    """Test create_subsegment handles exceptions in user code."""
    mock_client = mocker.Mock()
    mocker.patch(
        "app.services.tracing.gcloud.trace_v1.TraceServiceClient",
        return_value=mock_client,
    )

    tracer = GCloudTracer("test-service")

    with pytest.raises(RuntimeError) as exc_info:
        with tracer.create_subsegment("error-subsegment"):
            raise RuntimeError("Subsegment error")

    assert str(exc_info.value) == "Subsegment error"
