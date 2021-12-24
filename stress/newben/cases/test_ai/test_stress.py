import json
import random
import pytest
import os
import datetime
from settings.global_settings import REMOTE_REGISTRY, LOCAL_REGISTRY
from concurrent.futures import ThreadPoolExecutor, as_completed
from libs.log_obj import LogObj
from stress import arguments
from stress.newben.common.common import create_mission_yaml, check_health, create_stop_ai_mission, ai_auth_token
from utils.util import time_str
from settings.newben_settings import MISSION_YAML_PATH
from prettytable import PrettyTable

logger = LogObj().get_logger()
args = arguments.parse_arg()


@pytest.fixture(scope='session')
def check_health_tb():
    tb = PrettyTable()
    tb.field_names = ['Check Health Time']
    return tb


@pytest.fixture(scope='function', autouse=True)
def check(node1_obj, etcd_node_obj, check_health_tb):
    logger.info('Check health before test!')
    check_health(node1_obj, etcd_node_obj, args.workspace, single=args.single)
    node1_obj.is_gpu_healthy(args.gpu_quantity)
    yield
    logger.info('Check health after test!')
    node1_obj.is_gpu_healthy(args.gpu_quantity)
    take_time = check_health(node1_obj, etcd_node_obj, args.workspace, single=args.single)
    check_health_tb.add_row([take_time])
    logger.debug('Check Health Report: \n{0}'.format(check_health_tb))


@pytest.fixture(scope='session')
def mission_name_list():
    mission_name_list = []
    for i in range(args.concurrent):
        mission_name = 'neilautomission-{0}-{1}-{2}'.format(args.mission_type, time_str(), i)
        mission_name_list.append(mission_name)
    return mission_name_list


@pytest.fixture(scope='session')
def mission_yaml_file_path_list(node1_obj, mission_name_list):
    if args.image not in node1_obj.images:
        local_image = '{0}/{1}'.format(LOCAL_REGISTRY, '/'.join(args.image.split('/')[1:]))
        node1_obj.docker_pull(args.image)
        node1_obj.docker_tag(args.image, local_image)
        node1_obj.docker_push(local_image)
    else:
        local_image = args.image
    logger.info('Mission image is {0}!'.format(local_image))
    mission_yaml_file_path_list = []
    node1_obj.make_dir(MISSION_YAML_PATH)
    for mission_name in mission_name_list:
        pytorch_datas = {
            '/root/code': args.train_code_path,
            '/root/data': args.train_data_path,
            '/root/output': args.train_output_path + mission_name
        }
        tensorflow_datas = {
            '/root/code': args.train_code_path,
            '/root/data': args.train_data_path,
            '/root/output': args.train_output_path + mission_name
        }
        mission_datas_info = {'tensorflow': tensorflow_datas, 'pytorch': pytorch_datas}
        mission_yaml_file_local_path = create_mission_yaml(mission_name, args.workspace, local_image,
                                                           mission_datas_info[args.mission_type])
        mission_yaml_file_path = os.path.join(MISSION_YAML_PATH, '{0}.yaml'.format(mission_name))
        node1_obj.remote_scp_put(mission_yaml_file_local_path, mission_yaml_file_path)
        mission_yaml_file_path_list.append(mission_yaml_file_path)
    return mission_yaml_file_path_list


@pytest.fixture(scope='function')
def mission_name_list_new():
    mission_name_list = []
    for i in range(args.concurrent):
        mission_name = 'automission-{}-{}'.format(int(datetime.datetime.now().timestamp()), i)
        mission_name_list.append(mission_name)
    return mission_name_list


def test_create_mission(node1_obj, mission_yaml_file_path_list):
    logger.info('Test start!')
    start_time = datetime.datetime.now()
    pool = ThreadPoolExecutor(max_workers=5)
    futures = []
    for mission_yaml_file_path in mission_yaml_file_path_list:
        futures.append(pool.submit(node1_obj.nbctl_create, mission_yaml_file_path))
    pool.shutdown()
    for future in as_completed(futures):
        future.result()

    node1_obj.is_jobs_succeeded(args.workspace)
    end_time = datetime.datetime.now()
    take_time = end_time - start_time
    logger.info('{0} jobs succeeded take time: {1}'.format(args.concurrent, take_time))


def test_delete_mission(node1_obj, mission_name_list):
    pool = ThreadPoolExecutor(max_workers=5)
    futures = []
    for mission_name in mission_name_list:
        futures.append(pool.submit(node1_obj.delete_mission, mission_name, args.workspace))
    pool.shutdown()
    for future in as_completed(futures):
        future.result()

    for mission_name in mission_name_list:
        node1_obj.is_mission_not_exist(mission_name)


def test_job_long_time(node1_obj):
    logger.info('Test start!')
    if args.image not in node1_obj.images:
        local_image = '{0}/{1}'.format(LOCAL_REGISTRY, '/'.join(args.image.split('/')[1:]))
        node1_obj.docker_pull(args.image)
        node1_obj.docker_tag(args.image, local_image)
        node1_obj.docker_push(local_image)
    else:
        local_image = args.image

    logger.info('Mission image is {0}!'.format(local_image))
    mission_yaml_file_path_list = []
    mission_name_list = []
    # command = ['sleep']
    # command.append(str(args.job_time))
    train_command = args.train_mission_command.split("===")
    for i in range(args.concurrent):
        mission_name = 'neilautomission-longtime-{0}-{1}'.format(time_str(), i)
        pytorch_datas = {
            '/root/code': args.train_code_path,
            '/root/data': args.train_data_path,
            '/root/output': '{}/{}'.format(args.train_output_path, mission_name)
        }
        tensorflow_datas = {
            '/root/code': args.train_code_path,
            '/root/data': args.train_data_path,
            '/root/output': '{}/{}'.format(args.train_output_path, mission_name)
        }
        mission_datas_info = {'tensorflow': tensorflow_datas, 'pytorch': pytorch_datas}
        mission_yaml_file_local_path = create_mission_yaml(mission_name, args.workspace, local_image,
                                                     mission_datas_info[args.mission_type], train_command)
        mission_yaml_file_path = os.path.join(MISSION_YAML_PATH, '{0}.yaml'.format(mission_name))
        node1_obj.remote_scp_put(mission_yaml_file_local_path, mission_yaml_file_path)
        mission_yaml_file_path_list.append(mission_yaml_file_path)
        mission_name_list.append(mission_name)

    pool = ThreadPoolExecutor(max_workers=5)
    futures = []
    for mission_yaml_file_path in mission_yaml_file_path_list:
        futures.append(pool.submit(node1_obj.nbctl_create, mission_yaml_file_path))
    pool.shutdown()
    for future in as_completed(futures):
        future.result()


def test_force_stop_train(mission_name_list_new, request_obj, node1_obj):
    logger.info('Test Force Stop Train mission start!')
    train_command = ' '.join(args.train_mission_command.split("==="))
    auth_token = ai_auth_token(request_obj, args.ai_api_username, args.ai_api_password, args.api_server)
    box_table = PrettyTable(['BoxName', 'StopBoxTime(s)', 'IsGreaterThan3s'])
    check_point = True
    pool = ThreadPoolExecutor(max_workers=5)
    futures = []
    for mission_name in mission_name_list_new:
        futures.append(pool.submit(create_stop_ai_mission, request_obj, node1_obj, args.api_server, mission_name,
                                   auth_token, random.randint(args.min_wait, args.max_wait), args.train_code_path,
                                   args.train_data_path, args.train_output_path, train_command))
    pool.shutdown()
    for future in as_completed(futures):
        if future.result()[1] > 3:
            future.result().append(True)
            check_point = False
        else:
            future.result().append(False)
        box_table.add_row(future.result())
    if check_point:
        logger.info("The results of stop mission&box\n{}".format(box_table))
    else:
        raise Exception("Stop box take time greater than 10 s, the results check below\n{}".format(box_table))
