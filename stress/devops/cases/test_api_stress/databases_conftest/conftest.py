import pytest
from libs.log_obj import LogObj

logger = LogObj().get_logger()


@pytest.fixture(scope='session')
def db(api_data_for_devops):
    server_ip = api_data_for_devops['common']['api_server_ip']
    return '{}_devops_stress'.format(server_ip.replace('.', '_'))


@pytest.fixture(scope='session', autouse=True)
def init_db(mysql_show_obj, db, api_mysql_data):
    logger.info("Init the database for storage response time ...")
    create_db = 'create database if not exists {0}'.format(db)
    mysql_show_obj.run_sql_cmd(create_db)

    for table_name in api_mysql_data:
        sql = """create table if not exists {0}.{1} (
                        api VARCHAR(255), 
                        take_time double,
                        c_time DATETIME)""".format(db, table_name)
        mysql_show_obj.run_sql_cmd(sql)
