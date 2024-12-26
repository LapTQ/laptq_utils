import logging
from logging.handlers import RotatingFileHandler
import sys
import os

from pprint import pformat
from typing import Any
from pygments import highlight
from pygments.formatters import Terminal256Formatter, TerminalFormatter
from pygments.lexers import PythonLexer


def pformat_color(obj: Any) -> None:
    """Pretty-print in color."""
    return highlight(pformat(obj), PythonLexer(), TerminalFormatter())[:-1]


def get_escape_code_levelname_bright(levelname):
    return {
        "DEBUG": "\033[95m",
        "INFO": "\033[92m",
        "WARNING": "\033[33m",
        "ERROR": "\033[31m",
        "CRITICAL": "\033[38;5;214m",
    }.get(levelname, "\033[94m")


class ColorPrettyFormatter(logging.Formatter):

    def format(self, record):
        levelname = record.levelname
        colored_levelname = "{}{:<8}{}".format(
            get_escape_code_levelname_bright(levelname), levelname, "\033[0m"
        )
        record.levelname = colored_levelname

        return super().format(record)


def load_logger(**kwargs):
    levelname = kwargs["levelname"]
    enable__color = kwargs.get("enable__color", True)
    enable__asctime = kwargs.get("enable__asctime", False)
    format = kwargs.get(
        "format",
        "%(levelname)s | {}{}%(pathname)s: line %(lineno)d \t| %(funcName)-10s{}\t | %(message)s".format(
            get_escape_code_levelname_bright("gray") if enable__color else "",
            "%(asctime)s | " if enable__asctime else "",
            "\033[0m" if enable__color else "",
        ),
    )
    directory = kwargs.get("directory", None)
    handlers = kwargs.get("handlers", "stdout")
    maxBytes = kwargs.get("maxBytes", 1073741824)
    backupCount = kwargs.get("backupCount", 1)

    level = eval("logging.{}".format(levelname))

    formatter = (
        ColorPrettyFormatter(format) if enable__color else logging.Formatter(format)
    )

    handlers_ = []
    if not isinstance(handlers, list):
        handlers = [handlers]
    for name_handler in handlers:
        if name_handler == "stdout":
            handler = logging.StreamHandler(sys.stdout)
        elif name_handler == "stderr":
            handler = logging.StreamHandler(sys.stderr)
        elif isinstance(name_handler, str):
            assert (
                directory is not None
            ), "Logging directory must be specified when using file handler."
            assert os.path.isdir(directory), "Logging directory must be a directory."
            log_fpath = os.path.join(directory, name_handler)
            handler = RotatingFileHandler(
                log_fpath, maxBytes=maxBytes, backupCount=backupCount
            )
        else:
            raise ValueError("Invalid logging handler: {}".format(handler))
        handler.setFormatter(formatter)
        handlers_.append(handler)

    handlers = handlers_

    logging.basicConfig(level=level, handlers=handlers)

    return logging.getLogger(__name__)
