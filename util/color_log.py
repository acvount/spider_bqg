import logging
import colorlog
import threading


class Log:
    def __init__(self):
        self.local_logger = threading.local()  # 创建线程专属的 Logger 对象

        self.logger = logging.getLogger(__name__)  # 创建实例的 Logger 对象
        self.logger.setLevel(logging.INFO)
        self.formatter = colorlog.ColoredFormatter(
            '%(asctime)s - %(log_color)s%(levelname)s - %(message)s',
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
        self.console_handler = logging.StreamHandler()
        self.console_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.console_handler)

    def _get_thread_logger(self):
        if not hasattr(self.local_logger, 'logger'):  # 每个线程使用独立的 Logger 对象
            self.local_logger.logger = logging.getLogger(__name__)
            self.local_logger.logger.setLevel(logging.INFO)
            self.local_logger.logger.addHandler(self.console_handler)
        return self.local_logger.logger

    def info(self, info):
        logger = self._get_thread_logger()
        logger.info(info)

    def error(self, info):
        logger = self._get_thread_logger()
        logger.error(info)

    def sql(self, info):
        logger = self._get_thread_logger()
        logger.debug(info)
