import pytest
import socket
import datetime
import traceback
import json
import struct
from stress import arguments
from libs.log_obj import LogObj
from libs.mysql_obj import MysqlObj
from settings.global_settings import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, SOCKET_SERVER_TABLE, SOCKET_SERVER_PORT
from settings.newben_settings import NB_APP_TABLE, NB_DB
from utils.util import run_cmd, get_localhost_ip


logger = LogObj().get_logger()
args = arguments.parse_arg()


@pytest.fixture(scope='session')
def mysql_obj():
    return MysqlObj(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD)


@pytest.fixture(scope='session')
def socket_db():
    return '{0}_{1}'.format(args.ip.replace('.', '_'), NB_DB)


@pytest.fixture(scope='session')
def create_socket_db(mysql_obj, socket_db):
    create_db = 'create database if not exists {0}'.format(socket_db)
    mysql_obj.run_sql_cmd(create_db)


@pytest.fixture(scope='session')
def create_socket_server_table(mysql_obj, socket_db):
    create_table = """create table if not exists {0}.{1} (
                name VARCHAR(255) PRIMARY KEY,
                ip VARCHAR(255) DEFAULT NULL,
                port INT,
                status TINYINT(1) DEFAULT 1,
                connected TINYINT(1) DEFAULT 0,
                client_ip VARCHAR(255) DEFAULT NULL,
                client_port INT DEFAULT NULL,
                c_time DATETIME DEFAULT NULL,
                su_time DATETIME DEFAULT NULL,
                cu_time DATETIME DEFAULT NULL)""".format(socket_db, SOCKET_SERVER_TABLE)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def socket_server_name():
    cmd = 'env | grep app_name'
    rtn_dict = run_cmd(cmd)
    if rtn_dict['rc'] == 0 and not rtn_dict['stderr']:
        return rtn_dict['stdout'].strip().split('=')[-1]
    else:
        raise Exception('App had not exist into env!')


@pytest.fixture(scope='session')
def socket_server_ip():
    return get_localhost_ip()


@pytest.fixture(scope='session')
def cmd_result_table(socket_server_name):
    return '{0}_cmd_result'.format(socket_server_name.replace('-', '_'))


@pytest.fixture(scope='session')
def create_cmd_result_table(mysql_obj, cmd_result_table, socket_db):
    create_table = """create table if not exists {0}.{1} (
                client_ip VARCHAR(255),
                client_port INT,
                cmd VARCHAR(255),
                rc INT,
                stdout TEXT DEFAULT NULL,
                stderr TEXT DEFAULT NULL,
                c_time DATETIME)""".format(socket_db, cmd_result_table)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_app_table(mysql_obj, socket_db):
    create_table = """create table if not exists {0}.{1} (
                workspace VARCHAR(255),
                name VARCHAR(255),
                ippool VARCHAR(255))""".format(socket_db, NB_APP_TABLE)
    mysql_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def init_app_table(node1_obj, mysql_obj, socket_db):
    for app_info in node1_obj.get_apps_info_by_workspace(args.workspace):
        workspace = app_info['meta']['workspace']
        name = app_info['meta']['name']
        ippool = app_info['spec']['template']['spec']['template']['spec']['network']
        init_app_table = """INSERT INTO {0}.{1} (workspace, name, ippool) SELECT '{2}','{3}','{4}' 
        FROM DUAL WHERE NOT EXISTS (SELECT * FROM {0}.{1} WHERE workspace='{2}' and name='{3}')""".format(
            socket_db, NB_APP_TABLE, workspace, name, ippool)
        mysql_obj.run_sql_cmd(init_app_table)


@pytest.fixture(scope='session')
def socket_server_info(mysql_obj, socket_db):
    get_socket_server_cmd = 'select * from {0}.{1}'.format(socket_db, SOCKET_SERVER_TABLE)
    rows = mysql_obj.run_sql_cmd(get_socket_server_cmd)
    for row in rows:
        if row['status'] == 0 and row['connected'] == 0:
            return row
    else:
        raise Exception('All socket servers had been connected!')


@pytest.fixture(scope='session')
def nb_apps_info(mysql_obj, socket_db):
    get_nb_apps_info = 'select * from {0}.{1}'.format(socket_db, NB_APP_TABLE)
    return mysql_obj.run_sql_cmd(get_nb_apps_info)


@pytest.fixture(scope='session')
def cmd_list(mysql_obj, nb_apps_info):
    cmd_list = []
    for cmd in args.cmds:
        if cmd == 'ping -c 1' or cmd == 'dig':
            for app_info in nb_apps_info:
                if cmd == 'dig':
                    cmd_suffix = '{0}.{1}.svc.cluster.local'.format(app_info['name'], app_info['workspace'])
                else:
                    cmd_suffix = '{0}.{1}'.format(app_info['name'], app_info['workspace'])
                full_cmd = '{0} {1}'.format(cmd, cmd_suffix)
                cmd_list.append(full_cmd)
        elif cmd == 'dig_ping':
            tmp_cmds = cmd.split('_')
            for app_info in nb_apps_info:
                cmd_suffix = '{0}.{1}'.format(app_info['name'], app_info['workspace'])
                tmp_cmd1 = '{0} {1}.svc.cluster.local'.format(tmp_cmds[0], cmd_suffix)
                tmp_cmd2 = '{0} -c 1 {1}'.format(tmp_cmds[1], cmd_suffix)
                full_cmd = '{0};{1}'.format(tmp_cmd1, tmp_cmd2)
                cmd_list.append(full_cmd)
        else:
            cmd_list.append(cmd)
    return cmd_list


@pytest.mark.usefixtures("init_app_table")
@pytest.mark.usefixtures("create_app_table")
def test_socket_run(mysql_obj, socket_server_info, cmd_list):
    socket_server_ip = socket_server_info['ip']
    socket_server_port = socket_server_info['port']
    try:
        logger.info('Socket server {0}:{1} is connecting!'.format(socket_server_ip, socket_server_port))
        socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_obj.connect((socket_server_ip, socket_server_port))
        logger.info('Socket server {0}:{1} is connected!'.format(socket_server_ip, socket_server_port))
        while True:
            for cmd in cmd_list:
                cmd_header = struct.pack('i', len(cmd))
                socket_obj.send(cmd_header)
                socket_obj.send(cmd.encode('utf-8'))
                rtn_header = socket_obj.recv(4)
                rtn_size = struct.unpack('i', rtn_header)[0]
                logger.debug('rtn size is {0}!'.format(rtn_size))
                recv_size = 0
                total_data = b''
                while recv_size < rtn_size:
                    recv_data = socket_obj.recv(1024)
                    recv_size += len(recv_data)
                    total_data += recv_data
                    logger.debug('recv_size: {0}'.format(recv_size))
                logger.info('{0}:{1} socket server cmd executed done: {2}'.format(
                    socket_server_ip, socket_server_port, cmd))
                logger.info('Result: {0}'.format(total_data.decode('utf-8')))
    except KeyboardInterrupt:
        logger.warning('Socket client was cancelled!')
    except Exception as e:
        raise Exception('Connect socket server {0}:{1} exception occured, error is {2}!'.format(socket_server_ip,
                                                                                                socket_server_port, e))
    finally:
        socket_obj.close()
        logger.info("Socket server {0}:{1} is disconnected!".format(socket_server_ip, socket_server_port))


@pytest.mark.usefixtures("create_cmd_result_table")
@pytest.mark.usefixtures("create_socket_server_table")
@pytest.mark.usefixtures("create_socket_db")
def test_socket_server(mysql_obj, socket_server_ip, socket_server_name, socket_db, cmd_result_table):
    try:
        c_time = datetime.datetime.now()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((socket_server_ip, SOCKET_SERVER_PORT))
        sock.listen(1)
        sql_cmd = """INSERT INTO {0}.{1} (name, port, c_time) SELECT '{2}',{3},'{4}' 
        FROM DUAL WHERE NOT EXISTS (SELECT * FROM {0}.{1} WHERE name='{2}')""".format(
            socket_db, SOCKET_SERVER_TABLE, socket_server_name, SOCKET_SERVER_PORT, c_time)
        mysql_obj.run_sql_cmd(sql_cmd)
        update_status = 'update {0}.{1} set ip="{2}", status=0, connected=0, su_time="{3}" where name="{4}"'.format(
            socket_db, SOCKET_SERVER_TABLE, socket_server_ip, c_time, socket_server_name)
        mysql_obj.run_sql_cmd(update_status)
        while True:
            logger.info("Waitting for connection...")
            conn, client_addr = sock.accept()
            client_ip = client_addr[0]
            client_port = client_addr[1]
            client_addr_str = '{0}:{1}'.format(client_ip, client_port)
            logger.info("{0} successful connection!".format(client_addr_str))
            update_server = 'update {0}.{1} set connected=1, client_ip="{2}", client_port={3}, cu_time="{4}" ' \
                            'where name="{5}"'.format(
                socket_db, SOCKET_SERVER_TABLE, client_ip, client_port, datetime.datetime.now(), socket_server_name)
            mysql_obj.run_sql_cmd(update_server)
            while True:
                try:
                    cmd_header = conn.recv(4)
                    cmd_size = struct.unpack('i', cmd_header)[0]
                    logger.debug('cmd size is {0}!'.format(cmd_size))
                    recv_size = 0
                    total_data = b''
                    while recv_size < cmd_size:
                        recv_data = conn.recv(1024)
                        recv_size += len(recv_data)
                        total_data += recv_data
                        logger.debug('recv_size: {0}'.format(recv_size))
                    cmd = total_data.decode('utf-8')
                    rtn_dict = run_cmd(cmd)
                    logger.info('From socket client {0} cmd executed done: {1}'.format(client_addr, cmd))
                    rtn_dict_str = json.dumps(rtn_dict)
                    rtn_header = struct.pack('i', len(rtn_dict_str))
                    conn.send(rtn_header)
                    conn.send(rtn_dict_str.encode('utf-8'))
                    rc = rtn_dict['rc']
                    stdout = rtn_dict['stdout'].strip() if rtn_dict['stdout'] else rtn_dict['stdout']
                    stderr = rtn_dict['stderr'].strip() if rtn_dict['stderr'] else rtn_dict['stderr']
                    if stdout is None and stderr is not None:
                        sql_cmd = """INSERT INTO {0}.{1} (client_ip, client_port, cmd, rc, stderr, c_time) 
                        VALUES ('{2}', {3}, '{4}', {5}, '{6}', '{7}')""".format(
                            socket_db, cmd_result_table, client_ip, client_port, cmd, rc, stderr,
                            datetime.datetime.now())
                    elif stderr is None and stdout is not None:
                        sql_cmd = """INSERT INTO {0}.{1} (client_ip, client_port, cmd, rc, stdout, c_time) 
                                            VALUES ('{2}', {3}, '{4}', {5}, '{6}', '{7}')""".format(
                            socket_db, cmd_result_table, client_ip, client_port, cmd, rc, stdout,
                            datetime.datetime.now())
                    elif stdout is None and stderr is None:
                        sql_cmd = """INSERT INTO {0}.{1} (client_ip, client_port, cmd, rc, c_time) 
                                                                VALUES ('{2}', {3}, '{4}', {5}, '{6}')""".format(
                            socket_db, cmd_result_table, client_ip, client_port, cmd, rc, datetime.datetime.now())
                    else:
                        sql_cmd = """INSERT INTO {0}.{1} (client_ip, client_port, cmd, rc, stdout, stderr, c_time) 
                        VALUES ('{2}', {3}, '{4}', {5}, '{6}', '{7}', '{8}')""".format(
                            socket_db, cmd_result_table, client_ip, client_port, cmd, rc, stdout, stderr,
                            datetime.datetime.now())
                    mysql_obj.run_sql_cmd(sql_cmd)
                except Exception:
                    logger.warning('Conenction exception occured, error is {0}!'.format(traceback.format_exc()))
                    break
            conn.close()
            logger.info("Connect is disconnected...")
            update_server = 'update {0}.{1} set connected=0, client_ip=NULL, client_port=NULL, cu_time="{2}" ' \
                            'where name="{3}"'.format(socket_db, SOCKET_SERVER_TABLE, datetime.datetime.now(),
                                                      socket_server_name)
            mysql_obj.run_sql_cmd(update_server)
    except KeyboardInterrupt:
        logger.warning('Socket server was cancelled!')
    except Exception as e:
        raise Exception('Socket server exception occured, error is {0}!'.format(traceback.format_exc()))
    finally:
        sock.close()
        logger.info("Socket server is disconnected...")
        update_server = 'update {0}.{1} set connected=0, status=1, client_ip=NULL, client_port=NULL, ' \
                        'su_time="{2}" ' 'where name="{3}"'.format(socket_db, SOCKET_SERVER_TABLE,
                                                                   datetime.datetime.now(), socket_server_name)
        mysql_obj.run_sql_cmd(update_server)
