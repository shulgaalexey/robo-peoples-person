"""Tests for the main module."""
from unittest.mock import MagicMock, patch

import pytest


def test_main_entry_point():
    """Test main entry point execution."""
    # Mock the CLI and settings to avoid actual execution
    with patch('src.main.cli') as mock_cli, \
         patch('src.main.Settings') as mock_settings, \
         patch('src.main.setup_logging') as mock_setup_logging:

        # Mock settings instance
        mock_settings_instance = MagicMock()
        mock_settings.return_value = mock_settings_instance

        # Import and execute main
        from src.main import main

        # Test that main function exists and can be called
        assert main is not None

        # Test that main calls the CLI
        main()

        # Verify calls
        mock_settings.assert_called_once()
        mock_setup_logging.assert_called_once_with(mock_settings_instance)
        mock_cli.assert_called_once()


def test_main_module_import():
    """Test that main module can be imported without errors."""
    import src.main
    assert hasattr(src.main, 'main')
    assert hasattr(src.main, 'setup_logging')


@patch('src.main.cli')
@patch('src.main.Settings')
@patch('src.main.setup_logging')
def test_main_if_name_main(mock_setup_logging, mock_settings, mock_cli):
    """Test the if __name__ == '__main__' block."""
    # Mock settings instance
    mock_settings_instance = MagicMock()
    mock_settings.return_value = mock_settings_instance

    from src.main import main

    # Call main directly to simulate __main__ execution
    main()

    # Verify all components were called
    mock_settings.assert_called_once()
    mock_setup_logging.assert_called_once_with(mock_settings_instance)
    mock_cli.assert_called_once()


def test_main_module_attributes():
    """Test that main module has expected attributes."""
    import src.main

    # Check that the module has the expected exports
    expected_attributes = ['main', 'setup_logging', 'cli', 'Settings']
    for attr in expected_attributes:
        assert hasattr(src.main, attr), f"Module should have {attr} attribute"


def test_setup_logging():
    """Test logging setup function."""
    with patch('src.main.logging') as mock_logging:
        from src.config.settings import Settings
        from src.main import setup_logging

        # Create settings with log_level
        settings = Settings()

        # Call setup_logging
        setup_logging(settings)

        # Verify logging.basicConfig was called
        mock_logging.basicConfig.assert_called_once()

        # Check that the call included the expected arguments
        call_args = mock_logging.basicConfig.call_args
        assert 'level' in call_args[1]
        assert 'format' in call_args[1]
        assert 'handlers' in call_args[1]
