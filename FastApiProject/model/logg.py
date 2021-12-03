# Python记录日志
import logging
import os

__dir__ = os.path.dirname(__file__)
__log_path__ = f'{__dir__}/log/'


class Log(object):

    def __init__(self, name, path=None):
        if path is None:
            self.path = __log_path__
        else:
            self.path = path
        self.name = name
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.INFO)
        self.sh = logging.StreamHandler()
        self.sh.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] >> %(message)s')
        self.sh.setFormatter(self.formatter)
        self.logger.addHandler(self.sh)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def close(self):
        self.logger.removeHandler(self.sh)
