import logging


class Logger(object):
    """Base MEG logging class."""

    @staticmethod
    def debug(self, message):
        logger = logging.getLogger(__name__)
        logger.debug(message)

    @staticmethod
    def warning(self, message):
        logger = logging.getLogger(__name__)
        logger.debug(message)
