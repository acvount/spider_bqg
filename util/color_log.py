import logging
import colorlog
import threading


class Log:
    def __init__(self):
        self.local_logger = threading.local()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s \t %(levelname)s \t:\t%(message)s',
            log_colors={
                'DEBUG': 'reset',
                'INFO': 'purple',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            },
            reset=True,
            style='%'
        )
        self._create_console_handler()

    def _create_console_handler(self):
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self.formatter)
        self.local_logger.console_handler = console_handler

    def _get_thread_logger(self):
        if not hasattr(self.local_logger, 'logger'):
            logger = logging.getLogger(__name__)
            logger.setLevel(logging.INFO)
            logger.addHandler(self.local_logger.console_handler)
            self.local_logger.logger = logger
        return self.local_logger.logger

    def info(self, info):
        logger = self._get_thread_logger()
        logger.info(info)

    def error(self, info):
        logger = self._get_thread_logger()
        logger.error(info)

    def sql(self, info):
        logger = self._get_thread_logger()
        logger.info(info)
