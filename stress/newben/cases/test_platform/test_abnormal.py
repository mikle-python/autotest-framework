import pytest
import random
import os
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.times import sleep
from libs.log_obj import LogObj
from libs.vmware_obj import VMwareObj
from libs.hwcloud_obj import HWCloudObj
from settings.newben_settings import INSTALL_YAML_PATH, NB_PROCESSES
from common.common import is_ping_ok, dump_yaml_data
from stress.newben.common.common import check_health, is_nginx_working_tmp
from stress.newben.common.node_obj import NodeObj
from stress import arguments


logger = LogObj().get_logger()
args = arguments.parse_arg()


@pytest.fixture(scope='session')
def platform_obj():
    if args.platform == 'vmware':
        return VMwareObj(args.vc_ip, args.vc_user, args.vc_pwd, args.vc_port)
    elif args.platform == 'huaweicloud':
        return HWCloudObj(args.access_key, args.secret_key, args.region)
    else:
        raise Exception('Not support platform {0}'.format(args.platform))


@pytest.fixture(scope='session')
def nodes_ip(node1_obj):
    return node1_obj.nodes_ip


@pytest.fixture(scope='session')
def workersets_name(node1_obj):
    return node1_obj.workersets_name


@pytest.fixture(scope='function')
def random_nodes_ip(nodes_ip):
    if args.all_nodes:
        min_nodes_ip = len(nodes_ip)
    else:
        min_nodes_ip = args.min

    if args.max == 0:
        max_nodes_ip = len(nodes_ip)
    else:
        max_nodes_ip = args.max
    return random.sample(nodes_ip, random.randint(min_nodes_ip, max_nodes_ip))


@pytest.fixture(scope='function')
def random_workersets_name(node1_obj, random_nodes_ip, etcd_nodes_ip):
    random_workersets_name = []
    for node_ip in random_nodes_ip:
        if node_ip not in etcd_nodes_ip:
            workerset_info = node1_obj.get_workerset_info_by_ip(node_ip)
            random_workersets_name.append(workerset_info['meta']['name'])
    return random_workersets_name


@pytest.fixture(scope='session')
def install_yaml_path(node1_obj):
    for ip in list(set(args.add_nodes_ip).difference(set(node1_obj.install_nodes_ip))):
        node_info = dict()
        node_info['address'] = ip
        node_info['modules'] = ["bootstrap", "agent", "proxy"]
        node_info['password'] = "password"
        node_info['port'] = "22"
        node_info['user'] = "root"
        node1_obj.install_config_data['nodes'].append(node_info)
    node1_obj.make_dir(INSTALL_YAML_PATH)
    install_yaml_local_path = dump_yaml_data(node1_obj.install_config_data)
    install_yaml_path = os.path.join(INSTALL_YAML_PATH, 'install.yaml')
    node1_obj.remote_scp_put(install_yaml_local_path, install_yaml_path)
    return install_yaml_path


@pytest.fixture(scope='function')
def random_add_nodes_ip():
    if args.add_nodes_ip:
        return random.sample(args.add_nodes_ip, random.randint(args.min, len(args.add_nodes_ip)))
    else:
        return args.add_nodes_ip


@pytest.fixture(scope='function')
def random_services_info(random_nodes_ip):
    random_services_info = dict()
    for node_ip in random_nodes_ip:
        if args.all_services:
            min_services = len(NB_PROCESSES)
        else:
            min_services = 1
        random_services = random.sample(NB_PROCESSES, random.randint(min_services, len(NB_PROCESSES)))
        random_services_info[node_ip] = random_services
    return random_services_info


@pytest.fixture(scope='session', autouse=True)
def check_before(node1_obj, etcd_node_obj):
    logger.info('Check health before test!')
    check_health(node1_obj, etcd_node_obj, single=args.single)


@pytest.fixture(scope='function', autouse=True)
def check(node1_obj, etcd_node_obj, random_add_nodes_ip):
    logger.info('Record box quantity before test!')
    boxs_info_before = node1_obj.boxs_info
    box_nums_before = len(boxs_info_before)
    yield
    logger.info('Check health after test!')
    check_health(node1_obj, etcd_node_obj, add_nodes_ip=random_add_nodes_ip, single=args.single)
    logger.info('Compare the box quantity before and after!')
    boxs_info_after = node1_obj.boxs_info
    box_nums_after = len(boxs_info_after)
    assert box_nums_after == box_nums_before
    logger.info('Boxs number are right!')


@pytest.fixture(scope='session')
def ceph_monitor_ip():
    return args.ceph_monitor_ip


@pytest.fixture(scope='session')
def ceph_nodes_ip():
    return args.ceph_nodes_ip


@pytest.fixture(scope='function')
def random_ceph_nodes_ip(ceph_nodes_ip):
    if args.all_nodes:
        min_nodes_ip = len(ceph_nodes_ip)
    else:
        min_nodes_ip = args.min
    return random.sample(ceph_nodes_ip, random.randint(min_nodes_ip, len(ceph_nodes_ip)))


@pytest.mark.parametrize("power_option", args.power_options)
def test_power_node(platform_obj, random_nodes_ip, random_workersets_name, workersets_name, node1_obj, nodes_ip,
                    etcd_info, power_option):
    test_power_node.__doc__ = 'Test start, power node ips: {0}, power option is {1}!'.format(random_nodes_ip,
                                                                                             power_option)
    logger.info(test_power_node.__doc__)
    logger.debug('Power node ips: {0}, power option is {1}!'.format(random_nodes_ip, power_option))
    vm_names = [platform_obj.get_vm_name_by_ip(node_ip) for node_ip in random_nodes_ip]

    before_running_boxes = node1_obj.running_boxes_quantity
    platform_obj.batch_opreate_vms(vm_names, power_option)

    if power_option in ['poweroff', 'shutdown', 'suspend']:
        if len(random_nodes_ip) < len(nodes_ip) and node1_obj.ip not in random_nodes_ip and \
                etcd_info['ip'] not in random_nodes_ip:
            logger.info('Power nodes number less than all nodes number, so check box failover to other workerset!')
            node1_obj.is_workersets_disconnect(workersets_name=random_workersets_name)
            node1_obj.is_workers_disconnect(workers_name=random_workersets_name)
            not_power_nodes = list(set(workersets_name).difference(set(random_workersets_name)))
            node1_obj.is_workersets_running(workersets_name=not_power_nodes)
            node1_obj.is_workers_running(workers_name=not_power_nodes)
            node1_obj.is_boxsets_running()
            node1_obj.is_apps_running()
            logger.info('Check running box number during test!')
            after_running_boxes = node1_obj.running_boxes_quantity
            logger.info('Running box number is {0}'.format(after_running_boxes))
            assert before_running_boxes == after_running_boxes
            logger.debug('Check running box number done during test, box number is {0}!'.format(after_running_boxes))
        sleep(5)
        platform_obj.batch_opreate_vms(vm_names, 'poweron')

    for ip in random_nodes_ip:
        is_ping_ok(ip)


def test_force_reboot_node(nodes_ip, random_nodes_ip):
    test_force_reboot_node.__doc__ = 'Test start, force reboot node ips: {0}'.format(random_nodes_ip)
    logger.info(test_force_reboot_node.__doc__)
    not_power_nodes_ip = list(set(nodes_ip).difference(set(random_nodes_ip)))
    logger.info('Force reboot node are {0}, not reboot node are {1}'.format(random_nodes_ip, not_power_nodes_ip))
    pool = ThreadPoolExecutor(max_workers=10)
    futures = []
    for ip in random_nodes_ip:
        node_obj = NodeObj(ip, args.sys_user, args.sys_pwd)
        futures.append(pool.submit(node_obj.force_reboot))
    pool.shutdown()
    for future in as_completed(futures):
        future.result()

    for ip in random_nodes_ip:
        is_ping_ok(ip)


def test_disconnect_network(platform_obj, random_nodes_ip, random_workersets_name, workersets_name, node1_obj,
                            nodes_ip, etcd_info):
    test_disconnect_network.__doc__ = 'Test start, random disconnect network ips: {0}'.format(random_nodes_ip)
    logger.info(test_disconnect_network.__doc__)
    logger.debug('Random disconnect network ips: {0}'.format(random_nodes_ip))
    before_running_boxes = node1_obj.running_boxes_quantity
    pool = ThreadPoolExecutor(max_workers=10)
    futures = []
    vm_name_list = []
    for node_ip in random_nodes_ip:
        vm_obj = platform_obj.get_vm_obj_by_ip(node_ip)
        vm_name_list.append(vm_obj.name)
        futures.append(pool.submit(platform_obj.update_nic_state, vm_obj, 'Network adapter 1', 'disconnect'))
    pool.shutdown()

    for future in as_completed(futures):
        future.result()

    if len(random_nodes_ip) < len(nodes_ip) and node1_obj.ip not in random_nodes_ip and etcd_info['ip'] \
            not in random_nodes_ip:
        logger.info('Disconnect network nodes number less than all nodes number, '
                    'so check box failover to other workerset!')
        node1_obj.is_workersets_disconnect(workersets_name=random_workersets_name)
        node1_obj.is_workers_disconnect(workers_name=random_workersets_name)
        not_disconnect_nodes = list(set(workersets_name).difference(set(random_workersets_name)))
        node1_obj.is_workersets_running(workersets_name=not_disconnect_nodes)
        node1_obj.is_workers_running(workers_name=not_disconnect_nodes)
        node1_obj.is_boxsets_running()
        node1_obj.is_apps_running()
        logger.info('Check running box number during test!')
        after_running_boxes = node1_obj.running_boxes_quantity
        logger.info('Running box number is {0}'.format(after_running_boxes))
        assert before_running_boxes == after_running_boxes
        logger.debug('Check running box number done during test, box number is {0}!'.format(after_running_boxes))
    sleep(5)
    pool = ThreadPoolExecutor(max_workers=10)
    futures = []
    for vm_name in vm_name_list:
        vm_obj = platform_obj.get_vm_obj_by_name(vm_name)
        futures.append(pool.submit(platform_obj.update_nic_state, vm_obj, 'Network adapter 1', 'connect'))
    pool.shutdown()
    for future in as_completed(futures):
        future.result()

    for node_ip in random_nodes_ip:
        is_ping_ok(node_ip)


def test_kill_services(random_services_info):
    test_kill_services.__doc__ = 'Test start, Kill services info are {0}'.format(random_services_info)
    logger.info(test_kill_services.__doc__)
    pool = ThreadPoolExecutor(max_workers=5)
    futures = []
    for node_ip, random_services in random_services_info.items():
        node_obj = NodeObj(node_ip, args.sys_user, args.sys_pwd)
        for service in random_services:
            futures.append(pool.submit(node_obj.kill_service_by_name, service))
    pool.shutdown()
    for future in as_completed(futures):
        future.result()


def test_maintain_workerset(node1_obj, nodes_ip, random_nodes_ip, random_workersets_name, workersets_name,
                            etcd_nodes_ip):
    random_maintain_nodes_ip = list(set(random_nodes_ip).difference(set(etcd_nodes_ip)))
    test_maintain_workerset.__doc__ = 'Test start, random maintain workersets ip: {0}'.format(random_maintain_nodes_ip)
    logger.info(test_maintain_workerset.__doc__)
    before_running_boxes = node1_obj.running_boxes_quantity
    pool = ThreadPoolExecutor(max_workers=10)
    futures = []
    for node_ip in random_maintain_nodes_ip:
        workerset_info = node1_obj.get_workerset_info_by_ip(node_ip)
        futures.append(pool.submit(node1_obj.maintain_workerset, workerset_info['meta']['name']))
    pool.shutdown()
    for future in as_completed(futures):
        future.result()

    for node_ip in random_maintain_nodes_ip:
        node1_obj.is_enter_maintain_by_ip(node_ip)

    if len(random_maintain_nodes_ip) < len(nodes_ip) and node1_obj.ip not in random_maintain_nodes_ip:
        logger.info('Maintain nodes number less than all nodes number, so check box failover to other workerset!')
        not_maintain_nodes = list(set(workersets_name).difference(set(random_workersets_name)))
        node1_obj.is_workersets_running(workersets_name=not_maintain_nodes)
        node1_obj.is_workers_running(workers_name=not_maintain_nodes)
        node1_obj.is_boxsets_running()
        node1_obj.is_apps_running()
        logger.info('Check running box number during test!')
        after_running_boxes = node1_obj.running_boxes_quantity
        logger.info('Running box number is {0}'.format(after_running_boxes))
        assert before_running_boxes == after_running_boxes
        logger.info('Check running box number done during test, box number is {0}!'.format(after_running_boxes))

    pool = ThreadPoolExecutor(max_workers=10)
    futures = []
    for node_ip in random_maintain_nodes_ip:
        workerset_info = node1_obj.get_workerset_info_by_ip(node_ip)
        futures.append(pool.submit(node1_obj.exit_maintain_workerset, workerset_info['meta']['name']))
    pool.shutdown()
    for future in as_completed(futures):
        future.result()

    for node_ip in random_maintain_nodes_ip:
        node1_obj.is_exit_maintain_by_ip(node_ip)


def test_disconnect_share_storage(node1_obj, platform_obj):
    pool = ThreadPoolExecutor(max_workers=10)
    futures = []
    vm_name_list = []
    for share_storage_vm in args.share_storage_vms:
        vm_obj = platform_obj.get_vm_obj_by_name(share_storage_vm)
        vm_name_list.append(vm_obj.name)
        futures.append(pool.submit(platform_obj.poweroff_vm, vm_obj))
    pool.shutdown()

    pool = ThreadPoolExecutor(max_workers=10)
    futures = []
    vm_name_list = []
    for share_storage_vm in args.share_storage_vms:
        vm_obj = platform_obj.get_vm_obj_by_name(share_storage_vm)
        vm_name_list.append(vm_obj.name)
        futures.append(pool.submit(platform_obj.poweron_vm, vm_obj))
    pool.shutdown()


def test_add_delete_node(node1_obj, etcd_node_obj, install_yaml_path, random_add_nodes_ip):
    test_add_delete_node.__doc__ = 'Test start, add delete nodes are {0}'.format(random_add_nodes_ip)
    logger.info(test_add_delete_node.__doc__)
    start_time = datetime.datetime.now()
    node1_obj.update_node('add', install_yaml_path, random_add_nodes_ip)
    node1_obj.is_add_nodes_succeeded(random_add_nodes_ip)
    end_time = datetime.datetime.now()
    add_time = end_time - start_time
    logger.info('Add {0} nodes take time: {1}!'.format(len(random_add_nodes_ip), add_time))
    check_health(node1_obj, etcd_node_obj, add_nodes_ip=random_add_nodes_ip)
    if not args.not_delete:
        start_time = datetime.datetime.now()
        node1_obj.update_node('delete', install_yaml_path, random_add_nodes_ip)
        node1_obj.is_delete_nodes_succeeded(random_add_nodes_ip)
        end_time = datetime.datetime.now()
        delete_time = end_time - start_time
        logger.info('Delete {0} nodes take time: {1}!'.format(len(random_add_nodes_ip), delete_time))


def test_no_space(random_nodes_ip):
    test_no_space.__doc__ = 'Test start,no space ips: {0}'.format(random_nodes_ip)
    logger.info(test_no_space.__doc__)
    logger.debug('No space node ips: {0}'.format(random_nodes_ip))
    device = 'zero'
    file_path = "/mnt"
    count = '1024'
    bs = '2MB'

    pool_dd = ThreadPoolExecutor(max_workers=5)
    futures_dd = []
    for node_ip in random_nodes_ip:
        node_obj = NodeObj(node_ip, args.sys_user, args.sys_pwd)
        futures_dd.append(pool_dd.submit(node_obj.dd_file_until_no_space, device, file_path, count, bs))
    pool_dd.shutdown()
    for future in as_completed(futures_dd):
        future.result()
    sleep(60)

    remove_path = file_path + "/dd*"
    pool_remove = ThreadPoolExecutor(max_workers=5)
    futures_remove = []
    for node_ip in random_nodes_ip:
        node_obj = NodeObj(node_ip, args.sys_user, args.sys_pwd)
        futures_remove.append(pool_remove.submit(node_obj.remove_file, remove_path))
    pool_remove.shutdown()
    for future in as_completed(futures_remove):
        future.result()


# @pytest.mark.parametrize("power_option", ['poweroff', 'reboot', 'shutdown', 'reset', 'suspend'])
@pytest.mark.parametrize("power_option", ['poweroff'])
def test_power_ceph_node(platform_obj, ceph_monitor_ip, random_ceph_nodes_ip, node1_obj, power_option):
    test_power_ceph_node.__doc__ = 'Test start, power ceph node ips: {0}, power option is {1}!'\
        .format(random_ceph_nodes_ip, power_option)
    logger.info(test_power_ceph_node.__doc__)
    logger.info('check sp before test!')
    NodeObj(ceph_monitor_ip).is_ceph_health_ok()
    node1_obj.is_storagepool_available(['CephRBD', 'CephFS'])

    logger.debug('Power ceph node ips: {0}, power option is {1}!'.format(random_ceph_nodes_ip, power_option))
    vm_names = [platform_obj.get_vm_name_by_ip(node_ip) for node_ip in random_ceph_nodes_ip]

    platform_obj.batch_opreate_vms(vm_names, power_option)

    try:
        if power_option in ['poweroff', 'shutdown', 'suspend']:
            logger.debug('=========================================')
            if len(random_ceph_nodes_ip) < 2 and ceph_monitor_ip not in random_ceph_nodes_ip and node1_obj.ip not in \
                    random_ceph_nodes_ip:
                logger.info("Access the nginx that use ceph storage")
                for forward_info in node1_obj.get_forwards_info_by_workspace(args.workspace):
                    is_nginx_working_tmp(args.ip, forward_info)
            sleep(60)
            platform_obj.batch_opreate_vms(vm_names, 'poweron')
        sleep(60)
        for ip in random_ceph_nodes_ip:
            is_ping_ok(ip)

        NodeObj(ceph_monitor_ip).is_ceph_health_ok()
        logger.info('check sp after test!')
        node1_obj.is_storagepool_available(['CephRBD', 'CephFS'])
    except Exception as e:
        logger.debug('Exception occured, error is {0}'.format(e))
        raise e
