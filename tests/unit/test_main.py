from unittest.mock import MagicMock, patch


def test_main_function_logs_event():
    """Test that main function prints the cloud event."""
    # Create a mock cloud event
    mock_event = MagicMock()
    mock_event.__getitem__.side_effect = lambda key: {
        "id": "test-event-123",
    }[key]
    mock_event.data = {"message": "test message"}

    with patch("builtins.print") as mock_print:
        # Import here to avoid execution at module level
        from main import main

        main(mock_event)
        mock_print.assert_called_once()
        call_args = mock_print.call_args[0][0]
        assert "test-event-123" in call_args
        assert "test message" in str(call_args)
