"""Basic tests for {{PROJECT_NAME}}."""

import pytest

from {{PROJECT_NAME}} import __version__


def test_version() -> None:
    """Test that version is defined."""
    assert __version__ == "0.1.0"


class TestExample:
    """Example test class."""

    def test_placeholder(self) -> None:
        """Placeholder test."""
        assert True

    @pytest.mark.slow
    def test_slow_operation(self) -> None:
        """Example of a slow test."""
        import time
        time.sleep(0.1)
        assert True
