# -*- coding: utf-8 -*-

# @File    : test_zookeeper.py
# @Date    :  2021-09-27 下午5:35
# @Author  : wangkun

import pytest
import datetime
import os
from libs.log_obj import LogObj
from libs.zookeeper_obj import ZooKeeperObj
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.util import generate_random_string


logger = LogObj().get_logger()


@pytest.fixture(scope='session')
def zk_test_data(component_test_data):
    return component_test_data("zookeeper")


@pytest.fixture(scope='session')
def zookeeper_obj(zk_test_data):
    return ZooKeeperObj(zk_test_data['zk_hosts'])


def test_zookeeper(zookeeper_obj, zk_test_data):
    test_zookeeper.__doc__ = 'Test start, zookeeper stress test !'
    logger.info(test_zookeeper.__doc__)

    start_time = datetime.datetime.now()

    pool = ThreadPoolExecutor(max_workers=20)
    futures = []

    for node in range(zk_test_data['node_quantity']):
        futures.append(pool.submit(zookeeper_obj.create_multiple_part_node, os.path.join(zk_test_data['zk_path_name'],
                                                                                         generate_random_string(15, 6)),
                                   bytes(generate_random_string(zk_test_data['max_node_value'],
                                                                zk_test_data['min_node_value']).encode("utf8"))))

    pool.shutdown()
    for future in as_completed(futures):
        future.result()

    end_time = datetime.datetime.now()
    take_time = end_time - start_time

    logger.info("Create {} nodes take time: {} s !".format(zk_test_data['node_quantity'], take_time))
    logger.info("Zookeeper node stress successfully !")
