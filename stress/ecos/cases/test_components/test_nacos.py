import pytest
import random
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from libs.log_obj import LogObj
from libs.nacos_obj import NacosObj
from utils.util import generate_random_int, generate_random_string

logger = LogObj().get_logger()


@pytest.fixture(scope='session')
def nacos_test_data(component_test_data):
    return component_test_data("nacos")


@pytest.fixture(scope='session')
def nacos_obj(nacos_test_data):
    return NacosObj(nacos_test_data['server_address'], nacos_test_data['namespace'], nacos_test_data['username'],
                    nacos_test_data['password'])


@pytest.fixture(scope='function')
def nacos_configs_data(nacos_test_data):
    config_datas = []
    for quantity in range(nacos_test_data['config_quantity']):
        data_id = generate_random_string(15, 10)
        group = generate_random_string(6, 3)
        content = generate_random_string(1000, 500)
        config_datas.append({'data_id': data_id, 'group': group, 'content': content})
    return config_datas


@pytest.fixture(scope='function')
def random_data_id_with_groups(nacos_obj):
    data_id_with_groups = nacos_obj.get_data_id_with_groups
    random_data_id_with_groups = random.sample(data_id_with_groups, random.randint(1, len(data_id_with_groups)+1))

    return random_data_id_with_groups


@pytest.fixture(scope='function')
def nacos_register_instances_info(nacos_test_data):
    nacos_register_instances_info = []
    for quantity in range(nacos_test_data['instance_quantity']):
        service_name = generate_random_string(15, 10)
        ip = '{}.{}.{}.{}'.format(str(generate_random_int(255, 1)), str(generate_random_int(255, 1)),
                                  str(generate_random_int(255, 1)), str(generate_random_int(255, 1)))
        port = generate_random_int(30000)
        cluster = generate_random_string(6, 3)
        metadata = {
            generate_random_string(6, 3): generate_random_string(20, 10)
        }
        nacos_register_instances_info.append({'service_name': service_name, 'ip': ip, 'port': port, 'cluster': cluster,
                                              'metadata': metadata})

    return nacos_register_instances_info


def test_nacos_config_push(nacos_obj, nacos_configs_data):
    test_nacos_config_push.__doc__ = 'Test start, nacos config push stress test !'
    logger.info(test_nacos_config_push.__doc__)

    logger.info("Start nacos config push !")
    start_time = datetime.datetime.now()

    pool = ThreadPoolExecutor(max_workers=20)
    futures = []
    for nacos_config in nacos_configs_data:
        futures.append(pool.submit(nacos_obj.publish_config, nacos_config['data_id'], nacos_config['group'],
                                   nacos_config['content'], 'text'))
    pool.shutdown()
    for future in as_completed(futures):
        future.result()

    end_time = datetime.datetime.now()
    take_time = end_time - start_time
    logger.info(f'Nacos push {len(nacos_configs_data)} configs take time: {take_time}')
    logger.info("Nacos config push successfully !")


def test_nacos_config_search(nacos_obj, random_data_id_with_groups):
    test_nacos_config_search.__doc__ = 'Test start, nacos config search stress test !'
    logger.info(test_nacos_config_search.__doc__)

    logger.info("Start nacos config search !")
    start_time = datetime.datetime.now()

    pool = ThreadPoolExecutor(max_workers=20)
    futures = []
    for data_id_with_group in random_data_id_with_groups:
        futures.append(pool.submit(nacos_obj.search_config, data_id_with_group['data_id'], data_id_with_group['group']))
    pool.shutdown()
    for future in as_completed(futures):
        future.result()

    end_time = datetime.datetime.now()
    take_time = end_time - start_time
    logger.info(f'Nacos search {len(random_data_id_with_groups)} configs take time: {take_time}')
    logger.info("Nacos config search successfully !")


def test_nacos_instance_register(nacos_obj, nacos_register_instances_info):
    test_nacos_instance_register.__doc__ = 'Test start, nacos instance register stress test !'
    logger.info(test_nacos_instance_register.__doc__)

    logger.info("Start register nacos instance !")
    start_time = datetime.datetime.now()

    pool = ThreadPoolExecutor(max_workers=20)
    futures = []
    for nacos_register_instance_info in nacos_register_instances_info:
        futures.append(pool.submit(nacos_obj.register_instance, nacos_register_instance_info['service_name'],
                                   nacos_register_instance_info['ip'], nacos_register_instance_info['port'],
                                   nacos_register_instance_info['cluster'], nacos_register_instance_info['metadata']))
    pool.shutdown()
    for future in as_completed(futures):
        future.result()

    end_time = datetime.datetime.now()
    take_time = end_time - start_time
    logger.info(f'register {len(nacos_register_instances_info)} nacos instances take time: {take_time}')
    logger.info("Register nacos instance successfully !")
