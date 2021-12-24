import pytest
from concurrent.futures import ThreadPoolExecutor, as_completed
from libs.log_obj import LogObj
from stress import arguments
from settings.newben_settings import NB_DOCKERS, SEAM_PROCESS
from stress.newben.common.node_obj import NodeObj
from stress.newben.common.common import check_health
from prettytable import PrettyTable
from libs.etcd_obj import EtcdObj


logger = LogObj().get_logger()
args = arguments.parse_arg()


@pytest.fixture(scope='session')
def etcd_obj(etcd_info):
    return EtcdObj(etcd_info['ip'], etcd_info['port'])


def print_generator_value(generator):
    for info in generator:
        logger.debug(info)


def test_check_health(node1_obj, etcd_node_obj):
    check_health(node1_obj, etcd_node_obj, args.workspace, single=args.single)


def test_check_version(node1_obj, etcd_info):
    for node_ip in node1_obj.nodes_ip:
        tb = PrettyTable()
        tb.field_names = ['Node', 'ServiceName', 'gitVersion', 'gitCommit', 'buildDate', 'goVersion', 'compiler',
                          'platform']
        if node_ip != etcd_info['ip']:
            node_obj = NodeObj(node_ip, node1_obj.username, node1_obj.password, node1_obj.port)
            dockers_name = node_obj.dockers_name
            for docker_name in NB_DOCKERS:
                if docker_name in dockers_name:
                    version_info = node_obj.get_docker_version(docker_name)
                elif 'seam' in docker_name:
                    version_info = node_obj.get_binary_version(SEAM_PROCESS)
                else:
                    continue
                tb.add_row([
                    node_ip,
                    docker_name,
                    version_info['gitVersion'],
                    version_info['gitCommit'],
                    version_info['buildDate'],
                    version_info['goVersion'],
                    version_info['compiler'],
                    version_info['platform']
                ])
            logger.info('{0}\n'.format(tb))


def test_watch(node1_obj, etcd_obj):
    if args.kind == 'workermetrics':
        controller_kind = 'worker'
    else:
        controller_kind = args.kind
    controllers_name = node1_obj.get_controllers_name(controller_kind)
    pool = ThreadPoolExecutor(max_workers=10)
    futures = []
    for controller_name in controllers_name:
        key = '/newben/apps/{0}/{1}'.format(args.kind, controller_name)
        logger.info('Watch etcd {0} key {1} start!'.format(etcd_obj.ip, key))
        futures.append(pool.submit(etcd_obj.watch, key))
    pool.shutdown()
    watch_info_list = []
    for future in as_completed(futures):
        watch_info_list.append(future.result()[0])

    pool = ThreadPoolExecutor(max_workers=10)
    futures = []
    for watch_info_generator in watch_info_list:
        futures.append(pool.submit(print_generator_value, watch_info_generator))
    pool.shutdown()
    for future in as_completed(futures):
        future.result()
