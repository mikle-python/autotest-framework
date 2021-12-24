import pytest
from stress import arguments
from common.common import load_yaml
from libs.log_obj import LogObj
from stress.ecos.common.node_obj import NodeObj
from stress.ecos.common.common import check_health

args = arguments.parse_arg()
logger = LogObj().get_logger()


@pytest.fixture(scope='session')
def node1_obj():
    return NodeObj(args.ip, args.sys_user, args.sys_pwd)


@pytest.fixture(scope='session')
def component_test_data(component):
    test_data = load_yaml('config/components.yaml')['components']
    try:
        component_test_data = test_data[component]
    except KeyError:
        raise Exception("Not found the key:{}, please check it again !")
    return component_test_data


@pytest.fixture(scope='session')
def platform_test_data():
    return load_yaml('config/platform.yaml')


@pytest.fixture(scope='function', autouse=True)
def check(node1_obj):
    logger.info('Check health before test!')
    check_health(node1_obj)
    yield
    logger.info('Check health after test!')
    check_health(node1_obj)
