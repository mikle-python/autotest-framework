import pytest
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

from stress.newben.common.common import create, modify, delete, get
from stress.newben.common.space_module_checks import check_list_spaces, check_search_spaces
from libs.log_obj import LogObj

logger = LogObj().get_logger()


@pytest.fixture(scope='session')
def create_space_table():
    return 'create_space'


@pytest.fixture(scope='session')
def modify_space_table():
    return 'modify_space'


@pytest.fixture(scope='session')
def delete_space_table():
    return 'delete_space'


@pytest.fixture(scope='session')
def list_space_table():
    return 'list_space'


@pytest.fixture(scope='session')
def search_space_table():
    return 'search_space'


@pytest.fixture(scope='session')
def create_create_space_table(mysql_obj, db, create_space_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, create_space_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_modify_space_table(mysql_obj, db, modify_space_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, modify_space_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_delete_space_table(mysql_obj, db, delete_space_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, delete_space_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_list_space_table(mysql_obj, db, list_space_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, list_space_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_search_space_table(mysql_obj, db, search_space_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, search_space_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def request_data(api_performance_data):
    request_datas = []
    for i in range(api_performance_data['common']['data_quantity']):
        data = api_performance_data['case_module']['space_manager']['space_list']['default_create_space_data'].copy()
        data['name'] = "{}-{}".format("system", i)
        request_datas.append(data)
    return request_datas


@pytest.mark.run(order=1)
@pytest.mark.usefixtures("create_create_space_table")
def test_space_create(mysql_obj, api_server, header_after_login, db, create_space_table, request_obj,
                      api_performance_data, request_data):
    test_space_create.__doc__ = 'Test start, test_space_create test !'
    logger.info(test_space_create.__doc__)
    api_path = api_performance_data['case_module']['space_manager']['space_list']['path']['create_space']

    create_space_url = api_server + api_path

    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for data in request_data:
        futures.append(pool.submit(create, request_obj, data, header_after_login, create_space_url))
    pool.shutdown()

    for future in as_completed(futures):
        insert_create_api = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                            "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=create_space_table, api=api_path, take_time=future.result()[1], c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert_create_api)


@pytest.mark.run(order=2)
@pytest.mark.usefixtures("create_modify_space_table")
def test_space_modify(mysql_obj, api_server, header_after_login, db, modify_space_table, request_obj,
                      api_performance_data, request_data):
    test_space_modify.__doc__ = 'Test start, test_space_modify test !'
    logger.info(test_space_modify.__doc__)
    api_path = api_performance_data['case_module']['space_manager']['space_list']['path']['modify_space']

    modify_space_url = api_server + api_path

    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for data in request_data:
        request_body = data.copy()
        request_body["description"] = "空间描述信息"
        futures.append(pool.submit(modify, request_obj, request_body, header_after_login, modify_space_url))
    pool.shutdown()

    for future in as_completed(futures):
        insert_create_api = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                            "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=modify_space_table, api=api_path, take_time=future.result()[1], c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert_create_api)


@pytest.mark.run(order=3)
@pytest.mark.usefixtures("create_list_space_table")
def test_spaces_list(mysql_obj, api_server, header_after_login, db, list_space_table, request_obj,
                     api_performance_data, request_data):
    test_spaces_list.__doc__ = 'Test start, test_space_list test !'
    logger.info(test_spaces_list.__doc__)
    api_path = api_performance_data['case_module']['space_manager']['space_list']['path']['get_spaces']

    list_space_url = api_server + api_path
    response, take_time = get(request_obj, list_space_url, header_after_login)
    check_list_spaces(response)
    insert_create_api = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                        "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=list_space_table, api=api_path, take_time=take_time, c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert_create_api)


@pytest.mark.run(order=4)
@pytest.mark.usefixtures("create_search_space_table")
def test_spaces_search_and_paging(mysql_obj, api_server, header_after_login, db, search_space_table, request_obj,
                                  api_performance_data, request_data):
    test_spaces_search_and_paging.__doc__ = 'Test start, test_spaces_search_and_paging test !'
    logger.info(test_spaces_search_and_paging.__doc__)
    api_path = api_performance_data['case_module']['space_manager']['space_list']['path']['search_spaces_paging']

    search_spaces_url = api_server + api_path
    param = {"page": 1, "size": 10, "searchname": "syst"}
    response, take_time = get(request_obj, search_spaces_url, header_after_login, param)
    check_search_spaces(response, request_obj, search_spaces_url, header_after_login, param)
    insert_create_api = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                        "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=search_space_table, api=api_path, take_time=take_time, c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert_create_api)


@pytest.mark.run(order=5)
@pytest.mark.usefixtures("create_delete_space_table")
def test_space_delete(mysql_obj, api_server, header_after_login, db, delete_space_table, request_obj,
                      api_performance_data, request_data):
    test_space_delete.__doc__ = 'Test start, test_space_delete test !'
    logger.info(test_space_delete.__doc__)
    api_path = api_performance_data['case_module']['space_manager']['space_list']['path']['delete_space']

    delete_space_url = api_server + api_path

    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for data in request_data:
        request_body = data.copy()
        del request_body["description"]
        futures.append(pool.submit(delete, request_obj, delete_space_url, header_after_login, request_body))
    pool.shutdown()

    for future in as_completed(futures):
        insert_create_api = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                            "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=delete_space_table, api=api_path, take_time=future.result()[1], c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert_create_api)
