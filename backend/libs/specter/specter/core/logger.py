import logging
import os
from typing import Optional

from core.config import settings


def setup_logging(
    log_level: int = logging.INFO, script_name: Optional[str] = None
) -> logging.Logger:
    """
    Sets up logging for the application.

    Args:
        log_level (int): The logging level. Defaults to logging.INFO.
                        [can be logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
        script_name (str): The name of the script. Defaults to None, in which case it will use the name of the calling script.

    Returns:
        logging.Logger: Configured logger instance.
    """
    if script_name is None:
        # Get the calling script's name if not provided
        script_name = os.path.basename(__file__)

    _logger = logging.getLogger(script_name)
    _logger.setLevel(log_level)

    # Create console handler and set level to debug
    if not _logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(log_level)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        ch.setFormatter(formatter)
        _logger.addHandler(ch)

    return _logger


def configure_logger() -> logging.Logger:
    """
    Configures and returns a cached logger instance.

    Returns:
        logging.Logger: A configured logger instance, reused across the application.
    """
    instance: logging.Logger = setup_logging(script_name=settings.SERVICE_NAME)
    if settings.DEBUG:
        logging.basicConfig(level=logging.DEBUG)
    return instance


logger: logging.Logger = configure_logger()
