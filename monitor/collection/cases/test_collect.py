import datetime
import pytest
import json
from common.common import get_cpu_usage, get_memory_usage, get_iostats
from libs.mysql_obj import MysqlObj
from libs.log_obj import LogObj
from settings.global_settings import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD
from monitor.collection import arguments
from utils.util import get_localhost_ip
from utils.times import sleep


logger = LogObj().get_logger()
args = arguments.parse_arg()


@pytest.fixture(scope='session')
def mysql_obj():
    return MysqlObj(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD)


@pytest.fixture(scope='session')
def localhost_ip():
    return get_localhost_ip()


@pytest.fixture(scope='session')
def db(localhost_ip):
    return '{0}_system_resource'.format(localhost_ip.replace('.', '_'))


@pytest.fixture(scope='session')
def volume_db():
    return '{0}_{1}'.format(args.ip.replace('.', '_'), args.device.split('/')[-1])


@pytest.fixture(scope='session', autouse=True)
def create_system_db(mysql_obj, db):
    create_db = 'create database if not exists {0}'.format(db)
    mysql_obj.run_sql_cmd(create_db)


@pytest.fixture(scope='session', autouse=True)
def create_volume_db(mysql_obj, volume_db):
    create_volume_db = 'create database if not exists {0}'.format(volume_db)
    mysql_obj.run_sql_cmd(create_volume_db)


@pytest.fixture(scope='session')
def cpu_usage_table():
    return 'cpu_usage'


@pytest.fixture(scope='session')
def create_cpu_table(mysql_obj, db, cpu_usage_table):
    create_table = """create table if not exists {0}.{1} (
                percent FLOAT,
                user FLOAT,
                sys FLOAT,
                idle FLOAT,
                iowait FLOAT,
                nice FLOAT,
                c_time DATETIME)""".format(db, cpu_usage_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def memory_usage_table():
    return 'memory_usage'


@pytest.fixture(scope='session')
def create_memory_table(mysql_obj, db, memory_usage_table):
    create_table = """create table if not exists {0}.{1} (
                total BIGINT,
                available BIGINT,
                percent float,
                used BIGINT,
                free BIGINT,
                buffers BIGINT,
                cached BIGINT,
                c_time DATETIME)""".format(db, memory_usage_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def iostat_table():
    return 'iostat'


@pytest.fixture(scope='session')
def create_iostat_table(mysql_obj, volume_db, iostat_table):
    create_table = """create table if not exists {0}.{1} (
                                io_stat JSON,
                                c_time datetime)""".format(volume_db, iostat_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.mark.usefixtures("create_memory_table")
@pytest.mark.usefixtures("create_cpu_table")
def test_system(mysql_obj, db, cpu_usage_table, memory_usage_table):
    while True:
        cpu_usage = get_cpu_usage()
        memory_usage = get_memory_usage()
        now_time = datetime.datetime.now()
        insert_cpu_usage = """INSERT INTO {0}.{1} (percent, user, sys, idle, iowait, nice, c_time) 
            VALUES ('{2}', {3}, '{4}', {5}, '{6}', '{7}', '{8}')""".format(
            db, cpu_usage_table, cpu_usage['percent'], cpu_usage['user'], cpu_usage['system'], cpu_usage['idle'],
            cpu_usage['iowait'], cpu_usage['nice'], now_time)
        mysql_obj.run_sql_cmd(insert_cpu_usage)
        insert_memory_usage = """INSERT INTO {0}.{1} (total, available, percent, used, free, buffers, cached, c_time) 
        VALUES ('{2}', {3}, '{4}', {5}, '{6}', '{7}', '{8}', '{9}')""".format(
            db, memory_usage_table, memory_usage['total'], memory_usage['available'], memory_usage['percent'],
            memory_usage['used'], memory_usage['free'], memory_usage['buffers'], memory_usage['cached'], now_time)
        mysql_obj.run_sql_cmd(insert_memory_usage)
        sleep(args.interval)


def test_volume(mysql_obj, volume_db, iostat_table):
    while True:
        try:
            for c_time, io_stat in get_iostats(args.device, args.ip, args.username, args.password).items():
                if io_stat:
                    sql_cmd = """INSERT INTO {0}.{1} (
                                        io_stat,
                                        c_time)
                                        VALUES (
                                        '{2}',
                                        '{3}')""".format(volume_db, iostat_table, json.dumps(io_stat), c_time)
                    mysql_obj.run_sql_cmd(sql_cmd)
        except Exception as e:
            logger.error('Exception occured, error is {err}!'.format(err=e))

