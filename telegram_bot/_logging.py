import logging
import sys
from typing import Any, Union

from loguru import logger


class InterceptHandler(logging.Handler):
    """
    Default handler from examples in loguru documentation.

    This handler intercepts all log requests and
    passes them to loguru.

    For more info see:
    https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        """
        Propagates logs to loguru.

        :param record: record to log.
        """
        try:
            level: Union[str, int] = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


def record_formatter(record: dict[str, Any]) -> str:  # pragma: no cover
    """
    Formats the record.

    This function formats message
    by adding extra trace information to the record.

    :param record: record information.
    :return: format string.
    """
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> "
        "| <level>{level: <8}</level> "
        "| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> "
        "- <level>{message}</level>\n"
    )

    if record["exception"]:
        log_format = f"{log_format}{{exception}}"

    return log_format


def configure_logging(level: str = "INFO") -> None:  # pragma: no cover
    intercept_handler = InterceptHandler()
    logging.basicConfig(handlers=[intercept_handler], level=level)
    logger.remove()
    logger.add(
        sys.stdout,
        level=level,
        format=record_formatter,
    )
