import os
import time
log_file = "{}.log".format(time.strftime("%Y%m%d"))
LOGPATH = os.path.join(os.path.dirname(__file__), 'logs', log_file)

LOGGING_CONF= {
    "version": 1,
    "loggers": {
        "": {
            "level": "DEBUG",
            "handlers": ["stream_handler", "file_handler"],
        }
    },
    "handlers": {
        "stream_handler": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "level": "INFO",
            "formatter": "default_formatter"
        },
        "file_handler": {
            "class": "logging.FileHandler",
            "filename": LOGPATH,
            "mode": "a",
            "level": "ERROR",
            "formatter": "default_formatter"
        }
    },
    "formatters": {
        "default_formatter": {
            "format": "%(asctime)s | %(levelname)s | %(name)s | %(lineno)s:: %(message)s"
        }
    }
}