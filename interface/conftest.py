import os
import pytest
from common.common import load_yaml
from settings.global_settings import PROJECT_PATH
from interface import arguments


args = arguments.parse_arg()


def pytest_configure(config):
    if 'ip' in args and args.ip:
        config._metadata['Testbed'] = args.ip


@pytest.fixture(scope='session')
def global_config():
    return load_yaml(os.path.join(PROJECT_PATH, 'interface/config/config.yaml'))