import pytest
import json
import os

from libs.mysql_obj import MysqlObj
from libs.log_obj import LogObj
from common.common import load_yaml
from libs.request_obj import RequstObj
from settings.global_settings import PROJECT_PATH

logger = LogObj().get_logger()


@pytest.fixture(scope='session')
def request_obj():
    return RequstObj()


@pytest.fixture(scope='session')
def devops_test_data():
    return load_yaml(os.path.join(PROJECT_PATH, 'stress/devops/config/devops.yaml'))


@pytest.fixture(scope='session')
def auth_token(request_obj, devops_test_data):
    login_data = {
        "username": devops_test_data['login_info']['username'],
        "password": devops_test_data['login_info']['password'],
        "provider": devops_test_data['login_info']['provider']
    }
    login_headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/96.0.4664.45 Safari/537.36"
    }
    login_url = devops_test_data['common']['api_server'] + devops_test_data['login_info']['login_path']
    login_response = request_obj.call('post', login_url, data=json.dumps(login_data), headers=login_headers).json()
    if login_response['code'] == "200" and login_response['message'] == "success":
        logger.info("Login api server {} successfully !".format(login_url))
        return login_response['data']['token']
    else:
        raise Exception("Login api server {} failed, the error messages are [{}]".
                        format(login_url, login_response))


@pytest.fixture(scope='session')
def header_after_login(devops_test_data, auth_token):
    pipeline_header = devops_test_data['common']['header_after_login'].copy()
    pipeline_header['Authorization'] = auth_token
    return pipeline_header


@pytest.fixture(scope='session')
def mysql_obj(devops_test_data):
    return MysqlObj(devops_test_data['common']['mysql']['host'], devops_test_data['common']['mysql']['username'],
                    devops_test_data['common']['mysql']['password'])


@pytest.fixture(scope='session')
def mysql_show_obj(devops_test_data):
    return MysqlObj(devops_test_data['common']['show_mysql']['host'],
                    devops_test_data['common']['show_mysql']['username'],
                    devops_test_data['common']['show_mysql']['password'])
