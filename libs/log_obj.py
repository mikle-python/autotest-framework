import logging
import logging.handlers
import os
import threading
from settings.global_settings import PYTHON_MAJOR_VERSION


# file log level
FILE_LEVEL = logging.DEBUG
# console log level
CONSOLE_LEVEL = logging.DEBUG
# RotatingFileHandler backupCount
FILE_BACKUPCOUNT = 300
# RotatingFileHandler maxBytes
FILE_MAXBYTES = 20 * 1024 * 1024
# date formate
DATE_FORMATE = '%Y-%m-%d %H:%M:%S'
# file log format
FILE_FORMATE = '%(asctime)s %(filename)s[%(lineno)d] [PID:%(process)d] [TID:%(thread)d] %(levelname)s: %(message)s'
# console log format
CONSOLE_FORMATE = '%(asctime)s %(filename)s[%(lineno)d] [PID:%(process)d] [TID:%(thread)d] %(levelname)s: %(message)s'


class LogObj(object):
    _instance_lock = threading.Lock()

    def __new__(cls, log_dir=os.path.join(os.getcwd(), 'log/'), log_file_name='debug.log',
                logger_name='ghostcloudtest'):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    if PYTHON_MAJOR_VERSION > 2:
                        cls._instance = super(LogObj, cls).__new__(cls)
                    else:
                        cls._instance = super(LogObj, cls).__new__(cls, log_file_name, logger_name)

                    cls._instance.log_dir = log_dir
                    cls._instance.logger = logging.getLogger(logger_name)
                    cls._instance.logger.setLevel(logging.DEBUG)
                    if not os.path.exists(log_dir):
                        os.makedirs(log_dir)

                    # file
                    file_path_name = os.path.join(log_dir, log_file_name)
                    cls._instance.file_handler = logging.handlers.RotatingFileHandler(file_path_name, mode='a',
                                                                                      maxBytes=FILE_MAXBYTES,
                                                                                      backupCount=FILE_BACKUPCOUNT)
                    cls._instance.file_handler.setLevel(FILE_LEVEL)
                    cls._instance.file_handler.setFormatter(logging.Formatter(FILE_FORMATE))
                    cls._instance.logger.addHandler(cls._instance.file_handler)

                    # console
                    cls._instance.console_handler = logging.StreamHandler()
                    cls._instance.console_handler.setLevel(CONSOLE_LEVEL)
                    cls._instance.console_handler.setFormatter(logging.Formatter(CONSOLE_FORMATE))
                    cls._instance.logger.addHandler(cls._instance.console_handler)

        return cls._instance

    def __init__(self, log_file_name='debug.log', logger_name='pztest'):
        self.logger_name = logger_name
        self.log_file_name = log_file_name

    def get_logger(self):
        return self.logger


if __name__ == '__main__':
    logger = LogObj('C:\\Project\\Python\\ghostcloudtest\\log/2021-07-30-18-05-43.log').get_logger()
    logger.info('info!')
    logger.debug('debug!')
    logger.warning('warning!')