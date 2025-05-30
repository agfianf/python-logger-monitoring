import logging
import os
import re
from collections import OrderedDict
from logging.handlers import RotatingFileHandler
from typing import Literal

import structlog
from structlog.processors import EventRenamer

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def mask_sensitive_processor(logger, method_name, event_dict):
    """Mask sensitive data in logs"""
    sensitive_fields = [
        "password",
        "token",
        "api_key",
        "secret",
        "authorization",
        "email",
        "phone",
        "ssn",
        "credit_card",
    ]

    for key, value in event_dict.items():
        if isinstance(value, str) and key.lower() in sensitive_fields:
            event_dict[key] = "***MASKED***"

    return event_dict


def normalize_high_cardinality_processor(logger, method_name, event_dict):
    """Normalize high cardinality fields like paths with UUIDs"""
    # UUID4 pattern (8-4-4-4-12 hex characters)
    uuid_pattern = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"

    # Common high cardinality patterns to normalize
    patterns = {
        "path": [
            (uuid_pattern, "{uid}"),
            (r"\d{10,}", "{id}"),  # Long numeric IDs
            (r"/\d+/", "/{id}/"),  # Numeric path segments
            (r"/\d+$", "/{id}"),  # Numeric IDs at end of path
        ]
    }

    for field_name, field_patterns in patterns.items():
        if field_name in event_dict and isinstance(event_dict[field_name], str):
            value = event_dict[field_name]
            for pattern, replacement in field_patterns:
                value = re.sub(pattern, replacement, value, flags=re.IGNORECASE)
            event_dict[field_name] = value

    return event_dict


def _reorder_keys(_, __, event_dict):
    """Reorder keys for consistent log format"""
    key_order = [
        # Basic info
        "xtime",
        "level",
        "msg",
        # Common context
        "request_id",
        "user_id",
        # HTTP info
        "method",
        "path",
        "status_code",
        "response_time_ms",
        # Additional context
        "func_name",
        "pathname",
        "lineno",  # Debug info
    ]

    ordered_dict = OrderedDict()
    # Add keys in preferred order
    for key in key_order:
        if key in event_dict:
            ordered_dict[key] = event_dict.pop(key)

    # Add remaining keys
    ordered_dict.update(event_dict)
    return ordered_dict


def setup_logging(
    log_level: LogLevel = "INFO",
    is_async: bool = False,
    enable_file_logs: bool = False,
    log_file: str = "logs/app.log",
):
    # Core processors - simple and essential
    processors = [
        EventRenamer(to="msg", replace_by="event"),  # event -> msg
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,  # Add level field
        structlog.processors.TimeStamper(fmt="iso", utc=False, key="xtime"),
        mask_sensitive_processor,  # Mask sensitive data
        normalize_high_cardinality_processor,  # Normalize high cardinality fields
        _reorder_keys,  # Consistent key ordering
        structlog.processors.JSONRenderer(),  # JSON output
    ]

    # Choose wrapper class based on async requirement
    wrapper_class = (
        structlog.stdlib.AsyncBoundLogger if is_async else structlog.stdlib.BoundLogger
    )

    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=wrapper_class,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Setup stdlib logging handlers
    handlers = []

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(message)s"))
    handlers.append(console_handler)

    # File handler (optional)
    if enable_file_logs:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
        )
        file_handler.setFormatter(logging.Formatter("%(message)s"))
        handlers.append(file_handler)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.handlers = []
    for handler in handlers:
        root_logger.addHandler(handler)
    root_logger.setLevel(getattr(logging, log_level.upper()))

    # Quiet noisy third-party loggers
    noisy_loggers = [
        "httpx",
        "urllib3",
        "uvicorn.access",
        "multipart",
        "sqlalchemy",
        "alembic",
        "botocore",
        "boto3",
    ]
    for logger_name in noisy_loggers:
        logging.getLogger(logger_name).setLevel(logging.WARNING)


# Example usage
if __name__ == "__main__":
    import uuid

    # Development setup
    setup_logging(log_level="DEBUG", is_async=False)

    # Production setup with file logs
    # setup_logging(log_level="INFO", is_async=True, enable_file_logs=True)

    # Test
    logger = structlog.get_logger()
    logger.info("Test message", user_id=123, password="secret123")
    logger.error("Error occurred", request_id="abc-123", api_key="secret")
    logger.info("User activity", method="GET", path=f"/api/v1/users/{uuid.uuid4()}")
    logger.info("User activity", method="GET", path="/api/v1/users/2432")
