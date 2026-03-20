import logging
import sys
from pythonjsonlogger import jsonlogger
from core.config import settings


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter with additional fields"""
    
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['app_name'] = settings.APP_NAME
        log_record['version'] = settings.APP_VERSION
        log_record['level'] = record.levelname
        log_record['logger'] = record.name


def setup_logging():
    """Setup structured JSON logging"""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO if not settings.DEBUG else logging.DEBUG)
    
    # Console handler with JSON formatter
    handler = logging.StreamHandler(sys.stdout)
    formatter = CustomJsonFormatter(
        '%(timestamp)s %(level)s %(name)s %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Remove default handlers
    logger.handlers.clear()
    logger.addHandler(handler)
    
    return logger


# Create logger instance
logger = setup_logging()
