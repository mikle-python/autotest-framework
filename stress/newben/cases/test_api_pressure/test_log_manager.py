import random
import time
import pytest
from datetime import datetime

from stress.newben.common.common import get
from libs.log_obj import LogObj

logger = LogObj().get_logger()


@pytest.fixture(scope='session')
def query_event_log_table():
    return 'query_event_log'


@pytest.fixture(scope='session')
def query_audit_log_table():
    return 'query_audit_log'


@pytest.fixture(scope='session')
def create_query_event_log_table(mysql_obj, db, query_event_log_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255),
                take_time double,
                c_time DATETIME)""".format(db, query_event_log_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_query_audit_log_table(mysql_obj, db, query_audit_log_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255),
                take_time double,
                c_time DATETIME)""".format(db, query_audit_log_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def get_components_name(request_obj, api_server, header_after_login, api_performance_data):
    get_components_path = api_performance_data['case_module']['log_manager']['event_log']['path']['get_components']
    get_components_url = api_server + get_components_path
    result, _ = get(request_obj, get_components_url, header_after_login)
    components_name = [data["componentName"] for data in result["data"]["items"]]
    return components_name


@pytest.fixture(scope='session')
def get_workers_name(request_obj, api_server, header_after_login, api_performance_data):
    get_workers_path = api_performance_data['case_module']['log_manager']['event_log']['path']['get_workers']
    get_workers_url = api_server + get_workers_path
    result, _ = get(request_obj, get_workers_url, header_after_login)
    workers_name = [data["workerName"] for data in result["data"]["items"]]
    return workers_name


@pytest.fixture(scope='session')
def get_handle_accounts_name(request_obj, api_server, header_after_login, api_performance_data):
    get_handle_accounts_path = api_performance_data['case_module']['log_manager']['audit_log']['path'][
        'get_handle_accounts']
    get_handle_accounts_url = api_server + get_handle_accounts_path
    result, _ = get(request_obj, get_handle_accounts_url, header_after_login)
    handle_accounts_name = [data["value"] for data in result["data"]]
    return handle_accounts_name


@pytest.fixture(scope='session')
def get_handle_actions_name(request_obj, api_server, header_after_login, api_performance_data):
    get_handle_accounts_path = api_performance_data['case_module']['log_manager']['audit_log']['path'][
        'get_handle_actions']
    get_handle_actions_url = api_server + get_handle_accounts_path
    result, _ = get(request_obj, get_handle_actions_url, header_after_login)
    handle_actions_name = [data["value"] for data in result["data"]]
    return handle_actions_name


@pytest.fixture(scope='function')
def event_log_request_data(get_components_name, get_workers_name, api_performance_data):
    data = api_performance_data['case_module']['log_manager']['event_log']['default_query_param'].copy()
    component_name = random.choice(get_components_name)
    worker_name = random.choice(get_workers_name)
    level = random.choice(list(api_performance_data['case_module']['log_manager']['log_level'].values()))
    start_time = int(time.mktime(time.strptime(
        api_performance_data['case_module']['log_manager']['event_log']['default_query_param']['startTime'],
        "%Y-%m-%d %H:%M:%S")))
    end_time = int(time.mktime(time.strptime(
        api_performance_data['case_module']['log_manager']['event_log']['default_query_param']['endTime'],
        "%Y-%m-%d %H:%M:%S")))
    data["componentName"] = component_name
    data["workerName"] = worker_name
    data["level"] = level
    data["startTime"] = start_time
    data["endTime"] = end_time
    logger.debug(data)
    return data


@pytest.fixture(scope='function')
def audit_log_request_data(get_handle_accounts_name, get_handle_actions_name, api_performance_data):
    data = api_performance_data['case_module']['log_manager']['audit_log']['default_query_param'].copy()
    handle_account_name = random.choice(get_handle_accounts_name)
    handle_action_name = random.choice(get_handle_actions_name)
    data["user_name"] = handle_account_name
    data["action"] = handle_action_name
    logger.debug(data)
    return data


@pytest.mark.usefixtures("create_query_event_log_table")
def test_query_event_log(mysql_obj, api_server, header_after_login, db, query_event_log_table,
                         request_obj, api_performance_data, event_log_request_data):
    test_query_event_log.__doc__ = 'Test start, test_query_event_log test !'
    logger.info(test_query_event_log.__doc__)

    api_path = api_performance_data['case_module']['log_manager']['event_log']['path']['query_log']
    query_event_log_url = api_server + api_path

    response, take_time = get(request_obj, query_event_log_url, header_after_login, event_log_request_data)
    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=query_event_log_table, api=api_path, take_time=take_time, c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert)


@pytest.mark.usefixtures("create_query_audit_log_table")
def test_query_audit_log(mysql_obj, api_server, header_after_login, db, query_audit_log_table,
                         request_obj, api_performance_data, audit_log_request_data):
    test_query_audit_log.__doc__ = 'Test start, test_query_audit_log test !'
    logger.info(test_query_audit_log.__doc__)

    api_path = api_performance_data['case_module']['log_manager']['audit_log']['path']['query_log']
    query_audit_log_url = api_server + api_path

    response, take_time = get(request_obj, query_audit_log_url, header_after_login, audit_log_request_data)
    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=query_audit_log_table, api=api_path, take_time=take_time, c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert)
