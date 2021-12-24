import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

import pytest

from libs.log_obj import LogObj
from stress.newben.common.common import create, get, delete
from stress.newben.common.storage_module_checks import check_search_storage_pool, check_search_storage_volume, \
    check_all_create_storage_status

logger = LogObj().get_logger()


@pytest.fixture(scope='session')
def storage_pool_type_table():
    return 'storage_pool_type'


@pytest.fixture(scope='session')
def worker_name_table():
    return 'worker_name'


@pytest.fixture(scope='session')
def create_storage_pool_table():
    return 'create_storage_pool'


@pytest.fixture(scope='session')
def search_storage_pool_table():
    return 'search_storage_pool'


@pytest.fixture(scope='session')
def storage_pool_view_detail_table():
    return 'storage_pool_view_detail'


@pytest.fixture(scope='session')
def storage_pool_view_handle_detail_table():
    return 'storage_pool_view_handle_detail'


@pytest.fixture(scope='session')
def delete_storage_pool_table():
    return 'delete_storage_pool'


@pytest.fixture(scope='session')
def storage_pool_name_list_table():
    return 'storage_pool_name_list'


@pytest.fixture(scope='session')
def create_storage_volume_table():
    return 'create_storage_volume'


@pytest.fixture(scope='session')
def search_storage_volume_table():
    return 'search_storage_volume'


@pytest.fixture(scope='session')
def view_storage_volume_config_table():
    return 'view_storage_volume_config'


@pytest.fixture(scope='session')
def view_storage_volume_handle_detail_table():
    return 'view_storage_volume_handle_detail'


@pytest.fixture(scope='session')
def delete_storage_volume_table():
    return 'delete_storage_volume'


@pytest.fixture(scope='session')
def create_storage_pool_type_table(mysql_obj, db, storage_pool_type_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, storage_pool_type_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_worker_name_table(mysql_obj, db, worker_name_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, worker_name_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_create_storage_pool_table(mysql_obj, db, create_storage_pool_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, create_storage_pool_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_search_storage_pool_table(mysql_obj, db, search_storage_pool_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, search_storage_pool_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_storage_pool_view_detail_table(mysql_obj, db, storage_pool_view_detail_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, storage_pool_view_detail_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_storage_pool_view_handle_detail_table(mysql_obj, db, storage_pool_view_handle_detail_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, storage_pool_view_handle_detail_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_storage_pool_name_list_table(mysql_obj, db, storage_pool_name_list_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, storage_pool_name_list_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_delete_storage_pool_table(mysql_obj, db, delete_storage_pool_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, delete_storage_pool_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_create_storage_volume_table(mysql_obj, db, create_storage_volume_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, create_storage_volume_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_search_storage_volume_table(mysql_obj, db, search_storage_volume_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, search_storage_volume_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_view_storage_volume_config_table(mysql_obj, db, view_storage_volume_config_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, view_storage_volume_config_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_view_storage_volume_handle_detail_table(mysql_obj, db, view_storage_volume_handle_detail_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, view_storage_volume_handle_detail_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_delete_storage_volume_table(mysql_obj, db, delete_storage_volume_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, delete_storage_volume_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def storage_pool_request_data(request_obj, api_server, header_after_login, api_performance_data):
    request_datas = []
    data = api_performance_data['case_module']['storage_manager']['storage_pool']['default_create_storage_pool_data']
    api_path = api_performance_data['case_module']['storage_manager']['storage_pool']['path']['get_worker_name']
    worker_name_url = api_server + api_path
    response, _ = get(request_obj, worker_name_url, header_after_login, param={'provisioner': 'LocalStorage'})
    worker_names = [worker['workerName'] for worker in response['data']]
    hosts = [worker['host'] for worker in response['data']]
    for i in range(api_performance_data['common']['data_quantity']):
        storage_pool_type = random.choice(list(data.keys()))
        if storage_pool_type == 'local_storage':
            data1 = data['local_storage'].copy()
            data1['name'] = '{}-{}'.format('storage-pool', i)
            data1['workerName'] = random.choice(worker_names)
            data1['parameters']['host'] = random.choice(hosts)
        elif storage_pool_type == 'glusterfs':
            data1 = data['glusterfs'].copy()
            data1['name'] = '{}-{}'.format('storage-pool', i)
        elif storage_pool_type == 'cephfs':
            data1 = data['cephfs'].copy()
            data1['name'] = '{}-{}'.format('storage-pool', i)
        elif storage_pool_type == 'cephrbd':
            data1 = data['cephrbd'].copy()
            data1['name'] = '{}-{}'.format('storage-pool', i)
        else:
            data1 = {}
        request_datas.append(data1)
    return request_datas


@pytest.fixture(scope='session')
def storage_volume_request_data(request_obj, api_server, header_after_login, api_performance_data):
    request_datas = []
    api_path = api_performance_data['case_module']['storage_manager']['storage_volume']['path'][
        'get_storage_pool_list']
    storage_pool_list_url = api_server + api_path
    response, _ = get(request_obj, storage_pool_list_url, header_after_login)
    storage_pool_name_list = [data['name'] for data in response['data']]
    for i in range(api_performance_data['common']['data_quantity']):
        data = api_performance_data['case_module']['storage_manager']['storage_volume'][
            'default_create_storage_volume_data']['local_storage'].copy()
        data['name'] = "{}-{}".format("storage-volume", i)
        data['storagePool'] = random.choice(storage_pool_name_list)
        data['accessMode'] = random.choice(data['accessMode'])
        request_datas.append(data)
    return request_datas


@pytest.mark.usefixtures("create_storage_pool_type_table")
def test_storage_pool_type(mysql_obj, api_server, header_after_login, db, storage_pool_type_table,
                           request_obj, api_performance_data):
    test_storage_pool_type.__doc__ = 'Test start, test_storage_pool_type test !'
    logger.info(test_storage_pool_type.__doc__)

    api_path = api_performance_data['case_module']['storage_manager']['storage_pool']['path']['get_storage_pool_type']
    storage_pool_type_url = api_server + api_path

    response, take_time = get(request_obj, storage_pool_type_url, header_after_login)
    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=storage_pool_type_table, api=api_path, take_time=take_time, c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert)


@pytest.mark.usefixtures("create_worker_name_table")
def test_worker_name_list(mysql_obj, api_server, header_after_login, db, worker_name_table,
                          request_obj, api_performance_data):
    test_worker_name_list.__doc__ = 'Test start, test_worker_name_list test !'
    logger.info(test_worker_name_list.__doc__)

    api_path = api_performance_data['case_module']['storage_manager']['storage_pool']['path']['get_worker_name']
    worker_name_url = api_server + api_path

    param = {'provisioner': 'LocalStorage'}
    response, take_time = get(request_obj, worker_name_url, header_after_login, param)
    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=worker_name_table, api=api_path, take_time=take_time, c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert)


@pytest.mark.run(order=1)
@pytest.mark.usefixtures("create_create_storage_pool_table")
def test_storage_pool_create(mysql_obj, api_server, header_after_login, db, create_storage_pool_table, request_obj,
                             api_performance_data, storage_pool_request_data):
    test_storage_pool_create.__doc__ = 'Test start, test_storage_pool_create test !'
    logger.info(test_storage_pool_create.__doc__)

    api_path = api_performance_data['case_module']['storage_manager']['storage_pool']['path']['create_storage_pool']
    create_storage_pool_url = api_server + api_path

    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for data in storage_pool_request_data:
        futures.append(pool.submit(create, request_obj, data, header_after_login, create_storage_pool_url))
    pool.shutdown()

    for future in as_completed(futures):
        insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                 "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=create_storage_pool_table, api=api_path, take_time=future.result()[1],
                    c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert)

    api_path = api_performance_data['case_module']['storage_manager']['storage_pool']['path']['search_storage_pool']
    get_storage_pool_url = api_server + api_path
    param = {"page": 1, "size": 10}
    create_storage_pool_names = [data["name"] for data in storage_pool_request_data]
    check_all_create_storage_status(request_obj, get_storage_pool_url, header_after_login, param,
                                    create_storage_pool_names)


@pytest.mark.run(order=2)
@pytest.mark.usefixtures("create_search_storage_pool_table")
def test_storage_pool_search_and_paging(mysql_obj, api_server, header_after_login, db, search_storage_pool_table,
                                        request_obj, api_performance_data):
    test_storage_pool_search_and_paging.__doc__ = 'Test start, test_storage_pool_search_and_paging test !'
    logger.info(test_storage_pool_search_and_paging.__doc__)

    api_path = api_performance_data['case_module']['storage_manager']['storage_pool']['path']['search_storage_pool']
    search_storage_pool_url = api_server + api_path

    param = {"page": 1, "size": 10, "name": "stora"}
    response, take_time = get(request_obj, search_storage_pool_url, header_after_login, param)
    check_search_storage_pool(response, request_obj, search_storage_pool_url, header_after_login, param)
    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=search_storage_pool_table, api=api_path, take_time=take_time, c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert)


@pytest.mark.run(order=3)
@pytest.mark.usefixtures("create_storage_pool_view_detail_table")
def test_storage_pool_view_details(mysql_obj, api_server, header_after_login, db, storage_pool_view_detail_table,
                                   request_obj, api_performance_data, storage_pool_request_data):
    test_storage_pool_view_details.__doc__ = 'Test start, test_storage_pool_view_details test !'
    logger.info(test_storage_pool_view_details.__doc__)

    api_path = api_performance_data['case_module']['storage_manager']['storage_pool']['path'][
        'view_storage_pool_details']
    storage_pool_detail_url = api_server + api_path

    param = {"page": 1, "pageSize": 10, "name": storage_pool_request_data[0]['name']}
    response, take_time = get(request_obj, storage_pool_detail_url, header_after_login, param)
    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=storage_pool_view_detail_table, api=api_path, take_time=take_time, c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert)


@pytest.mark.run(order=4)
@pytest.mark.usefixtures("create_storage_pool_view_handle_detail_table")
def test_storage_pool_view_handle_details(mysql_obj, api_server, header_after_login, db,
                                          storage_pool_view_handle_detail_table,
                                          request_obj, api_performance_data, storage_pool_request_data):
    test_storage_pool_view_handle_details.__doc__ = 'Test start, create_storage_pool_view_handle_details test !'
    logger.info(test_storage_pool_view_handle_details.__doc__)

    api_path = api_performance_data['case_module']['storage_manager']['storage_pool']['path'][
        'view_storage_pool_handle_details']
    storage_pool_handle_detail_url = api_server + api_path
    # kind = storagepool & name = storage - pool - 11 & page = 1 & size = 10
    param = {"page": 1, "size": 10, "name": storage_pool_request_data[0]['name'], "kind": "storagepool"}
    response, take_time = get(request_obj, storage_pool_handle_detail_url, header_after_login, param)
    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=storage_pool_view_handle_detail_table, api=api_path, take_time=take_time,
                c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert)


@pytest.mark.run(order=5)
@pytest.mark.usefixtures("create_storage_pool_name_list_table")
def test_storage_pool_name_list(mysql_obj, api_server, header_after_login, db,
                                storage_pool_name_list_table,
                                request_obj, api_performance_data):
    test_storage_pool_name_list.__doc__ = 'Test start, test_storage_pool_name_list test !'
    logger.info(test_storage_pool_name_list.__doc__)

    api_path = api_performance_data['case_module']['storage_manager']['storage_volume']['path'][
        'get_storage_pool_list']
    storage_pool_list_url = api_server + api_path

    response, take_time = get(request_obj, storage_pool_list_url, header_after_login)
    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=storage_pool_name_list_table, api=api_path, take_time=take_time,
                c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert)


@pytest.mark.run(order=6)
@pytest.mark.usefixtures("create_create_storage_volume_table")
def test_storage_volume_create(mysql_obj, api_server, header_after_login, db,
                               create_storage_volume_table,
                               request_obj, api_performance_data, storage_volume_request_data):
    test_storage_volume_create.__doc__ = 'Test start, test_storage_volume_create test !'
    logger.info(test_storage_volume_create.__doc__)

    api_path = api_performance_data['case_module']['storage_manager']['storage_volume']['path'][
        'create_storage_volume']
    create_storage_volume_url = api_server + api_path

    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for data in storage_volume_request_data:
        futures.append(pool.submit(create, request_obj, data, header_after_login, create_storage_volume_url))
    pool.shutdown()

    for future in as_completed(futures):
        insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                 "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=create_storage_volume_table, api=api_path,
                    take_time=future.result()[1],
                    c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert)

    api_path = api_performance_data['case_module']['storage_manager']['storage_volume']['path']['search_storage_volume']
    get_storage_volume_url = api_server + api_path
    param = {"page": 1, "pageSize": 10}
    create_storage_volume_names = [data["name"] for data in storage_volume_request_data]
    check_all_create_storage_status(request_obj, get_storage_volume_url, header_after_login, param,
                                    create_storage_volume_names)


@pytest.mark.run(order=7)
@pytest.mark.usefixtures("create_search_storage_volume_table")
def test_storage_volume_search_and_paging(mysql_obj, api_server, header_after_login, db, search_storage_volume_table,
                                          request_obj, api_performance_data):
    test_storage_volume_search_and_paging.__doc__ = 'Test start, test_storage_volume_search_and_paging test !'
    logger.info(test_storage_volume_search_and_paging.__doc__)

    api_path = api_performance_data['case_module']['storage_manager']['storage_volume']['path']['search_storage_volume']
    search_storage_volume_url = api_server + api_path

    param = {"page": 1, "pageSize": 10, "searchname": "volum"}
    response, take_time = get(request_obj, search_storage_volume_url, header_after_login, param)
    check_search_storage_volume(response, request_obj, search_storage_volume_url, header_after_login, param)
    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=search_storage_volume_table, api=api_path, take_time=take_time, c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert)


@pytest.mark.run(order=8)
@pytest.mark.usefixtures("create_view_storage_volume_config_table")
def test_storage_volume_view_configure(mysql_obj, api_server, header_after_login, db, view_storage_volume_config_table,
                                       request_obj, api_performance_data, storage_volume_request_data):
    test_storage_volume_view_configure.__doc__ = 'Test start, test_storage_volume_view_configure test !'
    logger.info(test_storage_volume_view_configure.__doc__)

    api_path = api_performance_data['case_module']['storage_manager']['storage_volume']['path']['view_configure']
    view_configure_url = api_server + api_path

    param = {"name": storage_volume_request_data[0]["name"]}
    response, take_time = get(request_obj, view_configure_url, header_after_login, param)

    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=view_storage_volume_config_table, api=api_path, take_time=take_time, c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert)


@pytest.mark.run(order=9)
@pytest.mark.usefixtures("create_view_storage_volume_handle_detail_table")
def test_storage_volume_view_handle_detail(mysql_obj, api_server, header_after_login, db,
                                           view_storage_volume_handle_detail_table,
                                           request_obj, api_performance_data, storage_volume_request_data):
    test_storage_volume_view_handle_detail.__doc__ = 'Test start, test_storage_volume_view_handle_detail test !'
    logger.info(test_storage_volume_view_handle_detail.__doc__)

    api_path = api_performance_data['case_module']['storage_manager']['storage_volume']['path']['view_handle_detail']
    view_handle_detail_url = api_server + api_path

    # kind = persistentvolumeclaim & name = storage - volume - 10 & page = 1 & size = 10
    param = {"kind": "persistentvolumeclaim", "name": storage_volume_request_data[0]["name"]}
    response, take_time = get(request_obj, view_handle_detail_url, header_after_login, param)

    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=view_storage_volume_handle_detail_table, api=api_path, take_time=take_time,
                c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert)


@pytest.mark.run(order=9)
@pytest.mark.usefixtures("create_delete_storage_volume_table")
def test_storage_volume_delete(mysql_obj, api_server, header_after_login, db, delete_storage_volume_table, request_obj,
                               api_performance_data, storage_volume_request_data):
    test_storage_volume_delete.__doc__ = 'Test start, test_storage_volume_delete test !'
    logger.info(test_storage_volume_delete.__doc__)

    api_path = api_performance_data['case_module']['storage_manager']['storage_volume']['path']['delete_storage_volume']
    delete_storage_volume_url = api_server + api_path

    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for data in storage_volume_request_data:
        data1 = data.copy()
        del data1['storagePool']
        del data1['accessMode']
        # data1['isDeleteData'] = random.choice([True, False])
        data1['isDeleteData'] = False
        futures.append(pool.submit(delete, request_obj, delete_storage_volume_url, header_after_login, data1))
    pool.shutdown()

    for future in as_completed(futures):
        insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                 "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=delete_storage_volume_table, api=api_path, take_time=future.result()[1],
                    c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert)


@pytest.mark.run(order=10)
@pytest.mark.usefixtures("create_delete_storage_pool_table")
def test_storage_pool_delete(mysql_obj, api_server, header_after_login, db, delete_storage_pool_table, request_obj,
                             api_performance_data, storage_pool_request_data):
    test_storage_pool_delete.__doc__ = 'Test start, test_storage_pool_delete test !'
    logger.info(test_storage_pool_delete.__doc__)
    api_path = api_performance_data['case_module']['storage_manager']['storage_pool']['path']['delete_storage_pool']

    delete_storage_pool_url = api_server + api_path

    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for data in storage_pool_request_data:
        data1 = data.copy()
        del data1['provisioner']
        del data1['parameters']
        if 'total' in data1:
            del data1['total']
        if 'workerName' in data1:
            del data1['workerName']
        futures.append(pool.submit(delete, request_obj, delete_storage_pool_url, header_after_login, data1))
    pool.shutdown()

    for future in as_completed(futures):
        insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                 "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=delete_storage_pool_table, api=api_path, take_time=future.result()[1],
                    c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert)
