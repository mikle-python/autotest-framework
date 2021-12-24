import pytest
from web import arguments


args = arguments.parse_arg()


@pytest.fixture(scope='session')
def login_url(config):
    return 'http://{0}/#/login'.format(args.ip, args.sys_port)

@pytest.fixture(scope='session')
def nginx():
    return "registry.cluster.local/amd64/nginx"