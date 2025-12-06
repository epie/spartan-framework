from unittest.mock import MagicMock, patch


def test_main_function_logs_event():
    """Test that main function logs the cloud event with extra data."""
    # Create a mock cloud event
    mock_event = MagicMock()
    mock_event.__getitem__.side_effect = lambda key: {
        "id": "test-event-123",
    }[key]
    mock_event.data = {"message": "test message"}

    with patch("main.logger") as mock_logger:
        # Import here to avoid execution at module level
        from main import main

        main(mock_event)
        mock_logger.info.assert_called_once()
        # Verify the call includes message and extra data
        call_args, call_kwargs = mock_logger.info.call_args
        assert call_args[0] == "Testing"
        assert "extra" in call_kwargs
        assert call_kwargs["extra"]["testing"] == "test"
        assert call_kwargs["extra"]["another"] == 1234
