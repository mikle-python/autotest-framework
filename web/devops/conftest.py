import pytest
from web import arguments


args = arguments.parse_arg()


@pytest.fixture(scope='session')
def login_url():
    return 'http://{0}:{1}/devops-front/#/login'.format(args.ip, args.sys_port)
