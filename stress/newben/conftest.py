import pytest
from stress import arguments
from libs.log_obj import LogObj
from stress.newben.common.node_obj import NodeObj
from stress.newben.common.common import network_limit

args = arguments.parse_arg()
logger = LogObj().get_logger()


@pytest.fixture(scope='session')
def etcd_info(node1_obj):
    return node1_obj.etcd_info


@pytest.fixture(scope='session')
def etcd_node_obj(etcd_info):
    etcd_node_obj = NodeObj(etcd_info['ip'], args.sys_user, args.sys_pwd, args.sys_port)
    return etcd_node_obj


@pytest.fixture(scope='session')
def etcd_nodes_ip(etcd_node_obj):
    etcd_nodes_ip = []
    for etcd_info in etcd_node_obj.etcds_info:
        etcd_nodes_ip.append(etcd_info['ip'])
    return etcd_nodes_ip


@pytest.fixture(scope='session')
def node1_obj():
    return NodeObj(args.ip, args.sys_user, args.sys_pwd, args.sys_port)


if args.network_limit:
    @pytest.fixture(scope='function', autouse=True)
    def networks_limit(node1_obj):
        logger.info('Set the network limit before test!')
        network_limit(node1_obj)
        yield
        logger.info('Cancel the network limit after test!')
        network_limit(node1_obj, False)
