import os
import datetime
import yaml
import json
import pytz
from utils.times import sleep
from libs.log_obj import LogObj
from libs.request_obj import RequstObj
from stress.newben.common.node_obj import NodeObj
from utils.decorator import retry, print_for_call, run_time
from settings.global_settings import PROJECT_PATH
from settings.newben_settings import COLLECT_CORE_DUMP_PROCESSED, NB_DOCKERS
from concurrent.futures import ThreadPoolExecutor, as_completed
from common.common import dump_yaml_data, is_ping_ok

logger = LogObj().get_logger()


@run_time
def check_health(node1_obj, etcd_node_obj, workspace=None, add_nodes_ip=[], single=False):
    etcd_node_obj.is_docker_active()
    etcd_node_obj.is_etcd_up()

    node1_obj.is_docker_active()
    node1_obj.is_coreserver_up()
    is_coreserver_login_succeed(node1_obj.ip, "admin", "password")
    node1_obj.is_web_up()
    node1_obj.is_rqlite_up()
    node1_obj.is_log_up(single)

    nodes_ip = node1_obj.nodes_ip
    for ip in nodes_ip:
        is_ping_ok(ip)
    nodes_obj = [node1_obj]
    for node_ip in nodes_ip:
        if node_ip != node1_obj.ip and node_ip != etcd_node_obj.ip:
            node_obj = NodeObj(node_ip, node1_obj.username, node1_obj.password, node1_obj.port)
            nodes_obj.append(node_obj)
            node_obj.is_docker_active()

    for node_obj in nodes_obj:
        if node_obj.ip not in add_nodes_ip:
            node_obj.is_seam_up(single)
        node_obj.is_bootstrap_up()
        node_obj.is_agent_up()
        node_obj.is_docker_nai_up()
        node_obj.is_proxy_up(single)

    node1_obj.is_workersets_running()
    node1_obj.is_workers_running()
    node1_obj.is_boxs_running(workspace)
    node1_obj.is_boxsets_running(workspace)
    node1_obj.is_apps_running(workspace)
    node1_obj.is_forwards_ok(workspace)


def network_limit(node1_obj, set_limit=True):
    rate = 5120
    latency = 50
    burst = 5120
    if set_limit:
        network_limit_cmd = "tc qdisc add dev ens160 root tbf rate {rate}kbit latency {latency}ms burst {burst}" \
            .format(rate=rate, latency=latency, burst=burst)

        results = node1_obj.run_cmd(network_limit_cmd)
        if results['rc'] == 0 and results['stderr'] == '':
            logger.info("Set the network limit done")
        else:
            logger.warning(results)
            raise Exception("Set the network limit fail")
    else:
        network_limit_cmd = "tc qdisc del dev ens160 root"
        results = node1_obj.run_cmd(network_limit_cmd)
        if results['rc'] == 0 and results['stderr'] == '':
            logger.info("Cancel the network limit done")
        else:
            logger.warning(results)
            raise Exception("Cancel the network limit fail")


def access_nginx(ip, port):
    try:
        url = 'http://{0}:{1}/'.format(ip, port)
        request_obj = RequstObj()
        response = request_obj.call('GET', url)
        return response
    except Exception as e:
        raise e


@retry(tries=120, delay=5)
@print_for_call
def is_nginx_working(ip, forward_info):
    try:
        port = forward_info['spec']['rules'][0]['exposePort']
        app_name = forward_info['spec']['selector']['application-name']
        response = access_nginx(ip, port)
        response_code = response.status_code
        response_text = response.text
        if response_code == 200 and response_text == app_name:
            logger.info('App {0} nginx {1}:{2} is working, access take time is {3}!'.format(app_name, ip, port,
                                                                                            response.elapsed))
        else:
            raise Exception('App {0} nginx {1}:{2} is not working, response code is {3}, response text is {4}!'.format(
                app_name, ip, port, response_code, response_text))
    except Exception as e:
        logger.warning('App {0} nginx {1}:{2} exception occured, error is {3}!'.format(app_name, ip, port, e))
        raise e


@retry(tries=120, delay=5)
@print_for_call
def is_nginx_working_tmp(ip, forward_info):
    try:
        port = forward_info['spec']['rules'][0]['exposePort']
        app_name = forward_info['spec']['selector']['application-name']
        response = access_nginx(ip, port)
        response_code = response.status_code
        response_text = response.text
        if response_code == 200:
            logger.info('App {0} nginx {1}:{2} is working, access take time is {3}!'.format(app_name, ip, port,
                                                                                            response.elapsed))
        else:
            raise Exception('App {0} nginx {1}:{2} is not working, response code is {3}, response text is {4}!'.format(
                app_name, ip, port, response_code, response_text))
    except Exception as e:
        logger.warning('App {0} nginx {1}:{2} exception occured, error is {3}!'.format(app_name, ip, port, e))
        raise e


@retry(tries=120, delay=5)
@print_for_call
def is_nginxs_working(ip, forwards_info):
    not_working_nginxs = []
    access_apps_info = []
    try:
        for forward_info in forwards_info:
            tmp_info = dict()
            port = forward_info['spec']['rules'][0]['exposePort']
            app_name = forward_info['spec']['selector']['application-name']
            tmp_info['name'] = app_name
            start_time = datetime.datetime.now()
            response = access_nginx(ip, port)
            response_code = response.status_code
            response_text = response.text
            if response_code == 200 and response_text == app_name:
                end_time = datetime.datetime.now()
                take_time = end_time - start_time
                logger.info('App {0} nginx {1}:{2} is working, access take time is {3}!'.format(app_name, ip, port,
                                                                                                take_time))
                tmp_info['time'] = take_time
                access_apps_info.append(tmp_info)
            else:
                not_working_nginxs.append({app_name: port})
                logger.warning('App {0} nginx {1}:{2} is not working, response code is {3}, response text is {4}!'.
                               format(app_name, ip, port, response_code, response_text))
    except Exception as e:
        not_working_nginxs.append({app_name: port})
        logger.warning('App {0} nginx {1}:{2} exception occured, error is {3}!'.format(app_name, ip, port, e))

    if not_working_nginxs:
        raise Exception('Not working nginx are {0}!'.format(not_working_nginxs))
    else:
        logger.info('All nginx are working!')
        return access_apps_info


def collect_nb_processes_core_dump(node1_obj, core_dump_dir):
    pool = ThreadPoolExecutor(max_workers=10)
    futures = []
    for node_ip in node1_obj.nodes_ip:
        node_obj = NodeObj(node_ip, node1_obj.username, node1_obj.password)
        node_obj.make_dir(core_dump_dir)
        for process_name in COLLECT_CORE_DUMP_PROCESSED:
            futures.append(pool.submit(node_obj.collect_process_core_dump, process_name, core_dump_dir))
    pool.shutdown()
    for future in as_completed(futures):
        future.result()
    logger.info('All core dump files have been collected to {0} of each node!'.format(core_dump_dir))


def collect_nb_docker_logs(node1_obj, log_dir):
    pool = ThreadPoolExecutor(max_workers=10)
    futures = []
    for node_ip in node1_obj.nodes_ip:
        node_obj = NodeObj(node_ip, node1_obj.username, node1_obj.password)
        node_obj.make_dir(log_dir)
        dockers_name = node_obj.dockers_name
        for docker_name in NB_DOCKERS:
            if docker_name in dockers_name:
                futures.append(pool.submit(node_obj.docker_logs, docker_name, log_dir))
    pool.shutdown()
    for future in as_completed(futures):
        future.result()
    logger.info('All logs have been collected to {0} of each node!'.format(log_dir))


def create_app_yaml(name, workspace, replicas, image, ippool='seam-cni', volume_mounts=None, volumes=None,
                    command=None, envs=None, worker=None, resources=None):
    with open(os.path.join(PROJECT_PATH, 'stress/newben/templates/app_template.yaml'), mode='r') as file_obj:
        file_data = yaml.load(file_obj, Loader=yaml.FullLoader)
        file_data['meta']['name'] = name
        file_data['meta']['workspace'] = workspace
        file_data['spec']['template']['spec']['replicas'] = replicas
        file_data['spec']['template']['spec']['template']['spec']['network'] = ippool
        file_data['spec']['template']['spec']['template']['spec']['containers'][0]['image'] = image
        file_data['spec']['template']['spec']['template']['spec']['containers'][0]['name'] = '{0}-container'.format(
            name)
        if volume_mounts and volumes:
            file_data['spec']['template']['spec']['template']['spec']['containers'][0]['volumeMounts'] = volume_mounts
            file_data['spec']['template']['spec']['template']['spec']['volumes'] = volumes
        if command:
            file_data['spec']['template']['spec']['template']['spec']['containers'][0]['command'] = command.split('===')
        if envs:
            file_data['spec']['template']['spec']['template']['spec']['containers'][0]['env'] = envs
        if worker:
            file_data['spec']['template']['spec']['template']['spec']['workerName'] = worker
        if resources:
            file_data['spec']['template']['spec']['template']['spec']['containers'][0]['resources'] = resources

    return dump_yaml_data(file_data)


def create_appmatrix_yaml(name, workspace, replicas, image, ippool='default-pool', volume_mounts=None, volumes=None,
                          command=None, envs=None, worker=None, resources=None):
    with open(os.path.join(PROJECT_PATH, 'stress/newben/templates/appmatrix_template.yaml'), mode='r') as file_obj:
        file_data = yaml.load(file_obj, Loader=yaml.FullLoader)

        file_data['meta']['workspace'] = workspace
        file_data['meta']['name'] = name

        file_data['spec']['topology'][0]['name'] = name
        file_data_meta = file_data['spec']['items'][0]['meta']
        file_data_spec = file_data['spec']['items'][0]['spec']
        file_data_meta['name'] = name

        file_data_spec['template']['spec']['replicas'] = replicas
        file_data_spec['template']['spec']['template']['spec']['network'] = ippool
        file_data_spec['template']['spec']['template']['spec']['containers'][0]['image'] = image
        file_data_spec['template']['spec']['template']['spec']['containers'][0]['name'] = '{0}-container'.format(
            name)

        if volume_mounts and volumes:
            file_data_spec['template']['spec']['template']['spec']['containers'][0]['volumeMounts'] = volume_mounts
            file_data_spec['template']['spec']['template']['spec']['volumes'] = volumes
        if command:
            file_data_spec['template']['spec']['template']['spec']['containers'][0]['command'] = command.split('===')
        if envs:
            file_data_spec['template']['spec']['template']['spec']['containers'][0]['env'] = envs
        if worker:
            file_data_spec['template']['spec']['template']['spec']['workerName'] = worker
        if resources:
            file_data_spec['template']['spec']['template']['spec']['containers'][0]['resources'] = resources

    return dump_yaml_data(file_data)


def create_mission_yaml(name, workspace, image, datas, command=None):
    with open(os.path.join(PROJECT_PATH, 'stress/newben/templates/mission_template.yaml'), mode='r') as file_obj:
        file_data = yaml.load(file_obj, Loader=yaml.FullLoader)
        file_data['meta']['name'] = name
        file_data['meta']['workspace'] = workspace
        file_data['spec']['template']['containers'][0]['image'] = image
        file_data['spec']['template']['containers'][0]['name'] = '{0}-container'.format(name)
        if command:
            file_data['spec']['template']['containers'][0]['command'] = command

        volume_mounts_info = file_data['spec']['template']['containers'][0]['volumeMounts']
        file_data['spec']['template']['containers'][0]['volumeMounts'] = []
        for mount_info in volume_mounts_info:
            mount_info['subPath'] = datas[mount_info['mountPath']]
            file_data['spec']['template']['containers'][0]['volumeMounts'].append(mount_info)
    return dump_yaml_data(file_data)


def create_forward_yaml(name, workspace, port):
    with open(os.path.join(PROJECT_PATH, 'stress/newben/templates/forward_template.yaml'), mode='r') as file_obj:
        file_data = yaml.load(file_obj, Loader=yaml.FullLoader)
        file_data['meta']['name'] = name
        file_data['meta']['workspace'] = workspace
        file_data['spec']['rules'][0]['boxPort'] = port
        file_data['spec']['selector']['application-name'] = name
    return dump_yaml_data(file_data)


def create_apparafile_yaml(name, workspace, data):
    with open(os.path.join(PROJECT_PATH, 'stress/newben/templates/apparafile_template.yaml'), mode='r') as file_obj:
        file_data = yaml.load(file_obj, Loader=yaml.FullLoader)
        file_data['meta']['name'] = name
        file_data['meta']['workspace'] = workspace
        file_data['spec']['data'] = data
    return dump_yaml_data(file_data)


@retry(tries=5, delay=5)
@print_for_call
def is_coreserver_login_succeed(ip, username, password):
    url = 'http://{0}:8080/apis/login'.format(ip)
    request_obj = RequstObj()
    data = {"username": username, "password": password, "provider": "builtin"}
    response = request_obj.call('post', url, data=json.dumps(data))
    response_code = response.status_code
    response_text = response.text
    logger.debug('Response code: {0}!'.format(response_code))
    logger.debug('Response text: {0}!'.format(response_text))
    if response_code != 200:
        raise Exception('Login coreserver {0} failed!'.format(ip))
    logger.info('Login coreserver {0} succeed!'.format(ip))


def ai_auth_token(request_obj, ai_api_username, ai_api_password, api_server):
    login_data = {
        "userName": ai_api_username,
        "password": ai_api_password,
    }
    login_headers = {
        "Content-Type": "application/json;charset=UTF-8"
    }
    login_response = request_obj.call('post', api_server + "/ai/login/login", data=json.dumps(login_data),
                                      headers=login_headers).json()
    if login_response['code'] == "200" and login_response['message'] == "success":
        logger.info("Login api server {} successfully !".format(api_server))
        return login_response['data']['token']
    else:
        raise Exception("Login api server {} failed, the error messages are [{}]".
                        format(api_server, login_response))


def create_ai_mission_by_api(request_obj, server_address, mission_name, auth_token, train_code_path, train_data_path,
                             train_output_path, command="python mnist.py"):
    create_mission_url = server_address + "/ai/job/create"
    create_mission_headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": auth_token
    }
    create_mission_data = {
        "name": mission_name,
        "version": "0.0.1",
        "computingFrameworkId": 1,
        "algorithmPath": train_code_path,
        "startCommand": command,
        "dataSet": train_data_path,
        "outputPath": "{}/{}".format(train_output_path, mission_name),
        "trainingMode": {
            "trainingMode": "SINGLE",
            "workerResourceId": 1
        }
    }
    create_response = request_obj.call("post", create_mission_url, data=json.dumps(create_mission_data),
                                       headers=create_mission_headers)

    try:
        create_response = create_response.json()
    except Exception as e:
        if "Expecting value: line 1 column 1 (char 0)" in str(e):
            logger.warning("The response: {}".format(create_response.content.decode()))
            logger.warning("The data happened error: {}".format(create_mission_data))
            raise e

    if create_response['code'] == "200" and create_response['message'] == "success":
        logger.info("Create mission {} successfully !".format(mission_name))
        return create_response['data']
    else:
        raise Exception("Create mission {} failed, the error messages are [{}]".format(mission_name, create_response))


def stop_ai_mission_by_api(request_obj, server_address, stop_id, mission_name, auth_token):
    stop_mission_url = server_address + "/ai/job/stop?id={}".format(stop_id)
    stop_mission_headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": auth_token
    }
    stop_mission_data = {
        "id": stop_id
    }
    stop_response = request_obj.call("post", stop_mission_url, data=json.dumps(stop_mission_data),
                                     headers=stop_mission_headers)

    try:
        stop_response = stop_response.json()
    except Exception as e:
        if "Expecting value: line 1 column 1 (char 0)" in str(e):
            logger.warning("The response: {}".format(stop_response.content.decode()))
            logger.warning("The data happened error: {}".format(stop_mission_data))
            raise e

    if stop_response['code'] == "200" and stop_response['message'] == "success":
        logger.info("Stop mission {} successfully !".format(mission_name))
        return int(datetime.datetime.now(pytz.timezone("UTC")).timestamp())
    else:
        raise Exception("Stop mission {} failed, the error messages are [{}]".format(mission_name, stop_response))


def delete_ai_mission_by_api(request_obj, server_address, delete_id, mission_name, auth_token):
    delete_ai_mission_url = server_address + "/ai/job/delete?id={}".format(delete_id)
    delete_ai_mission_headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": auth_token
    }
    delete_mission_data = {
        "id": delete_id
    }

    delete_response = request_obj.call("delete", delete_ai_mission_url, data=json.dumps(delete_mission_data),
                                       headers=delete_ai_mission_headers).json()
    if delete_response['code'] == "200" and delete_response['message'] == "success":
        logger.info("Delete ai mission {} successfully !".format(mission_name))
    else:
        raise Exception("Delete ai mission {} failed, the error messages are [{}]".
                        format(mission_name, delete_response))


def create_stop_ai_mission(request_obj, node1_obj, server_address, mission_name, auth_token, create_to_stop,
                           train_code_path, train_data_path, train_output_path, command="python mnist.py"):
    stop_id = create_ai_mission_by_api(request_obj, server_address, mission_name, auth_token, train_code_path,
                                       train_data_path, train_output_path, command)
    node1_obj.is_box_running_new(mission_name)
    sleep(create_to_stop)
    stop_time = stop_ai_mission_by_api(request_obj, server_address, stop_id, mission_name, auth_token)
    finish_time = node1_obj.is_box_stopped(mission_name)
    return [mission_name, finish_time - stop_time]


def create_api(request_obj, data, header, url):
    response = request_obj.call('post', url, data=json.dumps(data), headers=header)
    try:
        response_json = response.json()
    except Exception as e:
        if "Expecting value: line 1 column 1 (char 0)" in str(e):
            logger.warning("The response: {}".format(response.content.decode()))
            logger.warning("The data happened error: {}".format(data))
            raise e

    if response_json['code'] == 200:
        logger.info("Use the <{}> done !".format(url))
        return response.elapsed.total_seconds()
    else:
        raise Exception("Use the <{}> failed, the error messages are [{}]".format(url, response_json))


def list_api(request_obj, header, url):
    response = request_obj.call('get', url, headers=header)
    try:
        response_json = response.json()
    except Exception as e:
        if "Expecting value: line 1 column 1 (char 0)" in str(e):
            logger.warning("The response: {}".format(response.content.decode()))
            raise e

    if response_json['code'] == 200:
        logger.info("List by <{}> done !".format(url))
        return response.elapsed.total_seconds()
    else:
        raise Exception("List by <{}> failed, the error messages are [{}]".format(url, response_json))


def update_api(request_obj, data, header, url):
    response = request_obj.call('put', url, data=json.dumps(data), headers=header)

    try:
        response_json = response.json()
    except Exception as e:
        if "Expecting value: line 1 column 1 (char 0)" in str(e):
            logger.warning(response.content.decode())
            raise e

    if response_json['code'] == 200:
        logger.info("Use the <{}> done !".format(url))
        return response.elapsed.total_seconds()
    else:
        raise Exception("Use the <{}> failed, the error messages are [{}]".format(url, response_json))


def delete_api(request_obj, header, url, data=None):
    if data:
        response = request_obj.call('delete', url, headers=header, data=json.dumps(data))
    else:
        response = request_obj.call('delete', url, headers=header)
    try:
        response_json = response.json()
    except Exception as e:
        if "Expecting value: line 1 column 1 (char 0)" in str(e):
            logger.warning("The response: {}".format(response.content.decode()))
            logger.warning("The url happened error: {}".format(url))
            raise e

    if response_json['code'] == 200:
        logger.info("Use the <{}> done !".format(url))
        return response.elapsed.total_seconds()
    else:
        raise Exception("Use the <{}> failed, the error messages are [{}]".format(url, response_json))


def api_table_create(mysql_obj, db, api_table_name):
    sql = """create table if not exists {0}.{1} (
                    api VARCHAR(255), 
                    take_time double,
                    c_time DATETIME)""".format(db, api_table_name)
    mysql_obj.run_sql_cmd(sql)


@retry(120, 5)
def is_app_running(request_obj, app_name, header, url):
    app_data = {
        "applicationName": app_name
    }
    response = request_obj.call('post', url, data=json.dumps(app_data), headers=header)
    try:
        response_json = response.json()
    except Exception as e:
        if "Expecting value: line 1 column 1 (char 0)" in str(e):
            logger.warning("The response: {}".format(response.content.decode()))
            logger.warning("The data happened error: {}".format(app_data))
            raise e

    if response_json['code'] == 200:
        if response_json['data']['applicationStatus'] != "running":
            raise Exception("The {}'s status is still {}".format(app_name, response_json['data']['applicationStatus']))
    else:
        raise Exception("Use the <{}> failed, the error messages are [{}]".format(url, response_json))


@retry(120, 5)
def is_forward_set_success(request_obj, app_name, header, url):
    app_data = {
        "applicationName": app_name
    }
    response = request_obj.call('post', url, data=json.dumps(app_data), headers=header)
    try:
        response_json = response.json()
    except Exception as e:
        if "Expecting value: line 1 column 1 (char 0)" in str(e):
            logger.warning("The response: {}".format(response.content.decode()))
            logger.warning("The data happened error: {}".format(app_data))
            raise e

    if response_json['code'] == 200:
        if response_json['data']['accessAddress'] == "未设置":
            raise Exception("The {}'s forward set fail {}".format(app_name, response_json['data']['applicationStatus']))
    else:
        raise Exception("Use the <{}> failed, the error messages are [{}]".format(url, response_json))


@retry(150, 2)
def is_forward_not_exist(request_obj, app_name, header, url):
    app_data = {
        "applicationName": app_name
    }
    response = request_obj.call('post', url, data=json.dumps(app_data), headers=header)
    try:
        response_json = response.json()
    except Exception as e:
        if "Expecting value: line 1 column 1 (char 0)" in str(e):
            logger.warning("The response: {}".format(response.content.decode()))
            logger.warning("The data happened error: {}".format(app_data))
            raise e

    if response_json['code'] == 200:
        if response_json['data']['accessAddress'] != "未设置":
            raise Exception("The {}'s forward is still exist {}".format(app_name,
                                                                        response_json['data']['applicationStatus']))
    else:
        raise Exception("Use the <{}> failed, the error messages are [{}]".format(url, response_json))


@retry(120, 5)
def is_app_not_exist(request_obj, app_name, header, url):
    app_data = {
        "applicationName": app_name
    }
    response = request_obj.call('post', url, data=json.dumps(app_data), headers=header)
    try:
        response_json = response.json()
    except Exception as e:
        if "Expecting value: line 1 column 1 (char 0)" in str(e):
            logger.warning("The response: {}".format(response.content.decode()))
            logger.warning("The data happened error: {}".format(app_data))
            raise e

    if response_json['code'] == 404:
        if response_json['data']['boxes']:
            raise Exception("The {} is still exist".format(app_name))
    elif response_json['code'] == 200:
        raise Exception("The {} is still exist".format(app_name))
    else:
        raise Exception("Use the <{}> failed, the error messages are [{}]".format(url, response_json))


@retry(120, 5)
def is_appmatrix_running(request_obj, appmatrix_name, header, url):
    response = request_obj.call('get', url, headers=header)
    try:
        response_json = response.json()
    except Exception as e:
        if "Expecting value: line 1 column 1 (char 0)" in str(e):
            logger.warning("The response: {}".format(response.content.decode()))
            raise e

    if response_json['code'] == 200:
        if response_json['data']['status'] != "running":
            raise Exception("The appmatrix {}'s status is still {}".format(appmatrix_name,
                                                                           response_json['data']['status']))
    else:
        raise Exception("Use the <{}> failed, the error messages are [{}]".format(url, response_json))


@retry(120, 5)
def is_application_not_exist(request_obj, app_name, header, url):
    response = request_obj.call('get', url, headers=header)
    try:
        response_json = response.json()
    except Exception as e:
        if "Expecting value: line 1 column 1 (char 0)" in str(e):
            logger.warning("The response: {}".format(response.content.decode()))
            raise e

    if response_json['code'] == 404:
        if "not found" not in response_json['message']:
            raise Exception("The {} is still exist".format(app_name))
    elif response_json['code'] == 200:
        raise Exception("The {} is still exist".format(app_name))
    else:
        raise Exception("Use the <{}> failed, the error messages are [{}]".format(url, response_json))


@retry(120, 5)
def is_mission_running(request_obj, mission_name, header, url):
    response = request_obj.call('get', url, headers=header)
    try:
        response_json = response.json()
    except Exception as e:
        if "Expecting value: line 1 column 1 (char 0)" in str(e):
            logger.warning("The response: {}".format(response.content.decode()))
            raise e

    if response_json['code'] == 200:
        if response_json['data']['missionStatus'] != "running" or response_json['data']['missionStatus'] != "completed":
            raise Exception("The mission {}'s status is still {}".format(mission_name,
                                                                         response_json['data']['missionStatus']))
    else:
        raise Exception("Use the <{}> failed, the error messages are [{}]".format(url, response_json))


@retry(120, 5)
def check_cronmission_status(request_obj, cronmission_name, header, url, status='running'):
    cronmission_data = {
        "cronMissionName": cronmission_name,
        "page": 1,
        "size": 10
    }

    response = request_obj.call('post', url, data=json.dumps(cronmission_data), headers=header)
    try:
        response_json = response.json()
    except Exception as e:
        if "Expecting value: line 1 column 1 (char 0)" in str(e):
            logger.warning("The response: {}".format(response.content.decode()))
            raise e

    if response_json['code'] == 200:
        if response_json['data']['cronMissionPhase'] != status:
            raise Exception("The cronmission {}'s status is still {}".format(cronmission_name,
                                                                             response_json['data']['cronMissionPhase']))
    else:
        raise Exception("Use the <{}> failed, the error messages are [{}]".format(url, response_json))


@retry(120, 5)
def is_cronmission_not_exist(request_obj, cronmission_name, header, url):
    cronmission_data = {
        "cronMissionName": cronmission_name,
        "page": 1,
        "size": 10
    }

    response = request_obj.call('post', url, data=json.dumps(cronmission_data), headers=header)
    try:
        response_json = response.json()
    except Exception as e:
        if "Expecting value: line 1 column 1 (char 0)" in str(e):
            logger.warning("The response: {}".format(response.content.decode()))
            raise e

    if response_json['code'] == 404:
        if "not found" not in response_json['message']:
            raise Exception("The {} is still exist".format(cronmission_name))
    elif response_json['code'] == 200:
        raise Exception("The {} is still exist".format(cronmission_name))
    else:
        raise Exception("Use the <{}> failed, the error messages are [{}]".format(url, response_json))


@retry(120, 5)
def is_apparafile_exist(request_obj, apparafile_name, header, url, check_exist=True):
    response = request_obj.call('get', url, headers=header)
    try:
        response_json = response.json()
    except Exception as e:
        if "Expecting value: line 1 column 1 (char 0)" in str(e):
            logger.warning("The response: {}".format(response.content.decode()))
            raise e

    if response_json['code'] == 200:
        if check_exist:
            if response_json['data']['list']:
                pass
            else:
                raise Exception("The {} is not exist".format(apparafile_name))
        else:
            if response_json['data']['list']:
                raise Exception("The {} is still exist".format(apparafile_name))
            else:
                pass
    else:
        raise Exception("Use the <{}> failed, the error messages are [{}]".format(url, response_json))


def check_data(request_obj, before_data, header, url, request_data=None):
    if request_data:
        response = request_obj.call('post', url, headers=header, data=json.dumps(request_data))
    else:
        response = request_obj.call('get', url, headers=header)
    try:
        response_json = response.json()
    except Exception as e:
        if "Expecting value: line 1 column 1 (char 0)" in str(e):
            logger.warning("The response: {}".format(response.content.decode()))
            raise e

    if response_json['code'] == 200:
        if before_data == response_json['data']['data']:
            pass
        else:
            raise Exception("Appear data error,before is <{}>, current is <{}>".format(before_data,
                                                                                       response_json['data']['data']))
    else:
        raise Exception("Use the <{}> failed, the error messages are [{}]".format(url, response_json))


def get(request_obj, url, header, param=None):
    response = request_obj.call('get', url, headers=header, param=param)
    response_json = None
    try:
        response_json = response.json()
    except Exception as e:
        if "Expecting value: line 1 column 1 (char 0)" in str(e):
            logger.warning("The response: {}".format(response.content.decode()))
            raise e

    if response_json['code'] == 200:
        logger.info("Use the <{}> done !".format(url))
        return response_json, response.elapsed.total_seconds()
    else:
        raise Exception("Use the <{}> failed, the error messages are [{}]".format(url, response_json))


def create(request_obj, data, header, url):
    response = request_obj.call('post', url, data=json.dumps(data), headers=header)
    response_json = None
    try:
        response_json = response.json()
        logger.debug(response_json)
    except Exception as e:
        if "Expecting value: line 1 column 1 (char 0)" in str(e):
            logger.warning("The response: {}".format(response.content.decode()))
            logger.warning("The data happened error: {}".format(data))
            raise e

    if response_json['code'] == 200:
        logger.info("Use the <{}> done !".format(url))
        return response_json, response.elapsed.total_seconds()
    else:
        raise Exception("Use the <{}> failed, the error messages are [{}]".format(url, response_json))


def modify(request_obj, data, header, url):
    response = request_obj.call('post', url, data=json.dumps(data), headers=header)
    response_json = None
    try:
        response_json = response.json()
        logger.debug(response_json)
    except Exception as e:
        if "Expecting value: line 1 column 1 (char 0)" in str(e):
            logger.warning("The response: {}".format(response.content.decode()))
            logger.warning("The data happened error: {}".format(data))
            raise e

    if response_json['code'] == 200:
        logger.info("Use the <{}> done !".format(url))
        return response_json, response.elapsed.total_seconds()
    else:
        raise Exception("Use the <{}> failed, the error messages are [{}]".format(url, response_json))


def update(request_obj, data, header, url):
    response = request_obj.call('put', url, data=json.dumps(data), headers=header)
    response_json = None
    try:
        response_json = response.json()
    except Exception as e:
        if "Expecting value: line 1 column 1 (char 0)" in str(e):
            logger.warning("The response: {}".format(response.content.decode()))
            logger.warning("The data happened error: {}".format(data))
            raise e

    if response_json['code'] == 200:
        logger.info("Use the <{}> done !".format(url))
        return response_json, response.elapsed.total_seconds()
    else:
        raise Exception("Use the <{}> failed, the error messages are [{}]".format(url, response_json))


def delete(request_obj, url, header, data=None, param=None):
    response = request_obj.call('delete', url, data=json.dumps(data), headers=header, param=param)
    response_json = None
    try:
        response_json = response.json()
    except Exception as e:
        if "Expecting value: line 1 column 1 (char 0)" in str(e):
            logger.warning("The response: {}".format(response.content.decode()))
            logger.warning("The data happened error: {}".format(data))
            raise e

    if response_json['code'] == 200:
        logger.info("Use the <{}> done !".format(url))
        return response_json, response.elapsed.total_seconds()
    else:
        raise Exception("Use the <{}> failed, the error messages are [{}]".format(url, response_json))


def upload(request_obj, url, header, file):
    response = request_obj.call('post', url, file=file, headers=header)
    response_json = None
    try:
        response_json = response.json()
        logger.debug(response_json)
    except Exception as e:
        if "Expecting value: line 1 column 1 (char 0)" in str(e):
            logger.warning("The response: {}".format(response.content.decode()))
            raise e

    if response_json['code'] == 200:
        logger.info("Use the <{}> done !".format(url))
        return response_json, response.elapsed.total_seconds()
    else:
        raise Exception("Use the <{}> failed, the error messages are [{}]".format(url, response_json))


def download(request_obj, url, header, param):
    response = request_obj.call('get', url, headers=header, param=param)
    if response.status_code == 200:
        logger.info("Use the <{}> done, file download success!".format(url))
        return response.elapsed.total_seconds()
    else:
        raise Exception("Use the <{}> failed, file download fail!".format(url))


def online_product_image(request_obj, url, header, param, file):
    response = request_obj.call('post', url, param=param, file=file, headers=header)
    response_json = None
    try:
        response_json = response.json()
    except Exception as e:
        if "Expecting value: line 1 column 1 (char 0)" in str(e):
            logger.warning("The response: {}".format(response.content.decode()))
            raise e

    if response_json['code'] == 200:
        logger.info("Use the <{}> done !".format(url))
        return response_json, response.elapsed.total_seconds()
    else:
        raise Exception("Use the <{}> failed, the error messages are [{}]".format(url, response_json))
