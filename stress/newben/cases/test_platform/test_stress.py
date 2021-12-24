import random
import pytest
import datetime
import os
from settings.newben_settings import APP_YAML_PATH, FORWARD_YAML_PATH, APPARAFILE_YAML_PATH, APPMATRIX_YAML_PATH
from settings.global_settings import LOCAL_TEMP_PATH
from concurrent.futures import ThreadPoolExecutor, as_completed
from libs.log_obj import LogObj
from stress import arguments
from stress.newben.common.common import check_health, create_app_yaml, create_forward_yaml, create_apparafile_yaml, \
    is_nginx_working, create_appmatrix_yaml
from utils.util import time_str
from common.common import dump_yaml_data, compress_files
from stress.newben.common.node_obj import NodeObj


logger = LogObj().get_logger()
args = arguments.parse_arg()


@pytest.fixture(scope='session')
def seam_brs_info(node1_obj):
    seam_brs_info = dict()
    for node_ip in node1_obj.nodes_ip:
        node_obj = NodeObj(node_ip, node1_obj.username, node1_obj.password)
        seam_br_ip = node_obj.seam_br_ip
        if seam_br_ip:
            seam_brs_info[node_ip] = seam_br_ip
    logger.debug('Seam brs info are {0} before test!'.format(seam_brs_info))
    return seam_brs_info


@pytest.fixture(scope='session', autouse=True)
def check_before(node1_obj, etcd_node_obj):
    logger.info('Check health before test!')
    check_health(node1_obj, etcd_node_obj, args.workspace, single=args.single)


@pytest.fixture(scope='function', autouse=True)
def check(node1_obj, etcd_node_obj, seam_brs_info):
    yield
    logger.info('Check health after test!')
    check_health(node1_obj, etcd_node_obj, args.workspace, single=args.single)
    logger.info('Check seam br ip!')
    exception_seam_brs_info = dict()
    for node_ip, seam_br_ip in seam_brs_info.items():
        node_obj = NodeObj(node_ip, node1_obj.username, node1_obj.password)
        after_seam_br_ip = node_obj.seam_br_ip
        if after_seam_br_ip != seam_br_ip:
            exception_seam_brs_info[node_ip] = dict()
            exception_seam_brs_info[node_ip]['after_seam_br_ip'] = after_seam_br_ip
            exception_seam_brs_info[node_ip]['before_seam_br_ip'] = seam_br_ip
        logger.debug('Node {0} seam br ip is {1}!'.format(node_ip, after_seam_br_ip))
    if exception_seam_brs_info:
        raise Exception('Seam br ip had happend change, exception seam brs info were {0}!'.format(
            exception_seam_brs_info))


@pytest.fixture(scope='session')
def before_boxs_info(node1_obj):
    return node1_obj.boxs_info


@pytest.fixture(scope='session')
def app_name_list():
    app_name_list = []
    for i in range(args.concurrent):
        app_name = 'lc-{0}-{1}-{2}'.format(args.app_type, time_str(), i)
        app_name_list.append(app_name)
    return app_name_list


@pytest.fixture(scope='session')
def apparafile_yaml_file_path_list(node1_obj, app_name_list):
    apparafile_yaml_file_path_list = []
    node1_obj.make_dir(APPARAFILE_YAML_PATH)
    compress_file_name = 'apparafiles_yaml_{}.tar'.format(time_str())
    compress_file_path = os.path.join(LOCAL_TEMP_PATH, compress_file_name)
    for app_name in app_name_list:
        apparafile_data = {"index.html": app_name}
        apparafile_yaml_file_local_path = create_apparafile_yaml(app_name, args.workspace, apparafile_data)
        apparafile_yaml_file_path = os.path.join(APPARAFILE_YAML_PATH, '{0}.yaml'.format(app_name))
        compress_files(compress_file_path, apparafile_yaml_file_local_path, new_file_name='{0}.yaml'.format(app_name))
        apparafile_yaml_file_path_list.append(apparafile_yaml_file_path)

    node1_obj.remote_scp_put(compress_file_path, os.path.join(APPARAFILE_YAML_PATH, compress_file_name))
    node1_obj.extract(os.path.join(APPARAFILE_YAML_PATH, compress_file_name), APPARAFILE_YAML_PATH)
    return apparafile_yaml_file_path_list


@pytest.fixture(scope='session')
def app_yaml_file_path_list(node1_obj, app_name_list):
    logger.info('App image is {0}!'.format(args.image))
    app_yaml_file_path_list = []
    node1_obj.make_dir(APP_YAML_PATH)
    compress_file_name = 'apps_yaml_{}.tar'.format(time_str())
    compress_file_path = os.path.join(LOCAL_TEMP_PATH, compress_file_name)
    for app_name in app_name_list:
        if args.app_type == 'nginx':
            volume_mounts = [{"alias": app_name, "mountPath": "/usr/share/nginx/html"}]
            volumes = [{"alias": app_name, "sourceName": app_name, "type": "apparafile"}]
        else:
            volume_mounts = None
            volumes = None
        envs = [{"name": "app_name", "value": app_name}]
        resources = {"cpu": args.app_cpu, "memory": args.app_memory * 1024 * 1024}
        app_yaml_file_local_path = create_app_yaml(app_name, args.workspace, args.replicas, args.image,
                                                   ippool=args.ippool, volume_mounts=volume_mounts, volumes=volumes,
                                                   command=args.app_command, envs=envs, worker=args.worker,
                                                   resources=resources)
        app_yaml_file_path = os.path.join(APP_YAML_PATH, '{0}.yaml'.format(app_name))
        compress_files(compress_file_path, app_yaml_file_local_path, new_file_name='{0}.yaml'.format(app_name))
        app_yaml_file_path_list.append(app_yaml_file_path)

    node1_obj.remote_scp_put(compress_file_path, os.path.join(APP_YAML_PATH, compress_file_name))
    node1_obj.extract(os.path.join(APP_YAML_PATH, compress_file_name), APP_YAML_PATH)
    return app_yaml_file_path_list


@pytest.fixture(scope='session')
def appmatrix_yaml_file_path_list(node1_obj, app_name_list):
    logger.info('App image is {0}!'.format(args.image))
    appmatrix_yaml_file_path_list = []
    node1_obj.make_dir(APPMATRIX_YAML_PATH)
    compress_file_name = 'appmatrixes_yaml_{}.tar'.format(time_str())
    compress_file_path = os.path.join(LOCAL_TEMP_PATH, compress_file_name)
    for app_name in app_name_list:
        if args.app_type == 'nginx':
            volume_mounts = [{"alias": app_name, "mountPath": "/usr/share/nginx/html"}]
            volumes = [{"alias": app_name, "sourceName": app_name, "type": "apparafile"}]
        else:
            volume_mounts = None
            volumes = None
        envs = [{"name": "app_name", "value": app_name}]
        resources = {"cpu": args.app_cpu, "memory": args.app_memory * 1024 * 1024}
        appmetrix_yaml_file_local_path = create_appmatrix_yaml(app_name, args.workspace, args.replicas, args.image,
                                                   ippool=args.ippool, volume_mounts=volume_mounts, volumes=volumes,
                                                   command=args.app_command, envs=envs, worker=args.worker,
                                                   resources=resources)
        appmatrix_yaml_file_path = os.path.join(APPMATRIX_YAML_PATH, '{0}.yaml'.format(app_name))
        compress_files(compress_file_path, appmetrix_yaml_file_local_path, new_file_name='{0}.yaml'.format(app_name))
        appmatrix_yaml_file_path_list.append(appmatrix_yaml_file_path)

    node1_obj.remote_scp_put(compress_file_path, os.path.join(APPMATRIX_YAML_PATH, compress_file_name))
    node1_obj.extract(os.path.join(APPMATRIX_YAML_PATH, compress_file_name), APPMATRIX_YAML_PATH)
    return appmatrix_yaml_file_path_list


@pytest.fixture(scope='session')
def forward_yaml_file_path_list(node1_obj, app_name_list):
    forward_yaml_file_path_list = []
    node1_obj.make_dir(FORWARD_YAML_PATH)
    compress_file_name = 'forwards_yaml_{}.tar'.format(time_str())
    compress_file_path = os.path.join(LOCAL_TEMP_PATH, compress_file_name)
    for app_name in app_name_list:
        forward_yaml_file_loocal_name = create_forward_yaml(app_name, args.workspace, 80)
        forward_yaml_file_path = os.path.join(FORWARD_YAML_PATH, '{0}.yaml'.format(app_name))
        compress_files(compress_file_path, forward_yaml_file_loocal_name, new_file_name='{0}.yaml'.format(app_name))
        forward_yaml_file_path_list.append(forward_yaml_file_path)

    node1_obj.remote_scp_put(compress_file_path, os.path.join(FORWARD_YAML_PATH, compress_file_name))
    node1_obj.extract(os.path.join(FORWARD_YAML_PATH, compress_file_name), FORWARD_YAML_PATH)
    return forward_yaml_file_path_list


def test_boxs_failover(node1_obj):
    logger.info('Test start!')
    boxs_info = node1_obj.get_boxs_info_by_workspace(args.workspace)
    box_nums_before = len(boxs_info)
    if box_nums_before == 0:
        raise Exception('Workspace {0} have not box!'.format(args.workspace))
    boxs_name_before = []
    start_time = datetime.datetime.now()
    pool = ThreadPoolExecutor(max_workers=5)
    futures = []
    for box_info in boxs_info:
        boxs_name_before.append(box_info['meta']['name'])
        futures.append(pool.submit(node1_obj.delete_box, box_info['meta']['name'], box_info['meta']['workspace']))
    pool.shutdown()
    for future in as_completed(futures):
        future.result()

    node1_obj.is_boxs_not_exist_by_name(boxs_name_before)
    end_time = datetime.datetime.now()
    take_time = end_time - start_time
    logger.info('{0} boxs were deleted total take time: {1}'.format(box_nums_before, take_time))

    node1_obj.is_boxs_running(args.workspace)
    node1_obj.is_boxsets_running(args.workspace)
    end_time = datetime.datetime.now()
    take_time = end_time - start_time
    logger.info('{0} boxs failover total take time: {1}'.format(box_nums_before, take_time))

    boxs_info_after = node1_obj.get_boxs_info_by_workspace(args.workspace)
    box_nums_after = len(boxs_info_after)
    assert box_nums_after == box_nums_before
    logger.info('Boxs number are right!')


def test_create_apparafile(node1_obj, apparafile_yaml_file_path_list):
    logger.info('Test start!')
    logger.info('Create apparafile start!')
    pool = ThreadPoolExecutor(max_workers=5)
    futures = []
    for apparafile_yaml_file_path in apparafile_yaml_file_path_list:
        futures.append(pool.submit(node1_obj.nbctl_create, apparafile_yaml_file_path))
    pool.shutdown()
    for future in as_completed(futures):
        future.result()
    logger.info('Create apparafile done!')


def test_create_apps(node1_obj, app_yaml_file_path_list):
    logger.info('Test start!')
    logger.info('Create apps start!')
    start_time = datetime.datetime.now()
    pool = ThreadPoolExecutor(max_workers=5)
    futures = []
    for app_yaml_file_path in app_yaml_file_path_list:
        futures.append(pool.submit(node1_obj.nbctl_create, app_yaml_file_path))
    pool.shutdown()
    for future in as_completed(futures):
        future.result()
    node1_obj.is_boxs_running(args.workspace)
    node1_obj.is_apps_running(args.workspace)
    end_time = datetime.datetime.now()
    create_app_time = end_time - start_time
    logger.info('Create apps done!')
    logger.info('Create {0} replicas app take time: {1}'.format(args.replicas, create_app_time))


def test_create_appmatrixes(node1_obj, appmatrix_yaml_file_path_list):
    logger.info('Test start!')
    logger.info('Create appmatrixes start!')
    start_time = datetime.datetime.now()
    pool = ThreadPoolExecutor(max_workers=5)
    futures = []
    for appmatrix_yaml_file_path in appmatrix_yaml_file_path_list:
        futures.append(pool.submit(node1_obj.nbctl_create, appmatrix_yaml_file_path))
    pool.shutdown()
    for future in as_completed(futures):
        future.result()
    node1_obj.is_boxs_running(args.workspace)
    node1_obj.is_appmatrixes_running(args.workspace)
    end_time = datetime.datetime.now()
    create_appmatrixes_time = end_time - start_time
    logger.info('Create appmatrixes done!')
    logger.info('Create {0} replicas app take time: {1}'.format(args.replicas, create_appmatrixes_time))


def test_expose_apps(node1_obj, app_name_list, forward_yaml_file_path_list):
    logger.info('Test start!')
    logger.info('Expose apps start!')
    pool = ThreadPoolExecutor(max_workers=5)
    futures = []
    for forward_yaml_file_path in forward_yaml_file_path_list:
        futures.append(pool.submit(node1_obj.nbctl_create, forward_yaml_file_path))
    pool.shutdown()
    for future in as_completed(futures):
        future.result()

    node1_obj.is_forwards_ok(forwards_name=app_name_list)
    logger.info('Expose apps done!')


def test_access_apps(node1_obj, app_name_list):
    logger.info('Test start!')
    start_time = datetime.datetime.now()
    pool = ThreadPoolExecutor(max_workers=100)
    futures = []
    for forward_info in node1_obj.get_forwards_info_by_workspace(args.workspace):
        if forward_info['spec']['selector']['application-name'] in app_name_list:
            futures.append(pool.submit(is_nginx_working, args.ip, forward_info))
    pool.shutdown()
    for future in as_completed(futures):
        future.result()
    end_time = datetime.datetime.now()
    take_time = end_time - start_time
    logger.info('Access {0} nginx take time: {1}!'.format(args.concurrent, take_time))


def test_delete_apps(node1_obj, app_name_list):
    logger.info('Test start!')
    start_time = datetime.datetime.now()
    pool = ThreadPoolExecutor(max_workers=5)
    futures = []
    for app_name in app_name_list:
        futures.append(pool.submit(node1_obj.delete_app, app_name, args.workspace))
    pool.shutdown()
    for future in as_completed(futures):
        future.result()

    node1_obj.is_apps_not_exist_by_name(app_name_list)
    end_time = datetime.datetime.now()
    delete_app_time = end_time - start_time
    logger.info('Delete {0} replicas {1} app take time: {2}'.format(args.replicas, args.concurrent, delete_app_time))

    # cmd = 'rm -rf {0}'.format(APP_YAML_PATH)
    # rtn_dict = node1_obj.run_cmd(cmd)
    # if rtn_dict['rc'] == 0 and rtn_dict['stderr'] == '':
    #     logger.info('Clear all app yaml {0} done!'.format(APP_YAML_PATH))
    # else:
    #     logger.error(rtn_dict)
    #     raise Exception('Clear all app yaml {0} fail!'.format(APP_YAML_PATH))


def test_delete_appmatrixes(node1_obj, app_name_list):
    logger.info('Test start!')
    logger.info('Delete appmatrixes start!')
    start_time = datetime.datetime.now()
    pool = ThreadPoolExecutor(max_workers=5)
    futures = []
    for appmarix_name in app_name_list:
        futures.append(pool.submit(node1_obj.delete_appmatrix, appmarix_name, args.workspace))
    pool.shutdown()
    for future in as_completed(futures):
        future.result()

    node1_obj.is_appmatrixes_not_exist_by_name(app_name_list)
    end_time = datetime.datetime.now()
    delete_appmatrix_time = end_time - start_time
    logger.info('Delete {} appmatrixes take time: {}'.format(args.concurrent, delete_appmatrix_time))


def test_delete_forward(node1_obj, app_name_list):
    for app_name in app_name_list:
        node1_obj.delete_forward(app_name, args.workspace)
    node1_obj.is_forwards_not_exist_by_name(app_name_list)
    # cmd = 'rm -rf {0}'.format(FORWARD_YAML_PATH)
    # rtn_dict = node1_obj.run_cmd(cmd)
    # if rtn_dict['rc'] == 0 and rtn_dict['stderr'] == '':
    #     logger.info('Clear all forward yaml {0} done!'.format(FORWARD_YAML_PATH))
    # else:
    #     logger.error(rtn_dict)
    #     raise Exception('Clear all forward yaml {0} fail!'.format(FORWARD_YAML_PATH))


def test_delete_apparafile(node1_obj, app_name_list):
    for app_name in app_name_list:
        node1_obj.delete_apparafile(app_name, args.workspace)
    node1_obj.is_apparafiles_not_exist_by_name(app_name_list)
    # cmd = 'rm -rf {0}'.format(APPARAFILE_YAML_PATH)
    # rtn_dict = node1_obj.run_cmd(cmd)
    # if rtn_dict['rc'] == 0 and rtn_dict['stderr'] == '':
    #     logger.info('Clear all apparafile yaml {0} done!'.format(FORWARD_YAML_PATH))
    # else:
    #     logger.error(rtn_dict)
    #     raise Exception('Clear all apparafile yaml {0} fail!'.format(FORWARD_YAML_PATH))


def test_app_scale(node1_obj):
    logger.info('Test start!')
    replica = random.randint(0, 100)
    app_yaml_data = node1_obj.update_replica(args.app, args.workspace, replica)
    app_yaml_file_local_path = dump_yaml_data(app_yaml_data)
    node1_obj.make_dir(APP_YAML_PATH)
    app_yaml_file_path = os.path.join(APP_YAML_PATH, '{0}.yaml'.format(args.app))
    node1_obj.remote_scp_put(app_yaml_file_local_path, app_yaml_file_path)
    node1_obj.nbctl_update(app_yaml_file_path)
    node1_obj.is_app_scale_done(args.app, replica)
    node1_obj.is_apps_running(args.workspace)
