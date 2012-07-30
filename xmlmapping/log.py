# Internal
from .settings import (
    LOGGER_NAME, LOG_FILE, LOG_SIZE, LOGGER_FORMAT, LOG_LEVEL
)
from .utils.loggers import DefaultLogger

default_logger = DefaultLogger(
    logger_name=LOGGER_NAME,
    level=LOG_LEVEL,
    log_file=LOG_FILE,
    log_size=LOG_SIZE,
    logger_format=LOGGER_FORMAT
)
