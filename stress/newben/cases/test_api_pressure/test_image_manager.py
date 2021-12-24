import copy
import json
import os
import shutil
import random
import time
import uuid
import websocket
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

import pytest

from libs.log_obj import LogObj
from libs.ssh_obj import SSHObj
from stress.conftest import args
from stress.newben.common.common import create, get, upload, delete, online_product_image, download

logger = LogObj().get_logger()


@pytest.fixture(scope='session')
def list_images_table():
    return 'list_images'


@pytest.fixture(scope='session')
def upload_image_table():
    return 'upload_image'


@pytest.fixture(scope='session')
def view_image_detail_table():
    return 'view_image_detail'


@pytest.fixture(scope='session')
def download_image_table():
    return 'download_image'


@pytest.fixture(scope='session')
def delete_image_table():
    return 'delete_image'


@pytest.fixture(scope='session')
def product_image_table():
    return 'product_image'


@pytest.fixture(scope='session')
def create_list_images_table(mysql_obj, db, list_images_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, list_images_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_upload_image_table(mysql_obj, db, upload_image_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, upload_image_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_view_image_detail_table(mysql_obj, db, view_image_detail_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, view_image_detail_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_download_image_table(mysql_obj, db, download_image_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, download_image_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_delete_image_table(mysql_obj, db, delete_image_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, delete_image_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_product_image_table(mysql_obj, db, product_image_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, product_image_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def prepare_image_tar_pkg(api_performance_data):
    test_env_info = api_performance_data['common']['execute_test_env']
    ssh_obj = SSHObj(test_env_info['host'], test_env_info['username'], test_env_info['password'])
    dockerfile_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                   'data/dockerfile/Dockerfile')
    origin_repository_tag = 'nginx:v0'
    ssh_obj.docker_build(dockerfile_path, origin_repository_tag)
    image_tar_pkgs = []
    for i in range(api_performance_data['common']['data_quantity']):
        new_repository_tag = '{}:{}'.format('nginx', 'v' + str(i + 1))
        ssh_obj.docker_tag(origin_repository_tag, new_repository_tag)
        pkg_name = '{}.tar'.format('nginx' + str(i + 1))
        ssh_obj.docker_save(pkg_name, new_repository_tag)
        ssh_obj.run_cmd('mv {} /root'.format(pkg_name))
        file_path = os.path.join('/root', pkg_name)
        image_tar_pkgs.append(file_path)
    return image_tar_pkgs


@pytest.fixture(scope='session')
def get_product_image_uid(uid_api_server, api_performance_data, header_after_login, ):
    api_path = api_performance_data['case_module']['image_manager']['docker_image']['path']['get_uid']
    get_uid_url = uid_api_server + api_path

    ws = websocket.create_connection(get_uid_url)
    data = {'token': header_after_login['Authorization'], 't': int(round(time.time() * 1000))}
    ws.send(json.dumps(data))
    uid = json.loads(ws.recv())['uid']
    logger.debug(uid)
    ws.close()
    return uid


@pytest.fixture(scope='session')
def online_product_image_data(api_performance_data, get_product_image_uid):
    data = copy.deepcopy(
        api_performance_data['case_module']['image_manager']['docker_image']['default_product_image_data'])
    data['query_param']['uid'] = get_product_image_uid
    name = data['body']['name']
    file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                             'data/image_product/exec_test.sh')
    file_obj = open(file_path, 'rb')
    file = {name: file_obj}
    data['file'] = file
    return data


@pytest.mark.usefixtures("create_list_images_table")
def test_images_list_view(mysql_obj, api_server, header_after_login, db, list_images_table,
                          request_obj, api_performance_data):
    test_images_list_view.__doc__ = 'Test start, test_images_list_view test !'
    logger.info(test_images_list_view.__doc__)

    api_path = api_performance_data['case_module']['image_manager']['docker_image']['path']['get_image_list']
    image_list_url = api_server + api_path
    param = {"page": 1, "size": 20}
    response, take_time = get(request_obj, image_list_url, header_after_login, param)
    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=list_images_table, api=api_path, take_time=take_time, c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert)


@pytest.mark.run(order=1)
@pytest.mark.usefixtures("create_upload_image_table")
def test_image_upload(mysql_obj, api_server, header_after_login, db, upload_image_table, request_obj,
                      api_performance_data, prepare_image_tar_pkg):
    test_image_upload.__doc__ = 'Test start, test_image_upload test !'
    logger.info(test_image_upload.__doc__)

    api_path = api_performance_data['case_module']['image_manager']['docker_image']['path']['upload_image']
    upload_image_url = api_server + api_path

    # pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    # futures = []
    # header = header_after_login.copy()
    # del header['Content-Type']
    # for data in upload_image_request_data:
    #     futures.append(pool.submit(upload, request_obj, upload_image_url, header, data))
    # pool.shutdown()

    header = header_after_login.copy()
    del header['Content-Type']

    name = \
        api_performance_data['case_module']['image_manager']['docker_image']['default_upload_image_data']['body'][
            'name']
    for tar in prepare_image_tar_pkg:
        file_obj = open(tar, 'rb')
        file = {name: file_obj}
        response, take_time = upload(request_obj, upload_image_url, header, file)

        insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                 "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=upload_image_table, api=api_path, take_time=take_time, c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert)


@pytest.mark.run(order=2)
@pytest.mark.usefixtures("create_view_image_detail_table")
def test_image_view_detail(mysql_obj, api_server, header_after_login, db, view_image_detail_table,
                           request_obj, api_performance_data):
    test_image_view_detail.__doc__ = 'Test start, test_image_view_detail test !'
    logger.info(test_image_view_detail.__doc__)

    image_list_path = api_performance_data['case_module']['image_manager']['docker_image']['path']['get_image_list']
    image_list_url = api_server + image_list_path
    param = {"page": 1, "size": 20}
    result, _ = get(request_obj, image_list_url, header_after_login, param)
    random_image_name = random.choice([data["name"] for data in result["data"]["list"]])

    api_path = api_performance_data['case_module']['image_manager']['docker_image']['path']['view_image_detail']
    view_image_detail_url = api_server + api_path

    # image = registry.cluster.local / venus / centos & page = 1 & pageSize = 10
    param = {"image": random_image_name, "page": 1, "pageSize": 10}
    response, take_time = get(request_obj, view_image_detail_url, header_after_login, param)
    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=view_image_detail_table, api=api_path, take_time=take_time, c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert)


@pytest.mark.run(order=3)
@pytest.mark.usefixtures("create_download_image_table")
def test_image_download(mysql_obj, api_server, header_after_login, db, download_image_table, request_obj,
                        api_performance_data):
    test_image_download.__doc__ = 'Test start, test_image_download test !'
    logger.info(test_image_download.__doc__)

    api_path = api_performance_data['case_module']['image_manager']['docker_image']['path']['download_image']
    download_image_url = api_server + api_path

    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    image_list_path = api_performance_data['case_module']['image_manager']['docker_image']['path']['get_image_list']
    image_list_url = api_server + image_list_path
    param = {"page": 1, "size": 20}
    result, _ = get(request_obj, image_list_url, header_after_login, param)
    random_image = random.choice(result["data"]["list"])
    image_name = random_image['name']
    image_tag = random_image['tags'][0]

    param = {'images': '{}:{}'.format(image_name, image_tag)}
    for _ in range(api_performance_data['common']['data_quantity']):
        futures.append(pool.submit(download, request_obj, download_image_url, header_after_login, param))
    pool.shutdown()

    for future in as_completed(futures):
        insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                 "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=download_image_table, api=api_path, take_time=future.result(),
                    c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert)


@pytest.mark.run(order=4)
@pytest.mark.usefixtures("create_delete_image_table")
def test_image_delete(mysql_obj, api_server, header_after_login, db, delete_image_table, request_obj,
                      api_performance_data):
    test_image_delete.__doc__ = 'Test start, test_image_delete test !'
    logger.info(test_image_delete.__doc__)

    api_path = api_performance_data['case_module']['image_manager']['docker_image']['path']['delete_image']
    delete_image_url = api_server + api_path

    pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    futures = []
    data = api_performance_data['case_module']['image_manager']['docker_image']['default_delete_image_data']
    for i in range(api_performance_data['common']['data_quantity']):
        param = {'image': data['image'], 'tag': 'v' + str(i + 1)}
        futures.append(pool.submit(delete, request_obj, delete_image_url, header_after_login, param=param))
    pool.shutdown()

    for future in as_completed(futures):
        insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                 "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=delete_image_table, api=api_path, take_time=future.result()[1], c_time=datetime.now())
        mysql_obj.run_sql_cmd(insert)


@pytest.mark.run(order=5)
@pytest.mark.usefixtures("create_product_image_table")
def test_image_online_product(mysql_obj, api_server, header_after_login, db, product_image_table, request_obj,
                              api_performance_data, online_product_image_data):
    test_image_online_product.__doc__ = 'Test start, test_image_online_product test !'
    logger.info(test_image_online_product.__doc__)

    api_path = api_performance_data['case_module']['image_manager']['docker_image']['path']['online_product_image']
    online_product_image_url = api_server + api_path

    # pool = ThreadPoolExecutor(max_workers=api_performance_data['common']['concurrent'])
    # futures = []
    # for data in online_product_image_data:
    #     param = data['query_param']
    #     file = data['file']
    #     futures.append(
    #         pool.submit(online_product_image, ))
    # pool.shutdown()

    param = online_product_image_data['query_param']
    file = online_product_image_data['file']
    response, take_time = online_product_image(request_obj, online_product_image_url, header_after_login, param, file)

    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=product_image_table, api=api_path, take_time=take_time, c_time=datetime.now())
    mysql_obj.run_sql_cmd(insert)
