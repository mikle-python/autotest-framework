import pytest
from datetime import datetime

from stress.newben.common.common import get
from libs.log_obj import LogObj

logger = LogObj().get_logger()


@pytest.fixture(scope='session')
def overview_table():
    return 'overview'


@pytest.fixture(scope='session')
def overview_list_table():
    return 'overview_list'


@pytest.fixture(scope='session')
def create_overview_table(mysql_obj, db, overview_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255),
                take_time double,
                c_time DATETIME)""".format(db, overview_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_overview_list_table(mysql_obj, db, overview_list_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255),
                take_time double,
                c_time DATETIME)""".format(db, overview_list_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.mark.usefixtures("create_overview_table")
def test_overview(mysql_obj, api_server, header_after_login, db, overview_table, request_obj, api_performance_data):
    test_overview.__doc__ = 'Test start, test_overview test !'
    logger.info(test_overview.__doc__)

    api_path = api_performance_data['case_module']['overview']['path']['resource_overview']
    overview_url = api_server + api_path

    response, take_time = get(request_obj, overview_url, header_after_login)
    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=overview_table, api=api_path, take_time=take_time, c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert)


@pytest.mark.usefixtures("create_overview_list_table")
def test_overview_list(mysql_obj, api_server, header_after_login, db, overview_list_table, request_obj,
                       api_performance_data):
    test_overview_list.__doc__ = 'Test start, test_overview_list test !'
    logger.info(test_overview_list.__doc__)

    api_path = api_performance_data['case_module']['overview']['path']['resource_overview_list']
    overview_list_url = api_server + api_path

    response, take_time = get(request_obj, overview_list_url, header_after_login)
    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=overview_list_table, api=api_path, take_time=take_time, c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert)
