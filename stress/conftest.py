import pytest
from stress import arguments
from libs.log_obj import LogObj


args = arguments.parse_arg()
logger = LogObj().get_logger()


def pytest_configure(config):
    if 'ip' in args and args.ip:
        config._metadata['Testbed'] = args.ip