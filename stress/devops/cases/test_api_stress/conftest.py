import pytest
from stress.devops.common.api_common import ApiCommon
from libs.log_obj import LogObj
from libs.mysql_obj import MysqlObj

logger = LogObj().get_logger()


@pytest.fixture(scope='session')
def devops_api_stress_common(api_login_data):
    return ApiCommon(api_login_data['login_data'], api_login_data['login_headers'], api_login_data['login_url'])


@pytest.fixture(scope='session')
def devops_api_stress_mysql_obj(api_login_data):
    return MysqlObj(api_login_data['database']['mysql']['host'], api_login_data['database']['mysql']['username'],
                    api_login_data['database']['mysql']['password'])


@pytest.fixture(scope='session')
def devops_api_stress_mysql_show_obj(api_login_data):
    return MysqlObj(api_login_data['database']['show_mysql']['host'],
                    api_login_data['database']['show_mysql']['username'],
                    api_login_data['database']['show_mysql']['password'])