import copy

import pytest
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

from stress.newben.common.common import create, modify, delete, get, update
from stress.newben.common.space_module_checks import check_list_spaces, check_search_spaces
from libs.log_obj import LogObj

logger = LogObj().get_logger()


@pytest.fixture(scope='session')
def create_node_table():
    return 'create_node'


@pytest.fixture(scope='session')
def list_node_table():
    return 'list_node'


@pytest.fixture(scope='session')
def modify_node_table():
    return 'modify_node'


@pytest.fixture(scope='session')
def view_node_handle_detail_table():
    return 'view_node_handle_detail'


@pytest.fixture(scope='session')
def maintain_node_table():
    return 'maintain_node'


@pytest.fixture(scope='session')
def delete_node_table():
    return 'delete_node'


@pytest.fixture(scope='session')
def create_create_node_table(mysql_obj, db, create_node_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, create_node_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_list_node_table(mysql_obj, db, list_node_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, list_node_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_modify_node_table(mysql_obj, db, modify_node_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, modify_node_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_view_node_handle_detail_table(mysql_obj, db, view_node_handle_detail_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, view_node_handle_detail_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_maintain_node_table(mysql_obj, db, maintain_node_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, maintain_node_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_delete_node_table(mysql_obj, db, delete_node_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, delete_node_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def get_one_node_name(request_obj, api_server, header_after_login, api_performance_data):
    get_nodes_path = api_performance_data['case_module']['host_manager']['host_list']['path']['list_node']
    get_nodes_url = api_server + get_nodes_path
    result, _ = get(request_obj, get_nodes_url, header_after_login)
    node_name = result["data"]["list"][0]["name"]
    return node_name


@pytest.fixture(scope='session')
def get_one_node_detail(request_obj, api_server, header_after_login, api_performance_data, get_one_node_name):
    get_node_detail_path = api_performance_data['case_module']['host_manager']['host_list']['path']['get_node_detail']
    get_node_detail_url = api_server + get_node_detail_path
    param = {"name": get_one_node_name}
    result, _ = get(request_obj, get_node_detail_url, header_after_login, param)
    return result["data"]


@pytest.fixture(scope='session')
def node_create_request_data(api_performance_data, api_server, request_obj, header_after_login):
    workerset_url = api_server + api_performance_data['case_module']['host_manager']['host_list']['path'][
        'get_workerset']
    request_datas = []
    for i in range(api_performance_data['common']['data_quantity']):
        data = copy.deepcopy(
            api_performance_data['case_module']['host_manager']['host_list']['default_create_node_data'])
        result1, _ = get(request_obj, workerset_url, header_after_login, param={"type": "workerset"})
        workerset_name = result1['data']['name']
        result2, _ = get(request_obj, workerset_url, header_after_login, param={"type": "worker"})
        worker_name = result2['data']['name']
        data['name'] = workerset_name
        data['workers'][0]['name'] = worker_name
        request_datas.append(data)
    return request_datas


@pytest.mark.usefixtures("create_list_node_table")
def test_node_list(mysql_obj, api_server, header_after_login, db, list_node_table, request_obj,
                   api_performance_data):
    test_node_list.__doc__ = 'Test start, test_node_list test !'
    logger.info(test_node_list.__doc__)

    api_path = api_performance_data['case_module']['host_manager']['host_list']['path']['list_node']
    list_node_url = api_server + api_path

    response, take_time = get(request_obj, list_node_url, header_after_login)
    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=list_node_table, api=api_path, take_time=take_time, c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert)


@pytest.mark.run(order=1)
@pytest.mark.usefixtures("create_create_node_table")
def test_node_create(mysql_obj, api_server, header_after_login, db, create_node_table, request_obj,
                     api_performance_data, node_create_request_data):
    test_node_create.__doc__ = 'Test start, test_node_create test !'
    logger.info(test_node_create.__doc__)

    api_path = api_performance_data['case_module']['host_manager']['host_list']['path']['create_node']
    create_node_url = api_server + api_path

    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for data in node_create_request_data:
        futures.append(pool.submit(create, request_obj, data, header_after_login, create_node_url))
    pool.shutdown()

    for future in as_completed(futures):
        insert_create_api = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                            "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=create_node_table, api=api_path, take_time=future.result()[1], c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert_create_api)


@pytest.mark.usefixtures("create_modify_node_table")
def test_node_modify(mysql_obj, api_server, header_after_login, db, modify_node_table, request_obj,
                     api_performance_data, node_create_request_data):
    test_node_modify.__doc__ = 'Test start, test_node_modify test !'
    logger.info(test_node_modify.__doc__)

    api_path = api_performance_data['case_module']['host_manager']['host_list']['path']['modify_node']
    modify_node_url = api_server + api_path

    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for data in node_create_request_data:
        data1 = data.copy()
        data1['boxGCInterval'] = 100
        futures.append(pool.submit(update, request_obj, data1, header_after_login, modify_node_url))
    pool.shutdown()

    for future in as_completed(futures):
        insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                 "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=modify_node_table, api=api_path, take_time=future.result()[1], c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert)


@pytest.mark.usefixtures("create_view_node_handle_detail_table")
def test_view_node_handle_detail(mysql_obj, api_server, header_after_login, db, view_node_handle_detail_table,
                                 request_obj, api_performance_data, get_one_node_name):
    test_view_node_handle_detail.__doc__ = 'Test start, test_view_node_handle_detail test !'
    logger.info(test_view_node_handle_detail.__doc__)

    api_path = api_performance_data['case_module']['host_manager']['host_list']['path']['list_node']
    view_node_handle_detail_url = api_server + api_path

    # kind = workerset & name = node2 & page = 1 & size = 10
    param = {'kind': 'workerset', 'page': 1, 'size': 10, 'name': get_one_node_name}
    response, take_time = get(request_obj, view_node_handle_detail_url, header_after_login, param)
    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=view_node_handle_detail_table, api=api_path, take_time=take_time, c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert)


@pytest.mark.usefixtures("create_maintain_node_table")
def test_node_maintain(mysql_obj, api_server, header_after_login, db, maintain_node_table, request_obj,
                       api_performance_data, node_create_request_data):
    test_node_maintain.__doc__ = 'Test start, test_node_maintain test !'
    logger.info(test_node_maintain.__doc__)

    api_path = api_performance_data['case_module']['host_manager']['host_list']['path']['maintain_node']
    maintain_node_url = api_server + api_path

    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for data in node_create_request_data:
        data1 = {"name": data['name'], "maintain": True}
        futures.append(pool.submit(update, request_obj, data1, header_after_login, maintain_node_url))
    pool.shutdown()

    for future in as_completed(futures):
        insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                 "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=maintain_node_table, api=api_path, take_time=future.result()[1], c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert)


@pytest.mark.run(order=5)
@pytest.mark.usefixtures("create_delete_node_table")
def test_node_delete(mysql_obj, api_server, header_after_login, db, delete_node_table, request_obj,
                     api_performance_data, node_create_request_data):
    test_node_delete.__doc__ = 'Test start, test_node_delete test !'
    logger.info(test_node_delete.__doc__)

    api_path = api_performance_data['case_module']['host_manager']['host_list']['path']['delete_node']
    delete_node_url = api_server + api_path

    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for data in node_create_request_data:
        data1 = {}
        data1['name'] = data['name']
        futures.append(pool.submit(delete, request_obj, delete_node_url, header_after_login, data1))
    pool.shutdown()

    for future in as_completed(futures):
        insert_create_api = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                            "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=delete_node_table, api=api_path, take_time=future.result()[1], c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert_create_api)
