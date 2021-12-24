import pytest
import random
from libs.log_obj import LogObj
from stress import arguments
from concurrent.futures import ThreadPoolExecutor, as_completed
from common.common import is_ping_ok
from utils.times import sleep
from libs.vmware_obj import VMwareObj
from libs.hwcloud_obj import HWCloudObj
from stress.ecos.common.node_obj import NodeObj
from stress.ecos.common.common import check_health
from settings.ecos_settings import ALL_PROCESSES, ALL_COMPONENTS, PAAS_COMPONENTS


logger = LogObj().get_logger()
args = arguments.parse_arg()


@pytest.fixture(scope='function', autouse=True)
def check(node1_obj):
    logger.info('Check health before test!')
    check_health(node1_obj)
    yield
    logger.info('Check health after test!')
    check_health(node1_obj)


@pytest.fixture(scope='session')
def nodes_ip(node1_obj):
    return node1_obj.nodes_ip


@pytest.fixture(scope='session')
def master_nodes_ip(node1_obj):
    return node1_obj.master_nodes_ip


@pytest.fixture(scope='function')
def random_nodes_ip(nodes_ip, master_nodes_ip):
    if args.power_master:
        return random.sample(master_nodes_ip, random.randint(1, len(master_nodes_ip)))
    else:
        return random.sample(nodes_ip, random.randint(1, len(nodes_ip)))


@pytest.fixture(scope='session')
def platform_obj():
    if args.platform == 'vmware':
        return VMwareObj(args.vc_ip, args.vc_user, args.vc_pwd, args.vc_port)
    elif args.platform == 'huaweicloud':
        return HWCloudObj(args.access_key, args.secret_key, args.region)
    else:
        raise Exception('Not support platform {0}'.format(args.platform))


@pytest.fixture(scope='function')
def random_processes_info(random_nodes_ip):
    random_processes_info = dict()
    for node_ip in random_nodes_ip:
        random_processes = random.sample(ALL_PROCESSES, random.randint(1, len(ALL_PROCESSES)))
        random_processes_info[node_ip] = random_processes
    return random_processes_info


@pytest.fixture(scope='function')
def random_components_info(random_nodes_ip):
    random_components_info = dict()
    for node_ip in random_nodes_ip:
        random_components = random.sample(ALL_COMPONENTS, random.randint(1, len(ALL_COMPONENTS)))
        random_components_info[node_ip] = random_components
    return random_components_info


@pytest.fixture(scope='function')
def random_pods_info(node1_obj, random_nodes_ip):
    random_pods_info = dict()

    # 随机获取组件名称 (一个~多个)
    random_components = random.sample(ALL_COMPONENTS, random.randint(1, len(ALL_COMPONENTS)))

    # 初始化组件信息列表，通过组件名称，获取组件相关信息
    components_info = []
    for pod in node1_obj.pods_info:
        for component in random_components:
            if component in pod['metadata']['name']:
                components_info.append(pod)

    # 初始化节点组件字典，通过节点，获取节点下的组件信息
    for component in components_info:
        node_ip = component['status']['hostIP']
        if node_ip not in random_nodes_ip:
            continue
        if node_ip in random_pods_info.keys():
            if {component['metadata']['name']: component['metadata']['namespace']} not in random_pods_info[node_ip]:
                random_pods_info[node_ip].append({component['metadata']['name']: component['metadata']['namespace']})
        else:
            random_pods_info[node_ip] = [{component['metadata']['name']: component['metadata']['namespace']}]

    return random_pods_info


@pytest.fixture(scope='session')
def components():
    return args.reboot_components.strip().split(",")


@pytest.fixture(scope='function')
def reboot_components(components, node1_obj):
    reboot_components = list(set(PAAS_COMPONENTS).intersection(components))
    if not reboot_components:
        raise Exception("Not support {}, please confirm it again !".format(components))

    components_info = []
    for pod in node1_obj.pods_info:
        for component in reboot_components:
            if component in pod['metadata']['name']:
                components_info.append(pod)
    return reboot_components


@pytest.mark.parametrize("power_option", ['poweroff', 'reset', 'suspend', 'shutdown'])
def test_power_node(platform_obj, random_nodes_ip, node1_obj, master_nodes_ip, power_option):
    test_power_node.__doc__ = 'Test start, power node ips: {0}, power option is {1}!'.format(random_nodes_ip,
                                                                                             power_option)
    logger.info(test_power_node.__doc__)
    logger.debug('Power node ips: {0}, power option is {1}!'.format(random_nodes_ip, power_option))
    vm_names = [platform_obj.get_vm_name_by_ip(node_ip) for node_ip in random_nodes_ip]
    platform_obj.batch_opreate_vms(vm_names, power_option)

    if power_option in ['poweroff', 'shutdown', 'suspend']:
        exist_master_ips = set(master_nodes_ip).difference(set(random_nodes_ip))
        if len(exist_master_ips) > 1:
            logger.info('Exist running master node, so check pod failover to other node!')
            if args.ip in random_nodes_ip:
                NodeObj(random.choice(list(exist_master_ips)), args.sys_user, args.sys_pwd).is_pods_running()
            else:
                node1_obj.is_pods_running()
        sleep(random.randint(5, 3600))
        platform_obj.batch_opreate_vms(vm_names, 'poweron')


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


def test_disconnect_network(platform_obj, random_nodes_ip, node1_obj, master_nodes_ip):
    test_disconnect_network.__doc__ = 'Test start, random disconnect network ips: {0}'.format(random_nodes_ip)
    logger.info(test_disconnect_network.__doc__)
    logger.debug('Random disconnect network ips: {0}'.format(random_nodes_ip))
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

    exist_master_ips = set(master_nodes_ip).difference(set(random_nodes_ip))
    if len(exist_master_ips) > 1:
        logger.info('Exist running master node, so check pod failover to other node!')
        if args.ip in random_nodes_ip:
            NodeObj(random.choice(list(exist_master_ips)), args.sys_user, args.sys_pwd).is_pods_running()
        else:
            node1_obj.is_pods_running()

    sleep(10)
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


def test_pid_kill_components(random_processes_info):
    test_pid_kill_components.__doc__ = 'Test start, Kill services info are {0}'.format(random_processes_info)
    logger.info(test_pid_kill_components.__doc__)
    pool = ThreadPoolExecutor(max_workers=5)
    futures = []
    for node_ip, random_processes in random_processes_info.items():
        node_obj = NodeObj(node_ip, args.sys_user, args.sys_pwd)
        for random_process in random_processes:
            futures.append(pool.submit(node_obj.kill_service_by_name, random_process))
    pool.shutdown()
    for future in as_completed(futures):
        future.result()


def test_docker_kill_components(random_components_info):
    test_docker_kill_components.__doc__ = 'Test start, Kill components info are {0}'.format(random_components_info)
    logger.info(test_docker_kill_components.__doc__)
    pool = ThreadPoolExecutor(max_workers=5)
    futures = []
    for node_ip, random_components in random_components_info.items():
        node_obj = NodeObj(node_ip, args.sys_user, args.sys_pwd)
        for random_component in random_components:
            futures.append(pool.submit(node_obj.dockers_kill, random_component))
    pool.shutdown()
    for future in as_completed(futures):
        future.result()


def test_force_delete_pods(random_pods_info, node1_obj):
    test_force_delete_pods.__doc__ = 'Test start, Delete pods info are {0}'.format(random_pods_info)
    logger.info(test_force_delete_pods.__doc__)
    pool = ThreadPoolExecutor(max_workers=5)
    futures = []
    for _, random_pods in random_pods_info.items():
        for random_pod in random_pods:
            futures.append(pool.submit(node1_obj.delete_pod, list(random_pod.values())[-1],
                                       list(random_pod.keys())[0], True))
    pool.shutdown()
    for future in as_completed(futures):
        future.result()


def test_grace_period_delete_pods(random_pods_info, node1_obj):
    test_grace_period_delete_pods.__doc__ = 'Test start, Delete pods info are {0}'.format(random_pods_info)
    logger.info(test_grace_period_delete_pods.__doc__)
    pool = ThreadPoolExecutor(max_workers=5)
    futures = []
    for _, random_pods in random_pods_info.items():
        for random_pod in random_pods:
            futures.append(pool.submit(node1_obj.delete_pod, list(random_pod.values())[-1],
                                       list(random_pod.keys())[0], False))
    pool.shutdown()
    for future in as_completed(futures):
        future.result()


def test_reboot_components(reboot_components, node1_obj):
    test_reboot_components.__doc__ = 'Test reboot components, reboot info are {0}'.format(reboot_components)
    logger.info(test_reboot_components.__doc__)
    pool = ThreadPoolExecutor(max_workers=5)
    futures = []
    for reboot_component in reboot_components:
        futures.append(pool.submit(node1_obj.delete_pod, reboot_component['metadata']['name'],
                                   reboot_component['metadata']['namespace'], False))
    pool.shutdown()
    for future in as_completed(futures):
        future.result()
