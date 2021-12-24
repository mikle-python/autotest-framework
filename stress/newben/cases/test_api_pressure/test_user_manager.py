import pytest
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

from libs.log_obj import LogObj
from stress.newben.common.common import create, update, delete, get
from stress.newben.common.user_module_checks import check_search_users

logger = LogObj().get_logger()


@pytest.fixture(scope='session')
def create_user_table():
    return 'create_user'


@pytest.fixture(scope='session')
def modify_user_table():
    return 'modify_user'


@pytest.fixture(scope='session')
def delete_user_table():
    return 'delete_user'


@pytest.fixture(scope='session')
def search_user_table():
    return 'search_user'


@pytest.fixture(scope='session')
def create_create_user_table(mysql_obj, db, create_user_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, create_user_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_modify_user_table(mysql_obj, db, modify_user_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, modify_user_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_delete_user_table(mysql_obj, db, delete_user_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, delete_user_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_search_user_table(mysql_obj, db, search_user_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, search_user_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def request_data(api_performance_data):
    request_datas = []
    for i in range(api_performance_data['common']['data_quantity']):
        data = api_performance_data['case_module']['user_manager']['user_list']['default_create_user_data'].copy()
        data['username'] = "{}-{}".format("admin", i)
        request_datas.append(data)
    return request_datas


@pytest.mark.run(order=1)
@pytest.mark.usefixtures("create_create_user_table")
def test_user_create(mysql_obj, api_server, header_after_login, db, create_user_table, request_obj,
                     api_performance_data, request_data):
    test_user_create.__doc__ = 'Test start, test_user_create test !'
    logger.info(test_user_create.__doc__)
    api_path = api_performance_data['case_module']['user_manager']['user_list']['path']['operate_user']

    create_user_url = api_server + api_path

    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for data in request_data:
        futures.append(pool.submit(create, request_obj, data, header_after_login, create_user_url))
    pool.shutdown()

    for future in as_completed(futures):
        insert_create_api = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                            "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=create_user_table, api=api_path, take_time=future.result()[1], c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert_create_api)


@pytest.mark.run(order=2)
@pytest.mark.usefixtures("create_modify_user_table")
def test_user_modify(mysql_obj, api_server, header_after_login, db, modify_user_table, request_obj,
                     api_performance_data, request_data):
    test_user_modify.__doc__ = 'Test start, test_user_modify test !'
    logger.info(test_user_modify.__doc__)
    api_path = api_performance_data['case_module']['user_manager']['user_list']['path']['operate_user']

    modify_user_url = api_server + api_path

    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for data in request_data:
        request_body = data.copy()
        request_body["password"] = "2"
        del request_body["confPassword"]
        futures.append(pool.submit(update, request_obj, request_body, header_after_login, modify_user_url))
    pool.shutdown()

    for future in as_completed(futures):
        insert_create_api = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                            "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=modify_user_table, api=api_path, take_time=future.result()[1], c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert_create_api)


@pytest.mark.run(order=3)
@pytest.mark.usefixtures("create_search_user_table")
def test_users_search_and_paging(mysql_obj, api_server, header_after_login, db, search_user_table, request_obj,
                                 api_performance_data, request_data):
    test_users_search_and_paging.__doc__ = 'Test start, test_users_search_and_paging test !'
    logger.info(test_users_search_and_paging.__doc__)
    api_path = api_performance_data['case_module']['user_manager']['user_list']['path']['search_users_paging']

    search_users_url = api_server + api_path
    param = {"page": 1, "size": 10, "searchname": "adm"}
    response, take_time = get(request_obj, search_users_url, header_after_login, param)
    check_search_users(response, request_obj, search_users_url, header_after_login, param)
    insert_create_api = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                        "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=search_user_table, api=api_path, take_time=take_time, c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert_create_api)


@pytest.mark.run(order=4)
@pytest.mark.usefixtures("create_delete_user_table")
def test_user_delete(mysql_obj, api_server, header_after_login, db, delete_user_table, request_obj,
                     api_performance_data, request_data):
    test_user_delete.__doc__ = 'Test start, test_user_delete test !'
    logger.info(test_user_delete.__doc__)
    api_path = api_performance_data['case_module']['user_manager']['user_list']['path']['operate_user']

    delete_user_url = api_server + api_path

    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for data in request_data:
        request_body = data.copy()
        del request_body["password"]
        del request_body["confPassword"]
        futures.append(pool.submit(delete, request_obj, delete_user_url, header_after_login, request_body))
    pool.shutdown()

    for future in as_completed(futures):
        insert_create_api = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                            "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=delete_user_table, api=api_path, take_time=future.result()[1], c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert_create_api)
