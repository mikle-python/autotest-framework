import pytest
import os
import json
from libs.mysql_obj import MysqlObj
from stress.newben.common.common import create_api
from common.common import load_yaml
from settings.global_settings import PROJECT_PATH
from libs.request_obj import RequstObj
from libs.log_obj import LogObj

logger = LogObj().get_logger()

api_header_after_login = dict()


@pytest.fixture(scope='session')
def request_obj():
    return RequstObj()


@pytest.fixture(scope='session')
def api_performance_data():
    return load_yaml(os.path.join(PROJECT_PATH, 'stress/newben/config/ApiPerformance.yaml'))


@pytest.fixture(scope='session')
def api_server(api_performance_data):
    return api_performance_data['common']['api_server'] + api_performance_data['common']['port']


@pytest.fixture(scope='session')
def uid_api_server(api_performance_data):
    return api_performance_data['common']['uid_api_server'] + api_performance_data['common']['port']


@pytest.fixture(scope='session')
def header_after_login(request_obj, api_performance_data, api_server):
    login_data = {
        "username": api_performance_data['common']['login_info']['username'],
        "password": api_performance_data['common']['login_info']['password'],
        "provider": api_performance_data['common']['login_info']['provider']
    }

    login_headers = api_performance_data['common']['header']['header_without_token']
    login_url = api_server + api_performance_data['common']['path']['login_path']

    login_response = request_obj.call('post', login_url, data=json.dumps(login_data), headers=login_headers).json()

    if login_response['code'] == 200:
        logger.info("Login api server {} successfully !".format(login_url))
        global api_header_after_login
        api_header_after_login = api_performance_data['common']['header']['header_without_token'].copy()
        api_header_after_login['Authorization'] = login_response['data']
        api_header_after_login['workspace'] = api_performance_data['common']['workspace']
        return api_header_after_login
    else:
        raise Exception("Login api server {} failed, the error messages are [{}]".
                        format(login_url, login_response))


@pytest.fixture(scope='function', autouse=True)
def certify_token_is_expired(header_after_login, api_performance_data, api_server, request_obj):
    api_path = api_performance_data['case_module']['overview']['path']['resource_overview']
    overview_url = api_server + api_path

    response = request_obj.call('get', overview_url, headers=header_after_login)
    response_json = response.json()

    login_data = {
        "username": api_performance_data['common']['login_info']['username'],
        "password": api_performance_data['common']['login_info']['password'],
        "provider": api_performance_data['common']['login_info']['provider']
    }

    login_headers = api_performance_data['common']['header']['header_without_token']
    login_url = api_server + api_performance_data['common']['path']['login_path']

    if response_json['code'] == 401 and 'token is expired' in response_json['message']:
        logger.warning("The token is expired!")
        login_response = request_obj.call('post', login_url, data=json.dumps(login_data),
                                          headers=login_headers).json()
        if login_response['code'] == 200:
            logger.info("Login api server {} successfully !".format(login_url))
            global api_header_after_login
            api_header_after_login['Authorization'] = login_response['data']


@pytest.fixture(scope='session')
def mysql_obj(api_performance_data):
    return MysqlObj(api_performance_data['common']['mysql']['host'],
                    api_performance_data['common']['mysql']['username'],
                    api_performance_data['common']['mysql']['password'])


@pytest.fixture(scope='session')
def db(api_performance_data):
    server_ip = api_performance_data['common']['api_server_ip']
    return '{}_newben'.format(server_ip.replace('.', '_'))


@pytest.fixture(scope='session', autouse=True)
def create_db(mysql_obj, db):
    create_db = 'create database if not exists {0}'.format(db)
    mysql_obj.run_sql_cmd(create_db)


@pytest.fixture(scope='session')
def create_api_table():
    return 'create_api'


@pytest.fixture(scope='session')
def list_api_table():
    return 'list_api'


@pytest.fixture(scope='session')
def delete_api_table():
    return 'delete_api'


@pytest.fixture(scope='session')
def update_api_table():
    return 'update_api'


@pytest.fixture(scope='session')
def create_create_api_table(mysql_obj, db, create_api_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, create_api_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_list_api_table(mysql_obj, db, list_api_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, list_api_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_delete_api_table(mysql_obj, db, delete_api_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, delete_api_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_update_api_table(mysql_obj, db, update_api_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, update_api_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session', autouse=True)
def switch_workspace(request_obj, header_after_login, api_server, api_performance_data):
    data = {
        "name": api_performance_data['common']['workspace']
    }
    url = api_server + api_performance_data['common']['path']['witch_workspace']
    create_api(request_obj, data, header_after_login, url)
