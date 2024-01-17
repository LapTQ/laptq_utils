import logging
import sys
import os


def load_logger(
        **kwargs
):
    level = kwargs.get('level', logging.INFO)
    format = kwargs.get('format', '%(asctime)s\t|%(funcName)20s |%(lineno)d\t|%(levelname)8s |%(message)s')
    directory = kwargs.get('directory', None)
    handlers = kwargs.get('handlers', 'stdout')

    if level == 'DEBUG':
        level = logging.DEBUG
    elif level == 'INFO':
        level = logging.INFO
    elif level == 'WARNING':
        level = logging.WARNING
    elif level == 'ERROR':
        level = logging.ERROR
    elif level == 'CRITICAL':
        level = logging.CRITICAL
    else:
        raise ValueError('Invalid logging level: {}'.format(level))

    handlers_ = []
    if not isinstance(handlers, list):
        handlers = [handlers]
    for handler in handlers:
        if handler == 'stdout':
            handlers_.append(logging.StreamHandler(sys.stdout))
        elif isinstance(handler, str):
            assert directory is not None, 'Logging directory must be specified when using file handler.'
            assert os.path.isdir(directory), 'Logging directory must be a directory.'
            log_fpath = os.path.join(directory, handler)
            handlers_.append(logging.FileHandler(log_fpath))
        else:
            raise ValueError('Invalid logging handler: {}'.format(handler))
    handlers = handlers_

    logging.basicConfig(
        level=level,
        format=format,
        handlers=handlers
    )

    return logging.getLogger(__name__)
