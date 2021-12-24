import copy
import random
import pytest
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.util import time_str
from utils.times import sleep
from stress.newben.common.common import create_api, list_api, delete_api, update_api, is_app_running, api_table_create,\
    is_forward_set_success, is_app_not_exist, is_appmatrix_running, is_application_not_exist, is_forward_not_exist, \
    is_mission_running, check_cronmission_status, is_cronmission_not_exist, is_apparafile_exist, check_data
from libs.log_obj import LogObj
from utils.util import generate_random_string


logger = LogObj().get_logger()


@pytest.fixture(scope='session')
def application_create_table():
    return 'application_create'


@pytest.fixture(scope='session')
def create_application_create_table(mysql_obj, db, application_create_table):
    api_table_create(mysql_obj, db, application_create_table)


@pytest.fixture(scope='session')
def application_list_table():
    return 'application_list'


@pytest.fixture(scope='session')
def create_application_list_table(mysql_obj, db, application_list_table):
    api_table_create(mysql_obj, db, application_list_table)


@pytest.fixture(scope='session')
def application_detail_table():
    return 'application_detail'


@pytest.fixture(scope='session')
def create_application_detail_table(mysql_obj, db, application_detail_table):
    api_table_create(mysql_obj, db, application_detail_table)


@pytest.fixture(scope='session')
def application_event_table():
    return 'application_event'


@pytest.fixture(scope='session')
def create_application_event_table(mysql_obj, db, application_event_table):
    api_table_create(mysql_obj, db, application_event_table)


@pytest.fixture(scope='session')
def application_redeploy_table():
    return 'application_redeploy'


@pytest.fixture(scope='session')
def create_application_redeploy_table(mysql_obj, db, application_redeploy_table):
    api_table_create(mysql_obj, db, application_redeploy_table)


@pytest.fixture(scope='session')
def application_update_table():
    return 'application_update'


@pytest.fixture(scope='session')
def create_application_update_table(mysql_obj, db, application_update_table):
    api_table_create(mysql_obj, db, application_update_table)


@pytest.fixture(scope='session')
def application_expose_create_table():
    return 'application_expose_create'


@pytest.fixture(scope='session')
def create_application_expose_create_table(mysql_obj, db, application_expose_create_table):
    api_table_create(mysql_obj, db, application_expose_create_table)


@pytest.fixture(scope='session')
def application_expose_delete_table():
    return 'application_expose_delete'


@pytest.fixture(scope='session')
def create_application_expose_delete_table(mysql_obj, db, application_expose_delete_table):
    api_table_create(mysql_obj, db, application_expose_delete_table)


@pytest.fixture(scope='session')
def application_delete_table():
    return 'application_delete'


@pytest.fixture(scope='session')
def create_application_delete_table(mysql_obj, db, application_delete_table):
    api_table_create(mysql_obj, db, application_delete_table)


@pytest.fixture(scope='session')
def appmatrix_create_table():
    return 'appmatrix_create'


@pytest.fixture(scope='session')
def create_appmatrix_create_table(mysql_obj, db, appmatrix_create_table):
    api_table_create(mysql_obj, db, appmatrix_create_table)


@pytest.fixture(scope='session')
def appmatrix_delete_table():
    return 'appmatrix_delete'


@pytest.fixture(scope='session')
def create_appmatrix_delete_table(mysql_obj, db, appmatrix_delete_table):
    api_table_create(mysql_obj, db, appmatrix_delete_table)


@pytest.fixture(scope='session')
def appmatrix_list_table():
    return 'appmatrix_list'


@pytest.fixture(scope='session')
def create_appmatrix_list_table(mysql_obj, db, appmatrix_list_table):
    api_table_create(mysql_obj, db, appmatrix_list_table)


@pytest.fixture(scope='session')
def appmatrix_detail_table():
    return 'appmatrix_detail'


@pytest.fixture(scope='session')
def create_appmatrix_detail_table(mysql_obj, db, appmatrix_detail_table):
    api_table_create(mysql_obj, db, appmatrix_detail_table)


@pytest.fixture(scope='session')
def appmatrix_event_table():
    return 'appmatrix_event'


@pytest.fixture(scope='session')
def create_appmatrix_event_table(mysql_obj, db, appmatrix_event_table):
    api_table_create(mysql_obj, db, appmatrix_event_table)


@pytest.fixture(scope='session')
def appmatrix_update_table():
    return 'appmatrix_update'


@pytest.fixture(scope='session')
def create_appmatrix_update_table(mysql_obj, db, appmatrix_update_table):
    api_table_create(mysql_obj, db, appmatrix_update_table)


@pytest.fixture(scope='session')
def mission_create_table():
    return "mission_create"


@pytest.fixture(scope='session')
def create_mission_create_table(mysql_obj, db, mission_create_table):
    api_table_create(mysql_obj, db, mission_create_table)


@pytest.fixture(scope='session')
def mission_delete_table():
    return "mission_delete"


@pytest.fixture(scope='session')
def create_mission_delete_table(mysql_obj, db, mission_delete_table):
    api_table_create(mysql_obj, db, mission_delete_table)


@pytest.fixture(scope='session')
def mission_list_table():
    return "mission_list"


@pytest.fixture(scope='session')
def create_mission_list_table(mysql_obj, db, mission_list_table):
    api_table_create(mysql_obj, db, mission_list_table)


@pytest.fixture(scope='session')
def mission_event_table():
    return "mission_event"


@pytest.fixture(scope='session')
def create_mission_event_table(mysql_obj, db, mission_event_table):
    api_table_create(mysql_obj, db, mission_event_table)


@pytest.fixture(scope='session')
def cronmission_create_table():
    return "cronmission_create"


@pytest.fixture(scope='session')
def create_cronmission_create_table(mysql_obj, db, cronmission_create_table):
    api_table_create(mysql_obj, db, cronmission_create_table)


@pytest.fixture(scope='session')
def cronmission_delete_table():
    return "cronmission_delete"


@pytest.fixture(scope='session')
def create_cronmission_delete_table(mysql_obj, db, cronmission_delete_table):
    api_table_create(mysql_obj, db, cronmission_delete_table)


@pytest.fixture(scope='session')
def cronmission_list_table():
    return "cronmission_list"


@pytest.fixture(scope='session')
def create_cronmission_list_table(mysql_obj, db, cronmission_list_table):
    api_table_create(mysql_obj, db, cronmission_list_table)


@pytest.fixture(scope='session')
def cronmission_event_table():
    return "cronmission_event"


@pytest.fixture(scope='session')
def create_cronmission_event_table(mysql_obj, db, cronmission_event_table):
    api_table_create(mysql_obj, db, cronmission_event_table)


@pytest.fixture(scope='session')
def cronmission_update_table():
    return "cronmission_update"


@pytest.fixture(scope='session')
def create_cronmission_update_table(mysql_obj, db, cronmission_update_table):
    api_table_create(mysql_obj, db, cronmission_update_table)


@pytest.fixture(scope='session')
def cronmission_suspend_table():
    return "cronmission_suspend"


@pytest.fixture(scope='session')
def create_cronmission_suspend_table(mysql_obj, db, cronmission_suspend_table):
    api_table_create(mysql_obj, db, cronmission_suspend_table)


@pytest.fixture(scope='session')
def cronmission_suspend_cancel_table():
    return "cronmission_suspend_cancel"


@pytest.fixture(scope='session')
def create_cronmission_suspend_cancel_table(mysql_obj, db, cronmission_suspend_cancel_table):
    api_table_create(mysql_obj, db, cronmission_suspend_cancel_table)


@pytest.fixture(scope='session')
def apparafile_create_table():
    return "apparafile_create"


@pytest.fixture(scope='session')
def create_apparafile_create_table(mysql_obj, db, apparafile_create_table):
    api_table_create(mysql_obj, db, apparafile_create_table)


@pytest.fixture(scope='session')
def apparafile_delete_table():
    return "apparafile_delete"


@pytest.fixture(scope='session')
def create_apparafile_delete_table(mysql_obj, db, apparafile_delete_table):
    api_table_create(mysql_obj, db, apparafile_delete_table)


@pytest.fixture(scope='session')
def apparafile_list_table():
    return "apparafile_list"


@pytest.fixture(scope='session')
def create_apparafile_list_table(mysql_obj, db, apparafile_list_table):
    api_table_create(mysql_obj, db, apparafile_list_table)


@pytest.fixture(scope='session')
def apparafile_update_table():
    return "apparafile_update"


@pytest.fixture(scope='session')
def create_apparafile_update_table(mysql_obj, db, apparafile_update_table):
    api_table_create(mysql_obj, db, apparafile_update_table)


@pytest.fixture(scope='session')
def applications_data(api_performance_data):
    applications_data = []
    date_tag = time_str()
    for i in range(api_performance_data['common']['data_quantity']):
        data = api_performance_data['case_module']['app_manager']['my_app']['default_create_app_data'].copy()
        data['applicationName'] = "{}-{}-{}".format("kwang", date_tag, i)
        data['containerName'] = "{}-{}-{}".format("kwang", date_tag, i)
        data['image'] = api_performance_data['common']['image']
        data['imageTag'] = api_performance_data['common']['image_tag']
        data['imagePullPolicy'] = random.choice(data['imagePullPolicy'])
        applications_data.append(data)
    return applications_data


@pytest.fixture(scope='session')
def appmatrixes_data(api_performance_data):
    appmatrixes_data = []
    date_tag = time_str()

    for i in range(api_performance_data['common']['data_quantity']):
        data = api_performance_data['case_module']['app_manager']['appmatrix']['default_appmatrix_data'].copy()
        data['appMatrixName'] = "{}-{}-{}".format("autotest", date_tag, i)

        topology = []
        application_list = []
        for app in range(api_performance_data['case_module']['app_manager']['appmatrix']['app_quantity']):
            topology.append({"name": "{}-{}-{}-{}".format("kwang", date_tag, i, app), "order": app})
            application_new = data['applicationList'][0].copy()
            application_new['id'] = generate_random_string(6, 6)
            application_new['order'] = app
            application_new['applicationName'] = "{}-{}-{}-{}".format("kwang", date_tag, i, app)
            application_new['containerName'] = "{}-{}-{}-{}".format("kwang", date_tag, i, app)
            application_new['image'] = api_performance_data['common']['image']
            application_new['imageTag'] = api_performance_data['common']['image_tag']
            application_new['imagePullPolicy'] = random.choice(application_new['imagePullPolicy'])
            application_list.append(application_new)

        data['topology'] = topology
        data['applicationList'] = application_list
        appmatrixes_data.append(data)
    return appmatrixes_data


@pytest.fixture(scope='session')
def missions_data(api_performance_data):
    missions_data = []
    date_tag = time_str()

    for i in range(api_performance_data['common']['data_quantity']):
        data = api_performance_data['case_module']['app_manager']['mission']['default_mission_data'].copy()
        data['name'] = "{}-{}-{}".format("kwang", date_tag, i)
        data['image'] = api_performance_data['common']['image']
        data['imageTag'] = api_performance_data['common']['image_tag']
        data['imagePullPolicy'] = random.choice(data['imagePullPolicy'])
        missions_data.append(data)

    return missions_data


@pytest.fixture(scope='session')
def cronmissions_data(api_performance_data):
    cronmissions_data = []
    date_tag = time_str()

    for i in range(api_performance_data['common']['data_quantity']):
        data = copy.deepcopy(api_performance_data['case_module']['app_manager']['cronmission']
                             ['default_cronmission_data'])
        data['cronMissionName'] = "{}-{}-{}".format("kwang", date_tag, i)
        data['image'] = api_performance_data['common']['image']
        data['imageTag'] = api_performance_data['common']['image_tag']
        data['imagePullPolicy'] = random.choice(data['imagePullPolicy'])
        data['concurrencyPolicy'] = random.choice(data['concurrencyPolicy'])
        cronmissions_data.append(data)

    return cronmissions_data


@pytest.fixture(scope='session')
def apparafiles_data(api_performance_data):
    apparafiles_data = []
    date_tag = time_str()

    for i in range(api_performance_data['common']['data_quantity']):
        data = copy.deepcopy(api_performance_data['case_module']['app_manager']['apparafile']
                             ['default_apparafile_data'])
        data['name'] = "{}-{}-{}".format("kwang", date_tag, i)
        for env in range(api_performance_data['case_module']['app_manager']['apparafile']['environment_quantity']):
            data_tag = "{}-{}-{}".format("kwang", date_tag, env)
            data['data'][data_tag] = data_tag

        apparafiles_data.append(data)

    return apparafiles_data


@pytest.mark.usefixtures("create_application_create_table")
def test_api_application_create(mysql_obj, api_server, header_after_login, db, application_create_table, request_obj,
                                api_performance_data, applications_data):
    test_api_application_create.__doc__ = 'Test start, test_api_application_create test !'
    logger.info(test_api_application_create.__doc__)
    api_path = api_performance_data['case_module']['app_manager']['my_app']['path']['create_application']

    create_app_url = api_server + api_path
    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for application in applications_data:
        futures.append(pool.submit(create_api, request_obj, application, header_after_login, create_app_url))
    pool.shutdown()

    for future in as_completed(futures):
        insert_create_api = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                            "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=application_create_table, api=api_path, take_time=future.result(),
                    c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert_create_api)

    api_path = api_performance_data['case_module']['app_manager']['my_app']['path']['application_detail']
    detail_url = api_server + api_path
    pool_check = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures_check = []
    for application in applications_data:
        futures_check.append(pool_check.submit(is_app_running, request_obj, application['applicationName'],
                                               header_after_login, detail_url))
    pool_check.shutdown()
    for future in as_completed(futures_check):
        future.result()


@pytest.mark.usefixtures("create_application_list_table")
def test_api_application_list(mysql_obj, api_server, header_after_login, db, application_list_table, request_obj,
                              api_performance_data):
    test_api_application_list.__doc__ = 'Test start, test_api_application_list test !'
    logger.info(test_api_application_list.__doc__)
    api_path = api_performance_data['case_module']['app_manager']['my_app']['path']['get_application']
    list_application_url = api_server + api_path

    take_time = list_api(request_obj, header_after_login, list_application_url)
    insert_list_api = "INSERT INTO {db}.{table} (api, take_time, c_time) VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=application_list_table, api=api_path, take_time=take_time, c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert_list_api)


@pytest.mark.usefixtures("create_application_detail_table")
def test_api_application_detail(mysql_obj, api_server, header_after_login, db, application_detail_table, request_obj,
                                api_performance_data, applications_data):
    test_api_application_detail.__doc__ = 'Test start, test_api_application_detail test !'
    logger.info(test_api_application_detail.__doc__)
    api_path = api_performance_data['case_module']['app_manager']['my_app']['path']['application_detail']

    detail_url = api_server + api_path
    detail_data = {
        "applicationName": random.choice(applications_data)['applicationName']
    }
    take_time = create_api(request_obj, detail_data, header_after_login, detail_url)
    insert_list_api = "INSERT INTO {db}.{table} (api, take_time, c_time) VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=application_detail_table, api=api_path, take_time=take_time, c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert_list_api)


@pytest.mark.usefixtures("create_application_event_table")
def test_api_application_event(mysql_obj, api_server, header_after_login, db, application_event_table, request_obj,
                               api_performance_data, applications_data):
    test_api_application_event.__doc__ = 'Test start, test_api_application_event test !'
    logger.info(test_api_application_event.__doc__)
    api_path = api_performance_data['case_module']['app_manager']['my_app']['path']['application_event']

    event_url = api_server + api_path
    event_url = event_url.replace("app_name", random.choice(applications_data)['applicationName'])

    take_time = list_api(request_obj, header_after_login, event_url)
    insert_list_api = "INSERT INTO {db}.{table} (api, take_time, c_time) VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=application_event_table, api=api_path, take_time=take_time, c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert_list_api)


@pytest.mark.usefixtures("create_application_update_table")
def test_api_application_update(mysql_obj, api_server, header_after_login, db, application_update_table, request_obj,
                                api_performance_data, applications_data):
    test_api_application_update.__doc__ = 'Test start, test_api_application_update test !'
    logger.info(test_api_application_update.__doc__)
    api_path = api_performance_data['case_module']['app_manager']['my_app']['path']['update_application']

    update_app_url = api_server + api_path

    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for application in applications_data:
        data = api_performance_data['case_module']['app_manager']['my_app']['default_create_app_data'].copy()
        application['imagePullPolicy'] = random.choice(data['imagePullPolicy'])
        application['containerName'] = "{}-{}".format("autotest", time_str())
        futures.append(pool.submit(update_api, request_obj, application, header_after_login, update_app_url))
    pool.shutdown()

    for future in as_completed(futures):
        insert_update_api = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                            "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=application_update_table, api=api_path, take_time=future.result(), c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert_update_api)

    sleep(api_performance_data['common']['wait_time'])

    api_path = api_performance_data['case_module']['app_manager']['my_app']['path']['application_detail']
    detail_url = api_server + api_path
    pool_check = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures_check = []
    for application in applications_data:
        futures_check.append(pool_check.submit(is_app_running, request_obj, application['applicationName'],
                                               header_after_login, detail_url))
    pool_check.shutdown()
    for future in as_completed(futures_check):
        future.result()


@pytest.mark.usefixtures("create_application_expose_create_table")
def test_api_application_expose_create(mysql_obj, api_server, header_after_login, db, application_expose_create_table,
                                       request_obj, api_performance_data, applications_data):
    test_api_application_expose_create.__doc__ = 'Test start, test_api_application_expose_create test !'
    logger.info(test_api_application_expose_create.__doc__)
    api_path = api_performance_data['case_module']['app_manager']['my_app']['path']['expose_application']

    expose_app_url = api_server + api_path
    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    port = api_performance_data['case_module']['app_manager']['my_app'].copy()['port']
    for application in applications_data:
        port += 1
        expose_app = {
            "name": application['applicationName'],
            "type": "hub",
            "rules": [
                {
                    "exposePort": port,
                    "boxPort": 80,
                    "protocol": "TCP"
                }
            ]
            }
        futures.append(pool.submit(create_api, request_obj, expose_app, header_after_login, expose_app_url))
    pool.shutdown()
    for future in as_completed(futures):
        insert_create_api = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                            "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=application_expose_create_table, api=api_path, take_time=future.result(),
                    c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert_create_api)

    api_path = api_performance_data['case_module']['app_manager']['my_app']['path']['application_detail']
    detail_url = api_server + api_path
    pool_check = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures_check = []
    for application in applications_data:
        futures_check.append(pool_check.submit(is_forward_set_success, request_obj, application['applicationName'],
                                               header_after_login, detail_url))
    pool_check.shutdown()
    for future in as_completed(futures_check):
        future.result()


@pytest.mark.usefixtures("create_application_expose_delete_table")
def test_api_application_expose_delete(mysql_obj, api_server, header_after_login, db, application_expose_delete_table,
                                       request_obj, api_performance_data, applications_data):
    test_api_application_expose_delete.__doc__ = 'Test start, test_api_application_expose_delete test !'
    logger.info(test_api_application_expose_delete.__doc__)
    api_path = api_performance_data['case_module']['app_manager']['my_app']['path']['delete_expose_application']

    del_expose_app_url = api_server + api_path
    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for application in applications_data:
        futures.append(pool.submit(delete_api, request_obj, header_after_login, del_expose_app_url,
                                   {"name": application['applicationName']}))
    pool.shutdown()
    for future in as_completed(futures):
        insert_del_api = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                            "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=application_expose_delete_table, api=api_path, take_time=future.result(),
                    c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert_del_api)

    api_path = api_performance_data['case_module']['app_manager']['my_app']['path']['application_detail']
    detail_url = api_server + api_path
    pool_check = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures_check = []
    for application in applications_data:
        futures_check.append(pool_check.submit(is_forward_not_exist, request_obj, application['applicationName'],
                                               header_after_login, detail_url))
    pool_check.shutdown()
    for future in as_completed(futures_check):
        future.result()


@pytest.mark.usefixtures("create_application_redeploy_table")
def test_api_application_redeploy(mysql_obj, api_server, header_after_login, request_obj, api_performance_data,
                                  applications_data, application_redeploy_table, db):
    test_api_application_redeploy.__doc__ = 'Test start, test_api_application_redeploy test !'
    logger.info(test_api_application_redeploy.__doc__)
    api_path = api_performance_data['case_module']['app_manager']['my_app']['path']['redeploy']

    redeploy_app_url = api_server + api_path

    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for application in applications_data:
        futures.append(pool.submit(create_api, request_obj, {"applicationName": application['applicationName']},
                                   header_after_login, redeploy_app_url,))
    pool.shutdown()
    for future in as_completed(futures):
        insert_rd_api = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                         "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=application_redeploy_table, api=api_path, take_time=future.result(),
                    c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert_rd_api)

    sleep(api_performance_data['common']['wait_time'])

    api_path = api_performance_data['case_module']['app_manager']['my_app']['path']['application_detail']
    detail_url = api_server + api_path
    pool_check = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures_check = []
    for application in applications_data:
        futures_check.append(pool_check.submit(is_app_running, request_obj, application['applicationName'],
                                               header_after_login, detail_url))
    pool_check.shutdown()
    for future in as_completed(futures_check):
        future.result()


@pytest.mark.usefixtures("create_application_delete_table")
def test_api_application_delete(mysql_obj, api_server, header_after_login, db, application_delete_table, request_obj,
                                api_performance_data, applications_data):
    test_api_application_delete.__doc__ = 'Test start, test_api_application_delete test !'
    logger.info(test_api_application_delete.__doc__)
    api_path = api_performance_data['case_module']['app_manager']['my_app']['path']['delete_application']

    delete_app_url = api_server + api_path

    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for application in applications_data:
        futures.append(pool.submit(delete_api, request_obj, header_after_login, delete_app_url,
                                   {"applicationName": application['applicationName']}))
    pool.shutdown()

    for future in as_completed(futures):
        insert_delete_api = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                            "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=application_delete_table, api=api_path, take_time=future.result(),
                    c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert_delete_api)

    api_path = api_performance_data['case_module']['app_manager']['my_app']['path']['application_detail']
    detail_url = api_server + api_path
    pool_check = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures_check = []
    for application in applications_data:
        futures_check.append(pool_check.submit(is_app_not_exist, request_obj, application['applicationName'],
                                               header_after_login, detail_url))
    pool_check.shutdown()
    for future in as_completed(futures_check):
        future.result()


@pytest.mark.usefixtures("create_appmatrix_create_table")
def test_api_appmatrix_create(mysql_obj, api_server, header_after_login, db, appmatrix_create_table, request_obj,
                              api_performance_data, appmatrixes_data):
    test_api_appmatrix_create.__doc__ = 'Test start, test_api_appmatrix_create test !'
    logger.info(test_api_appmatrix_create.__doc__)
    api_path = api_performance_data['case_module']['app_manager']['appmatrix']['path']['create_appmatrix']

    create_appmatrix_url = api_server + api_path
    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for appmatrix in appmatrixes_data:
        futures.append(pool.submit(create_api, request_obj, appmatrix, header_after_login, create_appmatrix_url))
    pool.shutdown()

    for future in as_completed(futures):
        insert_create_api = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                            "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=appmatrix_create_table, api=api_path, take_time=future.result(), c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert_create_api)

    api_path = api_performance_data['case_module']['app_manager']['appmatrix']['path']['appmatrix_detail']
    detail_url = api_server + api_path
    pool_check = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures_check = []
    for appmatrix in appmatrixes_data:
        futures_check.append(pool_check.submit(is_appmatrix_running, request_obj, appmatrix['appMatrixName'],
                                               header_after_login, detail_url.replace("appmatrix_name",
                                                                                      appmatrix['appMatrixName'])))
    pool_check.shutdown()
    for future in as_completed(futures_check):
        future.result()


@pytest.mark.usefixtures("create_appmatrix_list_table")
def test_api_appmatrix_list(mysql_obj, api_server, header_after_login, db, appmatrix_list_table, request_obj,
                            api_performance_data):
    test_api_appmatrix_list.__doc__ = 'Test start, test_api_appmatrix_list test !'
    logger.info(test_api_appmatrix_list.__doc__)
    api_path = api_performance_data['case_module']['app_manager']['appmatrix']['path']['appmatrix_list']
    list_application_url = api_server + api_path

    take_time = list_api(request_obj, header_after_login, list_application_url)
    insert_list_api = "INSERT INTO {db}.{table} (api, take_time, c_time) VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=appmatrix_list_table, api=api_path, take_time=take_time, c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert_list_api)


@pytest.mark.usefixtures("create_appmatrix_event_table")
def test_api_appmatrix_event(mysql_obj, api_server, header_after_login, db, appmatrix_event_table, request_obj,
                             api_performance_data, appmatrixes_data):
    test_api_appmatrix_event.__doc__ = 'Test start, test_api_appmatrix_event test !'
    logger.info(test_api_appmatrix_event.__doc__)
    api_path = api_performance_data['case_module']['app_manager']['appmatrix']['path']['appmatrix_event']

    event_url = api_server + api_path
    event_url = event_url.replace("appmatrix_name", random.choice(appmatrixes_data)['appMatrixName'])

    take_time = list_api(request_obj, header_after_login, event_url)
    insert_list_api = "INSERT INTO {db}.{table} (api, take_time, c_time) VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=appmatrix_event_table, api=api_path, take_time=take_time, c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert_list_api)


@pytest.mark.usefixtures("create_appmatrix_update_table")
def test_api_appmatrix_update(mysql_obj, api_server, header_after_login, db, appmatrix_update_table, request_obj,
                              api_performance_data, appmatrixes_data):
    test_api_appmatrix_update.__doc__ = 'Test start, test_api_appmatrix_update test !'
    logger.info(test_api_appmatrix_update.__doc__)
    api_path = api_performance_data['case_module']['app_manager']['appmatrix']['path']['update_appmatrix']

    update_appmatrix_url = api_server + api_path

    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for appmatrix in appmatrixes_data:
        new_appmatrix = copy.deepcopy(appmatrix)
        data = api_performance_data['case_module']['app_manager']['appmatrix']['default_appmatrix_data'].copy()
        update_type = random.choice(api_performance_data['case_module']['app_manager']['appmatrix']['update_type'])

        if update_type == "update_current":
            new_appmatrix['applicationList'][0]['imagePullPolicy'] = \
                random.choice(data['applicationList'][0]['imagePullPolicy'])
            new_appmatrix['applicationList'][0]['containerName'] = "{}-{}".format("autotest", time_str())

        elif update_type == "add_one":
            new_appmatrix['applicationList'].append()
            new_appmatrix['topology'].append()

        elif update_type == "delete_one":
            new_appmatrix['applicationList'].pop()
            new_appmatrix['topology'].pop()

        futures.append(pool.submit(update_api, request_obj, new_appmatrix, header_after_login, update_appmatrix_url))
    pool.shutdown()

    for future in as_completed(futures):
        insert_update_api = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                            "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=appmatrix_update_table, api=api_path, take_time=future.result(), c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert_update_api)

    sleep(api_performance_data['common']['wait_time'])

    api_path = api_performance_data['case_module']['app_manager']['appmatrix']['path']['appmatrix_detail']
    detail_url = api_server + api_path
    pool_check = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures_check = []
    for appmatrix in appmatrixes_data:
        futures_check.append(pool_check.submit(is_appmatrix_running, request_obj, appmatrix['appMatrixName'],
                                               header_after_login, detail_url.replace("appmatrix_name",
                                                                                      appmatrix['appMatrixName'])))
    pool_check.shutdown()
    for future in as_completed(futures_check):
        future.result()


@pytest.mark.usefixtures("create_appmatrix_delete_table")
def test_api_appmatrix_delete(mysql_obj, api_server, header_after_login, db, appmatrix_delete_table, request_obj,
                              api_performance_data, appmatrixes_data):
    test_api_appmatrix_delete.__doc__ = 'Test start, test_api_appmatrix_delete test !'
    logger.info(test_api_appmatrix_delete.__doc__)
    api_path = api_performance_data['case_module']['app_manager']['appmatrix']['path']['delete_appmatrix']

    delete_appmatrix_url = api_server + api_path
    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for appmatrix in appmatrixes_data:
        futures.append(pool.submit(delete_api, request_obj, header_after_login, delete_appmatrix_url,
                                   {"appMatrixName": appmatrix['appMatrixName']}))
    pool.shutdown()

    for future in as_completed(futures):
        insert_delete_api = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                            "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=appmatrix_delete_table, api=api_path, take_time=future.result(), c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert_delete_api)

    api_path = api_performance_data['case_module']['app_manager']['appmatrix']['path']['appmatrix_detail']
    detail_url = api_server + api_path
    pool_check = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures_check = []
    for appmatrix in appmatrixes_data:
        futures_check.append(pool_check.submit(is_application_not_exist, request_obj, appmatrix['appMatrixName'],
                                               header_after_login, detail_url.replace("appmatrix_name",
                                                                                      appmatrix['appMatrixName'])))
    pool_check.shutdown()
    for future in as_completed(futures_check):
        future.result()


@pytest.mark.usefixtures("create_mission_create_table")
def test_api_mission_create(mysql_obj, api_server, header_after_login, db, mission_create_table, request_obj,
                            api_performance_data, missions_data):
    test_api_mission_create.__doc__ = 'Test start, test_api_mission_create test !'
    logger.info(test_api_mission_create.__doc__)
    api_path = api_performance_data['case_module']['app_manager']['mission']['path']['create_mission']

    create_mission_url = api_server + api_path
    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for mission in missions_data:
        futures.append(pool.submit(create_api, request_obj, mission, header_after_login, create_mission_url))
    pool.shutdown()

    for future in as_completed(futures):
        insert_create_api = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                            "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=mission_create_table, api=api_path, take_time=future.result(), c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert_create_api)

    api_path = api_performance_data['case_module']['app_manager']['mission']['path']['mission_detail']
    detail_url = api_server + api_path
    pool_check = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures_check = []
    for mission in missions_data:
        futures_check.append(pool_check.submit(is_mission_running, request_obj, mission['name'],
                                               header_after_login, detail_url.replace("mission_name", mission['name'])))
    pool_check.shutdown()
    for future in as_completed(futures_check):
        future.result()


@pytest.mark.usefixtures("create_mission_list_table")
def test_api_mission_list(mysql_obj, api_server, header_after_login, db, mission_list_table, request_obj,
                          api_performance_data):
    test_api_mission_list.__doc__ = 'Test start, test_api_mission_list test !'
    logger.info(test_api_mission_list.__doc__)
    api_path = api_performance_data['case_module']['app_manager']['mission']['path']['mission_list']
    list_mission_url = api_server + api_path

    take_time = list_api(request_obj, header_after_login, list_mission_url)
    insert_list_api = "INSERT INTO {db}.{table} (api, take_time, c_time) VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=mission_list_table, api=api_path, take_time=take_time, c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert_list_api)


@pytest.mark.usefixtures("create_mission_event_table")
def test_api_mission_event(mysql_obj, api_server, header_after_login, db, mission_event_table, request_obj,
                           api_performance_data, missions_data):
    test_api_mission_event.__doc__ = 'Test start, test_api_mission_event test !'
    logger.info(test_api_mission_event.__doc__)
    api_path = api_performance_data['case_module']['app_manager']['mission']['path']['mission_event']

    event_url = api_server + api_path
    event_url = event_url.replace("mission_name", random.choice(missions_data)['name'])

    take_time = list_api(request_obj, header_after_login, event_url)
    insert_list_api = "INSERT INTO {db}.{table} (api, take_time, c_time) VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=mission_event_table, api=api_path, take_time=take_time, c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert_list_api)


@pytest.mark.usefixtures("create_mission_delete_table")
def test_api_mission_delete(mysql_obj, api_server, header_after_login, db, mission_delete_table, request_obj,
                            api_performance_data, missions_data):
    test_api_mission_delete.__doc__ = 'Test start, test_api_mission_delete test !'
    logger.info(test_api_mission_delete.__doc__)
    api_path = api_performance_data['case_module']['app_manager']['mission']['path']['delete_mission']

    delete_mission_url = api_server + api_path
    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for mission in missions_data:
        futures.append(pool.submit(delete_api, request_obj, header_after_login, delete_mission_url,
                                   {"name": mission['name']}))
    pool.shutdown()

    for future in as_completed(futures):
        insert_delete_api = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                            "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=mission_delete_table, api=api_path, take_time=future.result(), c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert_delete_api)

    api_path = api_performance_data['case_module']['app_manager']['mission']['path']['mission_detail']
    detail_url = api_server + api_path
    pool_check = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures_check = []
    for mission in missions_data:
        futures_check.append(pool_check.submit(is_application_not_exist, request_obj, mission['name'],
                                               header_after_login, detail_url.replace("mission_name", mission['name'])))
    pool_check.shutdown()
    for future in as_completed(futures_check):
        future.result()


@pytest.mark.usefixtures("create_cronmission_create_table")
def test_api_cronmission_create(mysql_obj, api_server, header_after_login, db, cronmission_create_table, request_obj,
                                api_performance_data, cronmissions_data):
    test_api_cronmission_create.__doc__ = 'Test start, test_api_cronmission_create test !'
    logger.info(test_api_cronmission_create.__doc__)
    api_path = api_performance_data['case_module']['app_manager']['cronmission']['path']['create_cronmission']

    create_cronmission_url = api_server + api_path
    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for cronmission in cronmissions_data:
        futures.append(pool.submit(create_api, request_obj, cronmission, header_after_login, create_cronmission_url))
    pool.shutdown()

    for future in as_completed(futures):
        insert_create_api = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                            "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=cronmission_create_table, api=api_path, take_time=future.result(),
                    c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert_create_api)

    api_path = api_performance_data['case_module']['app_manager']['cronmission']['path']['cronmission_detail']
    detail_url = api_server + api_path
    pool_check = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures_check = []
    for cronmission in cronmissions_data:
        futures_check.append(pool_check.submit(check_cronmission_status, request_obj, cronmission['cronMissionName'],
                                               header_after_login, detail_url))
    pool_check.shutdown()
    for future in as_completed(futures_check):
        future.result()


@pytest.mark.usefixtures("create_cronmission_list_table")
def test_api_cronmission_list(mysql_obj, api_server, header_after_login, db, cronmission_list_table, request_obj,
                              api_performance_data):
    test_api_cronmission_list.__doc__ = 'Test start, test_api_cronmission_list test !'
    logger.info(test_api_cronmission_list.__doc__)
    api_path = api_performance_data['case_module']['app_manager']['cronmission']['path']['cronmission_list']
    list_application_url = api_server + api_path

    take_time = list_api(request_obj, header_after_login, list_application_url)
    insert_list_api = "INSERT INTO {db}.{table} (api, take_time, c_time) VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=cronmission_list_table, api=api_path, take_time=take_time, c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert_list_api)


@pytest.mark.usefixtures("create_cronmission_event_table")
def test_api_cronmission_event(mysql_obj, api_server, header_after_login, db, cronmission_event_table, request_obj,
                               api_performance_data, cronmissions_data):
    test_api_cronmission_event.__doc__ = 'Test start, test_api_cronmission_event test !'
    logger.info(test_api_cronmission_event.__doc__)
    api_path = api_performance_data['case_module']['app_manager']['cronmission']['path']['cronmission_event']

    event_url = api_server + api_path
    event_url = event_url.replace("cronmission_name", random.choice(cronmissions_data)['cronMissionName'])

    take_time = list_api(request_obj, header_after_login, event_url)
    insert_list_api = "INSERT INTO {db}.{table} (api, take_time, c_time) VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=cronmission_event_table, api=api_path, take_time=take_time, c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert_list_api)


@pytest.mark.usefixtures("create_cronmission_suspend_table")
def test_api_cronmission_suspend(mysql_obj, api_server, header_after_login, db, cronmission_suspend_table, request_obj,
                                api_performance_data, cronmissions_data):
    test_api_cronmission_suspend.__doc__ = 'Test start, test_api_cronmission_suspend test !'
    logger.info(test_api_cronmission_suspend.__doc__)
    api_path = api_performance_data['case_module']['app_manager']['cronmission']['path']['suspend_cronmission']

    suspend_cronmission_url = api_server + api_path
    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for cronmission in cronmissions_data:
        suspend_data = {
            "cronMissionName": cronmission['cronMissionName'],
            "stop": 1
        }
        futures.append(pool.submit(create_api, request_obj, suspend_data, header_after_login, suspend_cronmission_url))
    pool.shutdown()

    for future in as_completed(futures):
        insert_create_api = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                            "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=cronmission_suspend_table, api=api_path, take_time=future.result(),
                    c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert_create_api)

    api_path = api_performance_data['case_module']['app_manager']['cronmission']['path']['cronmission_detail']
    detail_url = api_server + api_path
    pool_check = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures_check = []
    for cronmission in cronmissions_data:
        futures_check.append(pool_check.submit(check_cronmission_status, request_obj, cronmission['cronMissionName'],
                                               header_after_login, detail_url, status='suspend'))
    pool_check.shutdown()
    for future in as_completed(futures_check):
        future.result()


@pytest.mark.usefixtures("create_cronmission_suspend_cancel_table")
def test_api_cronmission_suspend_cancel(mysql_obj, api_server, header_after_login, db, cronmission_suspend_cancel_table,
                                        request_obj, api_performance_data, cronmissions_data):
    test_api_cronmission_suspend_cancel.__doc__ = 'Test start, test_api_cronmission_suspend_cancel test !'
    logger.info(test_api_cronmission_suspend_cancel.__doc__)
    api_path = api_performance_data['case_module']['app_manager']['cronmission']['path']['suspend_cronmission']

    suspend_cronmission_url = api_server + api_path
    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for cronmission in cronmissions_data:
        suspend_data = {
            "cronMissionName": cronmission['cronMissionName'],
            "stop": 0
        }
        futures.append(pool.submit(create_api, request_obj, suspend_data, header_after_login, suspend_cronmission_url))
    pool.shutdown()

    for future in as_completed(futures):
        insert_create_api = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                            "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=cronmission_suspend_cancel_table, api=api_path, take_time=future.result(),
                    c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert_create_api)

    api_path = api_performance_data['case_module']['app_manager']['cronmission']['path']['cronmission_detail']
    detail_url = api_server + api_path
    pool_check = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures_check = []
    for cronmission in cronmissions_data:
        futures_check.append(pool_check.submit(check_cronmission_status, request_obj, cronmission['cronMissionName'],
                                               header_after_login, detail_url))
    pool_check.shutdown()
    for future in as_completed(futures_check):
        future.result()


@pytest.mark.usefixtures("create_cronmission_update_table")
def test_api_cronmission_update(mysql_obj, api_server, header_after_login, db, cronmission_update_table, request_obj,
                                api_performance_data, cronmissions_data):
    test_api_cronmission_update.__doc__ = 'Test start, test_api_cronmission_update test !'
    logger.info(test_api_cronmission_update.__doc__)
    api_path = api_performance_data['case_module']['app_manager']['cronmission']['path']['update_cronmission']

    update_cronmission_url = api_server + api_path

    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for cronmission in cronmissions_data:
        data = api_performance_data['case_module']['app_manager']['cronmission']['default_cronmission_data']

        new_cronmission = copy.deepcopy(cronmission)
        new_cronmission['imagePullPolicy'] = random.choice(data['imagePullPolicy'])
        new_cronmission['concurrencyPolicy'] = random.choice(data['concurrencyPolicy'])

        futures.append(pool.submit(update_api, request_obj, new_cronmission, header_after_login,
                                   update_cronmission_url))
    pool.shutdown()

    for future in as_completed(futures):
        insert_update_api = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                            "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=cronmission_update_table, api=api_path, take_time=future.result(),
                    c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert_update_api)

    sleep(api_performance_data['common']['wait_time'])

    api_path = api_performance_data['case_module']['app_manager']['cronmission']['path']['cronmission_detail']
    detail_url = api_server + api_path
    pool_check = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures_check = []
    for cronmission in cronmissions_data:
        futures_check.append(pool_check.submit(check_cronmission_status, request_obj, cronmission['cronMissionName'],
                                               header_after_login, detail_url))
    pool_check.shutdown()
    for future in as_completed(futures_check):
        future.result()


@pytest.mark.usefixtures("create_cronmission_delete_table")
def test_api_cronmission_delete(mysql_obj, api_server, header_after_login, db, cronmission_delete_table, request_obj,
                                api_performance_data, cronmissions_data):
    test_api_cronmission_delete.__doc__ = 'Test start, test_api_cronmission_delete test !'
    logger.info(test_api_cronmission_delete.__doc__)
    api_path = api_performance_data['case_module']['app_manager']['cronmission']['path']['delete_cronmission']

    delete_mission_url = api_server + api_path
    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for cronmission in cronmissions_data:
        futures.append(pool.submit(delete_api, request_obj, header_after_login, delete_mission_url,
                                   {"cronMissionName": cronmission['cronMissionName']}))
    pool.shutdown()

    for future in as_completed(futures):
        insert_delete_api = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                            "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=cronmission_delete_table, api=api_path, take_time=future.result(),
                    c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert_delete_api)

    api_path = api_performance_data['case_module']['app_manager']['cronmission']['path']['cronmission_detail']
    detail_url = api_server + api_path
    pool_check = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures_check = []
    for cronmission in cronmissions_data:
        futures_check.append(pool_check.submit(is_cronmission_not_exist, request_obj, cronmission['cronMissionName'],
                                               header_after_login, detail_url))
    pool_check.shutdown()
    for future in as_completed(futures_check):
        future.result()


@pytest.mark.usefixtures("create_apparafile_create_table")
def test_api_apparafile_create(mysql_obj, api_server, header_after_login, db, apparafile_create_table, request_obj,
                               api_performance_data, apparafiles_data):
    test_api_apparafile_create.__doc__ = 'Test start, test_api_apparafile_create test !'
    logger.info(test_api_apparafile_create.__doc__)
    api_path = api_performance_data['case_module']['app_manager']['apparafile']['path']['create_apparafile']

    create_apparafile_url = api_server + api_path
    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for apparafile in apparafiles_data:
        futures.append(pool.submit(create_api, request_obj, apparafile, header_after_login, create_apparafile_url))
    pool.shutdown()

    for future in as_completed(futures):
        insert_create_api = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                            "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=apparafile_create_table, api=api_path, take_time=future.result(),
                    c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert_create_api)

    api_path = api_performance_data['case_module']['app_manager']['apparafile']['path']['apparafile_list']

    pool_check = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures_check = []
    for apparafile in apparafiles_data:
        apparafile_check_url = api_server + api_path + apparafile['name']
        futures_check.append(pool_check.submit(is_apparafile_exist, request_obj, apparafile['name'],
                                               header_after_login, apparafile_check_url))
    pool_check.shutdown()
    for future in as_completed(futures_check):
        future.result()


@pytest.mark.usefixtures("create_apparafile_list_table")
def test_api_apparafile_list(mysql_obj, api_server, header_after_login, db, apparafile_list_table, request_obj,
                             api_performance_data):
    test_api_apparafile_list.__doc__ = 'Test start, test_api_apparafile_list test !'
    logger.info(test_api_apparafile_list.__doc__)
    api_path = api_performance_data['case_module']['app_manager']['apparafile']['path']['apparafile_list']
    list_apparafile_url = api_server + api_path

    take_time = list_api(request_obj, header_after_login, list_apparafile_url)
    insert_list_api = "INSERT INTO {db}.{table} (api, take_time, c_time) VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=apparafile_list_table, api=api_path, take_time=take_time, c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert_list_api)


@pytest.mark.usefixtures("create_apparafile_update_table")
def test_api_apparafile_update(mysql_obj, api_server, header_after_login, db, apparafile_update_table, request_obj,
                               api_performance_data, apparafiles_data):
    test_api_apparafile_update.__doc__ = 'Test start, test_api_apparafile_update test !'
    logger.info(test_api_apparafile_update.__doc__)
    api_path = api_performance_data['case_module']['app_manager']['apparafile']['path']['update_apparafile']
    before_apparafile_data = []

    update_apparafile_url = api_server + api_path

    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for apparafile in apparafiles_data:
        new_apparafile = copy.deepcopy(apparafile)
        all_keys = list(new_apparafile['data'].keys())
        del_key = random.choice(all_keys)
        update_key = random.choice(all_keys)

        del new_apparafile['data'][del_key]
        new_apparafile['data']['add_new'] = 'add_new'
        new_apparafile['data'][update_key] = 'update'

        before_apparafile_data.append({'name': new_apparafile['name'], 'data': new_apparafile['data']})

        futures.append(pool.submit(create_api, request_obj, new_apparafile, header_after_login, update_apparafile_url))
    pool.shutdown()

    for future in as_completed(futures):
        insert_update_api = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                            "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=apparafile_update_table, api=api_path, take_time=future.result(),
                    c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert_update_api)

    sleep(api_performance_data['common']['wait_time'])

    api_path = api_performance_data['case_module']['app_manager']['apparafile']['path']['apparafile_detail']
    detail_url = api_server + api_path
    pool_check = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures_check = []
    for before_apparafile in before_apparafile_data:
        futures_check.append(pool_check.submit(check_data, request_obj, before_apparafile['data'],
                                               header_after_login, detail_url.replace("af_name",
                                                                                      before_apparafile['name'])))
    pool_check.shutdown()
    for future in as_completed(futures_check):
        future.result()


@pytest.mark.usefixtures("create_apparafile_delete_table")
def test_api_apparafile_delete(mysql_obj, api_server, header_after_login, db, apparafile_delete_table, request_obj,
                               api_performance_data, apparafiles_data):
    test_api_apparafile_delete.__doc__ = 'Test start, test_api_apparafile_delete test !'
    logger.info(test_api_apparafile_delete.__doc__)
    api_path = api_performance_data['case_module']['app_manager']['apparafile']['path']['delete_apparafile']

    delete_apparafile_url = api_server + api_path
    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    for apparafile in apparafiles_data:
        futures.append(pool.submit(delete_api, request_obj, header_after_login, delete_apparafile_url,
                                   {"name": apparafile['name']}))
    pool.shutdown()

    for future in as_completed(futures):
        insert_delete_api = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                            "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=apparafile_delete_table, api=api_path, take_time=future.result(),
                    c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert_delete_api)

    api_path = api_performance_data['case_module']['app_manager']['apparafile']['path']['apparafile_list']
    pool_check = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures_check = []
    for apparafile in apparafiles_data:
        apparafile_check_url = api_server + api_path + apparafile['name']
        futures_check.append(pool_check.submit(is_apparafile_exist, request_obj, apparafile['name'],
                                               header_after_login, apparafile_check_url, False))
    pool_check.shutdown()
    for future in as_completed(futures_check):
        future.result()

