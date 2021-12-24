from utils.decorator import retry, print_for_call
from utils.util import txt_w, get_file_md5
from libs.log_obj import LogObj
from libs.request_obj import RequstObj
import json
import os
import random

logger = LogObj().get_logger()


def check_health(node1_obj):
    node1_obj.is_nodes_ready()
    node1_obj.is_etcd_ok()
    node1_obj.is_pods_running()
    is_paas_web_working(node1_obj.ip)


@retry(tries=120, delay=5)
@print_for_call
def is_paas_web_working(ip):
    request_obj = RequstObj()
    url = 'http://{0}:30000/authnew/service/token'.format(ip)
    data = '{"username": "admin", "password": "admin12345"}'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Utc-Date': '1630048970'}
    response = request_obj.call('post', url, data=data, headers=headers)
    if response.status_code != 200:
        logger.error('Response code is {0}, response text is {1}!'.format(response.status_code, response.text))
        raise Exception('PAAS {0} can not access!'.format(ip))
    else:
        logger.info('PAAS {0} access success!'.format(ip))

@retry(tries=120, delay=30)
def is_index_green(es_obj, index_name):
    index_info = es_obj.get_cat_index_info(index_name=index_name)
    if len(es_obj.nodes) > 2:
        if 'green' not in index_info['health']:
            logger.error(json.dumps(index_info, indent=4))
            raise Exception('Index {target} exception occured!'.format(target=index_name))
    else:
        if 'yellow' not in index_info['health'] and 'green' not in index_info['health']:
            logger.error(json.dumps(index_info, indent=4))

            cluster_allocation_explain = es_obj.cluster_allocation_explain

            if 'index' in es_obj.cluster_allocation_explain and cluster_allocation_explain['index'] == index_name:
                logger.warning(cluster_allocation_explain['unassigned_info']['details'])

            raise Exception('Index {target} exception occured!'.format(target=index_name))

    logger.debug(json.dumps(index_info, indent=4))


def minio_files(file_path, file_quantity, file_min_size, file_max_size):
    minio_files = dict()
    for file in range(file_quantity):
        file_name = "gc-minio-test-{}".format(file)
        path_with_file_name = os.path.join(file_path, file_name)
        file_random_size = random.randint(file_min_size, file_max_size+1)
        txt_w(path_with_file_name, file_random_size)
        file_md5 = get_file_md5(path_with_file_name)

        minio_files[file_name] = {"file_path": path_with_file_name, "file_md5": file_md5}

    return minio_files


if __name__ == '__main__':
    pass
    # print(minio_files("/Users/wangkun/kwang_files", 10, 10, 15))
    # for i in range(100):
    #     file_pn = "./minio-stress-testminio-data-{}".format(i)
    #     try:
    #         os.remove(file_pn)
    #     except FileNotFoundError:
    #         print("nO FILE -> {}".format(file_pn))