import logging
from logging.handlers import RotatingFileHandler
import sys
import os

from pprint import pformat
from typing import Any
from pygments import highlight
from pygments.formatters import Terminal256Formatter, TerminalFormatter
from pygments.lexers import PythonLexer


def load_logger(**kwargs):
    level = kwargs.get("level", logging.INFO)
    format = kwargs.get(
        "format",
        "%(levelname)8s |%(asctime)s\t|%(pathname)s: line %(lineno)d\t|%(funcName)20s |%(message)s",
    )
    directory = kwargs.get("directory", None)
    handlers = kwargs.get("handlers", "stdout")
    maxBytes = kwargs.get("maxBytes", 1073741824)
    backupCount = kwargs.get("backupCount", 1)

    if level == "DEBUG":
        level = logging.DEBUG
    elif level == "INFO":
        level = logging.INFO
    elif level == "WARNING":
        level = logging.WARNING
    elif level == "ERROR":
        level = logging.ERROR
    elif level == "CRITICAL":
        level = logging.CRITICAL
    else:
        raise ValueError("Invalid logging level: {}".format(level))

    handlers_ = []
    if not isinstance(handlers, list):
        handlers = [handlers]
    for handler in handlers:
        if handler == "stdout":
            handlers_.append(logging.StreamHandler(sys.stdout))
        elif handler == "stderr":
            handlers_.append(logging.StreamHandler(sys.stderr))
        elif isinstance(handler, str):
            assert (
                directory is not None
            ), "Logging directory must be specified when using file handler."
            assert os.path.isdir(directory), "Logging directory must be a directory."
            log_fpath = os.path.join(directory, handler)
            handlers_.append(
                RotatingFileHandler(
                    log_fpath, maxBytes=maxBytes, backupCount=backupCount
                )
            )
        else:
            raise ValueError("Invalid logging handler: {}".format(handler))
    handlers = handlers_

    logging.basicConfig(level=level, format=format, handlers=handlers)

    return logging.getLogger(__name__)


def pprint_color(obj: Any) -> None:
    """Pretty-print in color."""
    print(highlight(pformat(obj), PythonLexer(), TerminalFormatter()), end="")
