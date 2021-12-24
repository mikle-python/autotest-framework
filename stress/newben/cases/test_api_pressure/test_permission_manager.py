import random

import pytest
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

from libs.log_obj import LogObj
from stress.newben.common.common import get, create, update, delete
from stress.newben.common.permission_module_checks import check_role_mapping, check_type_corresponding_permission, \
    check_search_role, check_search_authorization

logger = LogObj().get_logger()


@pytest.fixture(scope='session')
def role_mapping_table():
    return 'role_mapping'


@pytest.fixture(scope='session')
def type_corresponding_permission_table():
    return 'type_corresponding_permission'


@pytest.fixture(scope='session')
def user_and_roles_table():
    return 'user_and_roles'


@pytest.fixture(scope='session')
def create_role_table():
    return 'create_role'


@pytest.fixture(scope='session')
def search_role_table():
    return 'search_role'


@pytest.fixture(scope='session')
def update_role_table():
    return 'update_role'


@pytest.fixture(scope='session')
def delete_role_table():
    return 'delete_role'


@pytest.fixture(scope='session')
def create_authorization_table():
    return 'create_authorization'


@pytest.fixture(scope='session')
def search_authorization_table():
    return 'search_authorization'


@pytest.fixture(scope='session')
def update_authorization_table():
    return 'update_authorization'


@pytest.fixture(scope='session')
def delete_authorization_table():
    return 'delete_authorization'


@pytest.fixture(scope='session')
def create_role_mapping_table(mysql_obj, db, role_mapping_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, role_mapping_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_type_corresponding_permission(mysql_obj, db, type_corresponding_permission_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, type_corresponding_permission_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_user_and_roles_table(mysql_obj, db, user_and_roles_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, user_and_roles_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_create_role_table(mysql_obj, db, create_role_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, create_role_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_search_role_table(mysql_obj, db, search_role_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, search_role_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_update_role_table(mysql_obj, db, update_role_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, update_role_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_delete_role_table(mysql_obj, db, delete_role_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, delete_role_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_create_authorization_table(mysql_obj, db, create_authorization_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, create_authorization_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_search_authorization_table(mysql_obj, db, search_authorization_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, search_authorization_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_update_authorization_table(mysql_obj, db, update_authorization_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, update_authorization_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_delete_authorization_table(mysql_obj, db, delete_authorization_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, delete_authorization_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def role_request_data(api_performance_data):
    request_datas = []
    for i in range(api_performance_data['common']['data_quantity']):
        data = api_performance_data['case_module']['permission_manager']['role']['default_create_role_data'].copy()
        type_permission_dict = api_performance_data['case_module']['permission_manager']['role']['type_permission_data']
        data['name'] = "{}-{}".format('role', i)
        data['type'] = random.choice(list(type_permission_dict.keys()))
        if data['type'] == 'workspace':
            data['workspace'] = 'system'
            data['items'] = random.sample(type_permission_dict['workspace'],
                                          random.randint(0, len(type_permission_dict['workspace'])))
        else:
            data['items'] = random.sample(type_permission_dict['whole'],
                                          random.randint(0, len(type_permission_dict['whole'])))
        request_datas.append(data)
    return request_datas


@pytest.fixture(scope='session')
def authorization_request_data(api_performance_data):
    request_datas = []
    for i in range(api_performance_data['common']['data_quantity']):
        data = api_performance_data['case_module']['permission_manager']['authorization'][
            'default_create_authorization_data'].copy()
        scope = api_performance_data['case_module']['permission_manager']['authorization']['authorize_scope']
        data['name'] = "{}-{}".format('authorization', i)
        data['type'] = random.choice(scope)
        if data['type'] == 'workspace':
            data['workspace'] = 'system'
            data['roles']['role'] = ['cc']
        request_datas.append(data)
    return request_datas


@pytest.mark.usefixtures("create_role_mapping_table")
def test_super_role_mapping_auth(mysql_obj, api_server, header_after_login, db, role_mapping_table, request_obj,
                                 api_performance_data):
    test_super_role_mapping_auth.__doc__ = 'Test start, test_super_role_mapping_auth test !'
    logger.info(test_super_role_mapping_auth.__doc__)
    api_path = api_performance_data['case_module']['permission_manager']['role']['path']['super_role_mapping']

    super_role_mapping_url = api_server + api_path

    response, take_time = get(request_obj, super_role_mapping_url, header_after_login)
    check_role_mapping(response)
    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=role_mapping_table, api=api_path, take_time=take_time, c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert)


@pytest.mark.usefixtures("create_type_corresponding_permission")
def test_type_corresponding_permission(mysql_obj, api_server, header_after_login, db,
                                       type_corresponding_permission_table, request_obj, api_performance_data):
    test_type_corresponding_permission.__doc__ = 'Test start, test_type_corresponding_permission test !'
    logger.info(test_type_corresponding_permission.__doc__)
    api_path = api_performance_data['case_module']['permission_manager']['role']['path']['type_permission']

    type_permission_url = api_server + api_path
    response, take_time = get(request_obj, type_permission_url, header_after_login, param={"type": "whole"})
    check_type_corresponding_permission(response)
    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=type_corresponding_permission_table, api=api_path, take_time=take_time,
                c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert)

    response, take_time = get(request_obj, type_permission_url, header_after_login,
                              param={"type": "workspace"})
    check_type_corresponding_permission(response)
    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=type_corresponding_permission_table, api=api_path, take_time=take_time,
                c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert)


@pytest.mark.usefixtures("create_user_and_roles_table")
def test_user_and_roles(mysql_obj, api_server, header_after_login, db,
                        user_and_roles_table, request_obj, api_performance_data):
    test_user_and_roles.__doc__ = 'Test start, test_user_and_roles test !'
    logger.info(test_user_and_roles.__doc__)
    api_path = api_performance_data['case_module']['permission_manager']['authorization']['path']['user_and_roles']

    user_and_roles_url = api_server + api_path
    _, take_time = get(request_obj, user_and_roles_url, header_after_login, param={"type": "whole"})
    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=user_and_roles_table, api=api_path, take_time=take_time, c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert)
    response, take_time = get(request_obj, user_and_roles_url, header_after_login,
                              param={"workspace": "system", "type": "workspace"})
    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=user_and_roles_table, api=api_path, take_time=take_time, c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert)


@pytest.mark.run(order=1)
@pytest.mark.usefixtures("create_create_role_table")
def test_role_create(mysql_obj, api_server, header_after_login, db, create_role_table, request_obj,
                     api_performance_data, role_request_data):
    test_role_create.__doc__ = 'Test start, test_role_create test !'
    logger.info(test_role_create.__doc__)
    api_path = api_performance_data['case_module']['permission_manager']['role']['path']['create_role']

    create_role_url = api_server + api_path

    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for data in role_request_data:
        futures.append(pool.submit(create, request_obj, data, header_after_login, create_role_url))
    pool.shutdown()

    for future in as_completed(futures):
        insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                 "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=create_role_table, api=api_path, take_time=future.result()[1], c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert)


@pytest.mark.run(order=2)
@pytest.mark.usefixtures("create_search_role_table")
def test_role_search_and_paging(mysql_obj, api_server, header_after_login, db, search_role_table, request_obj,
                                api_performance_data, role_request_data):
    test_role_search_and_paging.__doc__ = 'Test start, test_role_search_and_paging test !'
    logger.info(test_role_search_and_paging.__doc__)
    api_path = api_performance_data['case_module']['permission_manager']['role']['path']['search_role']

    search_role_url = api_server + api_path
    param = {"page": 1, "size": 10, "searchname": "ro"}
    response, take_time = get(request_obj, search_role_url, header_after_login, param)
    check_search_role(response, request_obj, search_role_url, header_after_login, param)
    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=search_role_table, api=api_path, take_time=take_time, c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert)


@pytest.mark.run(order=3)
@pytest.mark.usefixtures("create_update_role_table")
def test_role_update(mysql_obj, api_server, header_after_login, db, update_role_table, request_obj,
                     api_performance_data, role_request_data):
    test_role_update.__doc__ = 'Test start, test_role_update test !'
    logger.info(test_role_update.__doc__)
    api_path = api_performance_data['case_module']['permission_manager']['role']['path']['update_role']

    update_role_url = api_server + api_path

    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for data in role_request_data:
        data1 = data.copy()
        data1['comment'] = '修改角色'
        type_permission_dict = api_performance_data['case_module']['permission_manager']['role']['type_permission_data']
        if data1.get('workspace'):
            data1['items'] = random.sample(type_permission_dict['workspace'],
                                           random.randint(0, len(type_permission_dict['workspace'])))
        else:
            data1['items'] = random.sample(type_permission_dict['whole'],
                                           random.randint(0, len(type_permission_dict['whole'])))
        futures.append(pool.submit(update, request_obj, data1, header_after_login, update_role_url))
    pool.shutdown()

    for future in as_completed(futures):
        insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                 "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=update_role_table, api=api_path, take_time=future.result()[1], c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert)


@pytest.mark.run(order=4)
@pytest.mark.usefixtures("create_delete_role_table")
def test_role_delete(mysql_obj, api_server, header_after_login, db, delete_role_table, request_obj,
                     api_performance_data, role_request_data):
    test_role_delete.__doc__ = 'Test start, test_role_delete test !'
    logger.info(test_role_delete.__doc__)
    api_path = api_performance_data['case_module']['permission_manager']['role']['path']['delete_role']

    delete_role_url = api_server + api_path

    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for data in role_request_data:
        data1 = data.copy()
        del data1['items']
        del data1['comment']
        if 'workspace' in data1:
            del data1['workspace']
        futures.append(pool.submit(delete, request_obj, delete_role_url, header_after_login, data1))
    pool.shutdown()

    for future in as_completed(futures):
        insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                 "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=delete_role_table, api=api_path, take_time=future.result()[1], c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert)


@pytest.mark.run(order=5)
@pytest.mark.usefixtures("create_create_authorization_table")
def test_authorization_create(mysql_obj, api_server, header_after_login, db, create_authorization_table, request_obj,
                              api_performance_data, authorization_request_data):
    test_authorization_create.__doc__ = 'Test start, test_authorization_create test !'
    logger.info(test_authorization_create.__doc__)
    api_path = api_performance_data['case_module']['permission_manager']['authorization']['path'][
        'create_authorization']

    create_authorization_url = api_server + api_path

    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for data in authorization_request_data:
        logger.debug(data)
        futures.append(pool.submit(create, request_obj, data, header_after_login, create_authorization_url))
    pool.shutdown()

    for future in as_completed(futures):
        insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                 "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=create_authorization_table, api=api_path, take_time=future.result()[1],
                    c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert)


@pytest.mark.run(order=6)
@pytest.mark.usefixtures("create_search_authorization_table")
def test_authorization_search_and_paging(mysql_obj, api_server, header_after_login, db, search_authorization_table,
                                         request_obj, api_performance_data, authorization_request_data):
    test_authorization_search_and_paging.__doc__ = 'Test start, test_authorization_search_and_paging test !'
    logger.info(test_authorization_search_and_paging.__doc__)
    api_path = api_performance_data['case_module']['permission_manager']['authorization']['path'][
        'search_authorization']

    search_authorization_url = api_server + api_path
    param = {"page": 1, "size": 10, "searchname": "auth"}
    response, take_time = get(request_obj, search_authorization_url, header_after_login, param)
    check_search_authorization(response, request_obj, search_authorization_url, header_after_login, param)
    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=search_authorization_table, api=api_path, take_time=take_time, c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert)


@pytest.mark.run(order=7)
@pytest.mark.usefixtures("create_update_authorization_table")
def test_authorization_update(mysql_obj, api_server, header_after_login, db, update_authorization_table, request_obj,
                              api_performance_data, authorization_request_data):
    test_authorization_update.__doc__ = 'Test start, test_authorization_update test !'
    logger.info(test_authorization_update.__doc__)
    api_path = api_performance_data['case_module']['permission_manager']['authorization']['path'][
        'update_authorization']

    update_authorization_url = api_server + api_path

    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for data in authorization_request_data:
        data1 = data.copy()
        data1['comment'] = '修改授权'
        data1['objects'] = {"user": ["aa", "aaa"]}
        if data1.get('workspace'):
            data1['roles'] = {"superRole": ["bb", "bbb"], "role": ["cc", "ccc"]}
        else:
            data1['roles'] = {"superRole": ["bb", "bbb"]}
        futures.append(
            pool.submit(update, request_obj, data1, header_after_login, update_authorization_url))
    pool.shutdown()

    for future in as_completed(futures):
        insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                 "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=update_authorization_table, api=api_path, take_time=future.result()[1],
                    c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert)


@pytest.mark.run(order=8)
@pytest.mark.usefixtures("create_delete_authorization_table")
def test_authorization_delete(mysql_obj, api_server, header_after_login, db, delete_authorization_table, request_obj,
                              api_performance_data, authorization_request_data):
    test_authorization_delete.__doc__ = 'Test start, test_authorization_delete test !'
    logger.info(test_authorization_delete.__doc__)
    api_path = api_performance_data['case_module']['permission_manager']['authorization']['path'][
        'delete_authorization']

    delete_authorization_url = api_server + api_path

    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for data in authorization_request_data:
        data1 = data.copy()
        del data1['comment']
        del data1['objects']
        del data1['roles']
        if 'workspace' in data1:
            del data1['workspace']
        futures.append(
            pool.submit(delete, request_obj, delete_authorization_url, header_after_login, data1))
    pool.shutdown()

    for future in as_completed(futures):
        insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                 "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=delete_authorization_table, api=api_path, take_time=future.result()[1],
                    c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert)
