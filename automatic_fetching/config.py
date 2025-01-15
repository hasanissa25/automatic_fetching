'''
..  codeauthor:: Hasan Issa <Hasan.issa@canada.ca>
'''
from functools import lru_cache

from enum import Enum
import logging


from pydantic_settings import BaseSettings


class LogLevels(Enum):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'


class BaseAppSettings(BaseSettings):
    # Env variables
    log_level: LogLevels = LogLevels.INFO
    log_format: str = '%(asctime)s.%(msecs)03d %(levelname)s \
%(module)s %(funcName)s: %(message)s'
    log_datefmt: str = '%Y-%m-%d %H:%M:%S'

    class Config:
        env_prefix = 'automaticfetching_'
        env_file = ".env"

    def configure_logging(self):
        '''
        Configure logging for app
        '''
        level = {
            LogLevels.DEBUG: logging.DEBUG,
            LogLevels.INFO: logging.INFO,
            LogLevels.WARNING: logging.WARNING,
            LogLevels.ERROR: logging.ERROR,
        }[self.log_level]
        logging.basicConfig(
            format=self.log_format,
            datefmt=self.log_datefmt,
            level=level)


@lru_cache()
def get_app_settings() -> BaseAppSettings:
    return BaseAppSettings()
