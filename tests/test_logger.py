import logging
import pytest

from mock import PropertyMock

from lazysusan.logger import (
    _configure,
    get_level,
    get_logger,
)


def test_get_level_default():
    assert get_level() == logging.WARN


def test_get_level_debug(mocker):
    mocker.patch.dict("os.environ", {"LAZYSUSAN_LOG_LEVEL": "logging.DEBUG"})
    assert get_level() == logging.DEBUG


@pytest.fixture(params=("INVALID", "log.INFO", "logger.INFO", "loggingINFO"))
def invalid_level(request):
    yield request.param


def test_get_level_invalid(mocker, invalid_level):
    mocker.patch.dict("os.environ", {"LAZYSUSAN_LOG_LEVEL": invalid_level})
    assert get_level() == logging.WARN


def test_configure(mocker):
    mock_config = mocker.patch("lazysusan.logger.logging.basicConfig")
    mock_configured = mocker.patch("lazysusan.logger._is_configured")
    mock_configured.return_value = False
    _configure(logging.INFO)
    assert mock_config.call_count == 1


def test_configure_once(mocker):
    mock_config = mocker.patch("lazysusan.logger.logging.basicConfig")

    mock_configured = mocker.patch("lazysusan.logger._is_configured")
    mock_configured.return_value = False
    _configure(logging.INFO)

    mock_configured.return_value = True
    _configure(logging.INFO)
    _configure(logging.INFO)
    assert mock_config.call_count == 1
