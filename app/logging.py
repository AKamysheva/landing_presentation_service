import logging

CONFIG = {
    "version": 1.0,
    "formatters": {
        "file_formatter": {
            "format": "{levelname}: {message} : {asctime}",
            "style": "{",
            "datefmt": "%d.%m.%Y %H:%M:%S",
        }
    },
    "handlers": {
        "file_handler": {
            "class": "logging.FileHandler",
            "formatter": "file_formatter",
            "filename": "logs.log",
            "encoding": "utf-8",
            "mode": "a",
        },
    },
    "loggers": {
        __name__: {
            "level": "INFO",
            "handlers": ["file_handler"],
        }
    },
}

logging.config.dictConfig(CONFIG)
logger = logging.getLogger(__name__)
