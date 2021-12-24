import pytest
import datetime
import os
from prettytable import PrettyTable
from libs.log_obj import LogObj
from libs.mysql_obj import MysqlObj
from stress.newben.common.node_obj import NodeObj
from stress.newben.common.common import check_health
from settings.newben_settings import NB_DB
from utils.times import sleep, str_to_datetime
from stress import arguments
from settings.newben_settings import INSTALL_YAML_PATH
from common.common import dump_yaml_data


logger = LogObj().get_logger()
args = arguments.parse_arg()


@pytest.fixture(scope='session')
def mysql_obj():
    if args.mysql_ip:
        return MysqlObj(args.mysql_ip, args.mysql_user, args.mysql_pwd, args.mysql_port)


@pytest.fixture(scope='session')
def db(mysql_obj):
    if mysql_obj:
        db = '{0}_{1}'.format(args.ip.replace('.', '_'), NB_DB)
        create_db = 'create database if not exists {0}'.format(db)
        mysql_obj.run_sql_cmd(create_db)
        return db


@pytest.fixture(scope='function')
def now_time():
    return str_to_datetime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


@pytest.fixture(scope='session')
def docker_fault_recovery_table(mysql_obj, db):
    if mysql_obj:
        table_name = 'docker_fault_recovery'
        sql_cmd = """create table if not exists {0}.{1} (
                    image VARCHAR(255) DEFAULT NULL,
                    node_number INT DEFAULT NULL,
                    docker_fault_check_take_time BIGINT DEFAULT NULL,
                    docker_boot_up_take_time BIGINT DEFAULT NULL,
                    docker_fault_recovery_take_time BIGINT DEFAULT NULL,
                    c_time DATETIME)""".format(db, table_name)
        mysql_obj.run_sql_cmd(sql_cmd)
        return table_name


@pytest.fixture(scope='session')
def node_fault_recovery_table(mysql_obj, db):
    if mysql_obj:
        table_name = 'node_fault_recovery'
        sql_cmd = """create table if not exists {0}.{1} (
                    image VARCHAR(255) DEFAULT NULL,
                    node_number INT DEFAULT NULL,
                    box_create_done_take_time BIGINT DEFAULT NULL,
                    docker_boot_up_take_time BIGINT DEFAULT NULL,
                    node_fault_recovery_take_time BIGINT DEFAULT NULL,
                    c_time DATETIME)""".format(db, table_name)
        mysql_obj.run_sql_cmd(sql_cmd)
        return table_name


@pytest.fixture(scope='session')
def docker_fault_recovery_tb():
    tb = PrettyTable()
    tb.field_names = ['Image', 'Node Number', 'Docker Fault Check Take Time(ms)',
                      'Docker Booted Up Take Time(ms)', 'Docker Fault Recovery Take Time(ms)',
                      'Docker Booted Up Take Time From Inspect(ms)']
    return tb


@pytest.fixture(scope='session')
def node_fault_recovery_tb():
    tb = PrettyTable()
    tb.field_names = ['Image', 'Node Number', 'Box Create Done Take Time(ms)', 'Docker Booted Up Take Time(ms)',
                      'Node Fault Recovery Take Time(ms)', 'Docker Booted Up Take Time From Inspect(ms)']
    return tb


@pytest.fixture(scope='session')
def add_delete_nodes_tb():
    tb = PrettyTable()
    tb.field_names = ['Nodes', 'Nodes Number', 'Add Time', 'Delete Time']
    return tb


@pytest.fixture(scope='function', autouse=True)
def cleanup(node1_obj):
    logger.info('Cleanup!')
    boxs_info = node1_obj.boxs_info
    if len(boxs_info) != 1:
        raise Exception('Boxes number must be 1!')
    box_info = boxs_info[0]
    box_name = box_info['meta']['name']
    workspace = box_info['meta']['workspace']
    node1_obj.delete_box(box_name, workspace)
    node1_obj.is_boxs_running()
    node1_obj.is_boxs_not_exist_by_name([box_name])
    for node_ip in node1_obj.nodes_ip:
        node_obj = NodeObj(node_ip, node1_obj.username, node1_obj.password)
        node_obj.clean_docker_log('nb-bootstrap')
    yield
    logger.info('Cleanup testbed!')
    for workerset_info in node1_obj.workersets_info:
        if workerset_info['status']['phase'] == 'maintained':
            node1_obj.exit_maintain_workerset(workerset_info['meta']['name'])


@pytest.fixture(scope='session')
def install_yaml_path(node1_obj):
    for ip in list(set(args.add_nodes_ip).difference(set(node1_obj.install_nodes_ip))):
        node_info = dict()
        node_info['address'] = ip
        node_info['modules'] = ["agent", "proxy"]
        node_info['password'] = "password"
        node_info['port'] = "22"
        node_info['user'] = "root"
        node1_obj.install_config_data['nodes'].append(node_info)
    node1_obj.make_dir(INSTALL_YAML_PATH)
    install_yaml_local_path = dump_yaml_data(node1_obj.install_config_data)
    install_yaml_path = os.path.join(INSTALL_YAML_PATH, 'install.yaml')
    node1_obj.remote_scp_put(install_yaml_local_path, install_yaml_path)
    return install_yaml_path


def test_docker_fault_recovery(node1_obj, mysql_obj, db, docker_fault_recovery_table, docker_fault_recovery_tb,
                               now_time):
    logger.info('Test start!')
    node_number = len(node1_obj.workersets_info)
    box_info = node1_obj.boxs_info[0]
    box_name = box_info['meta']['name']
    image = box_info['spec']['containers'][0]['image']
    docker_name = box_info['status']['containerStatuses'][0]['actualName']
    node_ip = node1_obj.get_node_ip_by_worker_name(box_info['status']['workerName'])
    node_obj = NodeObj(node_ip, node1_obj.username, node1_obj.password)
    docker_info = node_obj.docker_inspect(docker_name)
    docker_pid = docker_info[0]['State']['Pid']
    kill_time = datetime.datetime.now()
    node_obj.kill_process(docker_pid)
    sleep(5)
    node1_obj.is_box_running_by_name(box_name)
    docker_fault_check_time = node_obj.get_docker_fault_check_time(box_name)
    docker_fault_check_take_time = int((docker_fault_check_time - kill_time).total_seconds() * 1000)
    new_docker_info = node_obj.docker_inspect(docker_name)
    docker_id = new_docker_info[0]['Id']
    docker_boot_start_time = node_obj.get_docker_boot_start_time(docker_id)
    docker_boot_end_time = node_obj.get_docker_boot_end_time(docker_id)
    docker_boot_up_take_time = int((docker_boot_end_time - docker_boot_start_time).total_seconds() * 1000)
    docker_fault_recovery_take_time = int((docker_boot_end_time - kill_time).total_seconds() * 1000)

    tmp_finished_time = new_docker_info[0]['State']['FinishedAt'].split('T')
    finished_time = str_to_datetime(' '.join([tmp_finished_time[0], tmp_finished_time[1].strip('Z')[:-3]]),
                                    fmt="%Y-%m-%d %H:%M:%S.%f")
    tmp_started_time = new_docker_info[0]['State']['StartedAt'].split('T')
    started_time = str_to_datetime(' '.join([tmp_started_time[0], tmp_started_time[1].strip('Z')[:-3]]),
                                   fmt="%Y-%m-%d %H:%M:%S.%f")
    docker_boot_up_take_time_from_inspect = int((started_time - finished_time).total_seconds() * 1000)

    logger.debug('Docker kill time: {0}'.format(kill_time))
    logger.debug('Docker fault check time: {0}'.format(docker_fault_check_time))
    logger.debug('Docker boot start time: {0}'.format(docker_boot_start_time))
    logger.debug('Docker boot end time: {0}'.format(docker_boot_end_time))

    docker_fault_recovery_tb.add_row([image, node_number, docker_fault_check_take_time,
                                      docker_boot_up_take_time, docker_fault_recovery_take_time,
                                      docker_boot_up_take_time_from_inspect])
    logger.debug('Test Report:\n{0}'.format(docker_fault_recovery_tb))

    if mysql_obj:
        sql_cmd = """INSERT INTO {0}.{1} (image, node_number, docker_fault_check_take_time, 
        docker_boot_up_take_time, docker_fault_recovery_take_time, c_time) 
        VALUES ('{2}', {3}, {4}, {5}, {6}, '{7}')""".format(
            db, docker_fault_recovery_table, image, node_number, docker_fault_check_take_time,
            docker_boot_up_take_time, docker_fault_recovery_take_time, now_time)
        mysql_obj.run_sql_cmd(sql_cmd)


def test_node_fault_recovery(node1_obj, node_fault_recovery_tb, mysql_obj, db, docker_fault_recovery_table,
                             node_fault_recovery_table, now_time):
    node_number = len(node1_obj.workersets_info)
    box_info = node1_obj.boxs_info[0]
    worker_name = box_info['status']['workerName']
    image = box_info['spec']['containers'][0]['image']
    workerset_name = node1_obj.get_workerset_name_by_worker(worker_name)
    maintain_time = datetime.datetime.now()
    node1_obj.maintain_workerset(workerset_name)
    sleep(5)
    node1_obj.is_boxs_running()
    new_box_info = node1_obj.boxs_info[0]
    new_box_name = new_box_info['meta']['name']
    new_docker_name = new_box_info['status']['containerStatuses'][0]['actualName']
    latest_worker_name = new_box_info['status']['workerName']
    latest_node_ip = node1_obj.get_node_ip_by_worker_name(latest_worker_name)
    latest_node_obj = NodeObj(latest_node_ip, node1_obj.username, node1_obj.password)
    new_box_create_done_time = latest_node_obj.get_box_create_done_time(new_box_name)
    new_box_create_done_take_time = int((new_box_create_done_time - maintain_time).total_seconds() * 1000)

    new_docker_info = latest_node_obj.docker_inspect(new_docker_name)
    new_docker_id = new_docker_info[0]['Id']

    new_docker_boot_start_time = latest_node_obj.get_docker_boot_start_time(new_docker_id)
    new_docker_boot_end_time = latest_node_obj.get_docker_boot_end_time(new_docker_id)
    new_docker_boot_up_take_time = int((new_docker_boot_end_time - new_docker_boot_start_time).total_seconds() * 1000)
    node_fault_recovery_take_time = int((new_docker_boot_end_time - maintain_time).total_seconds() * 1000)

    tmp_created_time = new_docker_info[0]['Created'].split('T')
    created_time = str_to_datetime(' '.join([tmp_created_time[0], tmp_created_time[1].strip('Z')[:-3]]),
                                    fmt="%Y-%m-%d %H:%M:%S.%f")
    tmp_started_time = new_docker_info[0]['State']['StartedAt'].split('T')
    started_time = str_to_datetime(' '.join([tmp_started_time[0], tmp_started_time[1].strip('Z')[:-3]]),
                                   fmt="%Y-%m-%d %H:%M:%S.%f")
    docker_boot_up_take_time_from_inspect = int((started_time - created_time).total_seconds() * 1000)

    logger.debug('Node maintain time: {0}'.format(maintain_time))
    logger.debug('Box create done time: {0}'.format(new_box_create_done_time))
    logger.debug('Docker boot start time: {0}'.format(new_docker_boot_start_time))
    logger.debug('Docker boot end time: {0}'.format(new_docker_boot_end_time))
    node_fault_recovery_tb.add_row([image, node_number, new_box_create_done_take_time, new_docker_boot_up_take_time,
                                    node_fault_recovery_take_time, docker_boot_up_take_time_from_inspect])
    logger.debug('Test Report:\n{0}'.format(node_fault_recovery_tb))

    if mysql_obj:
        sql_cmd = """INSERT INTO {0}.{1} (image, node_number, box_create_done_take_time, docker_boot_up_take_time, 
        node_fault_recovery_take_time, c_time) VALUES ('{2}', {3}, {4}, {5}, {6}, '{7}')""".format(
            db, node_fault_recovery_table, image, node_number, new_box_create_done_take_time,
            new_docker_boot_up_take_time, node_fault_recovery_take_time, now_time)
        mysql_obj.run_sql_cmd(sql_cmd)


def test_scale_nodes(node1_obj, add_delete_nodes_tb, etcd_node_obj):
    start_time = datetime.datetime.now()
    node1_obj.update_node('add', install_yaml_path, args.add_nodes_ip)
    node1_obj.is_add_nodes_succeeded(args.add_nodes_ip)
    end_time = datetime.datetime.now()
    add_time = end_time - start_time
    logger.info('Add {0} nodes take time: {1}!'.format(len(args.add_nodes_ip), add_time))
    check_health(node1_obj, etcd_node_obj, add_nodes_ip=args.add_nodes_ip)
    start_time = datetime.datetime.now()
    node1_obj.update_node('delete', install_yaml_path, args.add_nodes_ip)
    node1_obj.is_delete_nodes_succeeded(args.add_nodes_ip)
    end_time = datetime.datetime.now()
    delete_time = end_time - start_time
    logger.info('Delete {0} nodes take time: {1}!'.format(len(args.add_nodes_ip), delete_time))
    add_delete_nodes_tb.add_row([args.add_nodes_ip, len(args.add_nodes_ip), add_time, delete_time])
    logger.debug('Test Report:\n{0}'.format(add_delete_nodes_tb))