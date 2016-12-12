import logging
import os


_configured = False


def _is_configured():
    return _is_configured


def _configure(level):
    global _configured #pylint: disable=I0011,global-statement
    if not _is_configured():
        logging.basicConfig(format="[%(levelname)s] %(filename)s %(message)s", level=level)
        _configured = True


def get_level():
    level = os.environ.get("LAZYSUSAN_LOG_LEVEL", "logging.WARN")
    if not level.startswith("logging."):
        level = logging.WARN
    else:
        level = eval(level) #pylint: disable=I0011,eval-used
    return level


def get_logger(name="LazySusan"):
    """Return a named logger.

    Note, this should be called one time per named logger.

    """
    level = get_level()
    _configure(level)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    return logger
