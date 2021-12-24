import pytest
import os
from copy import deepcopy
from libs.log_obj import LogObj
from common.common import load_yaml
from settings.global_settings import PROJECT_PATH

logger = LogObj().get_logger()


@pytest.fixture(scope='session')
def api_data_for_devops():
    return load_yaml(os.path.join(PROJECT_PATH, 'stress/devops/config/api_stress.yaml'))


@pytest.fixture(scope='session')
def api_login_data(api_data_for_devops):
    data_login_copy = deepcopy(api_data_for_devops)['login_info']
    data_common_copy = deepcopy(api_data_for_devops)['common']

    login_data = {
        "username": data_login_copy['username'],
        "password": data_login_copy['password'],
        "provider": data_login_copy['provider']
    }
    login_headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/96.0.4664.45 Safari/537.36"
    }
    login_url = data_common_copy['api_server'] + data_login_copy['login_path']

    return {'login_data': login_data, 'login_headers': login_headers, 'login_url': login_url}


@pytest.fixture(scope='session')
def api_mysql_data(api_data_for_devops):
    return api_data_for_devops['database']['table_names']


@pytest.fixture(scope='session')
def project_data(api_data_for_devops):
    data_copy = deepcopy(api_data_for_devops)['project']

