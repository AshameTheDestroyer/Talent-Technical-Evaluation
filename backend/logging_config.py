import logging
import logging.config
from config import settings
import os

def setup_logging():
    """Setup logging configuration"""
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(settings.log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format=settings.log_format,
        handlers=[
            logging.FileHandler(settings.log_file),
            logging.StreamHandler()  # Also log to console
        ]
    )
    
    # Create a logger for the application
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized with level: {settings.log_level}")
    
    return logger

# Initialize the logger
logger = setup_logging()

def get_logger(name: str = None):
    """Get a logger instance with the specified name"""
    if name:
        return logging.getLogger(name)
    else:
        return logger