import os
import pytest
from py._xmlgen import html
from common.common import load_yaml
from settings.global_settings import PROJECT_PATH


@pytest.fixture(scope='session')
def api_config():
    return load_yaml(os.path.join(PROJECT_PATH, 'interface/api/config/config.yaml'))