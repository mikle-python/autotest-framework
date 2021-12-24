import pytest
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from libs.log_obj import LogObj
from stress.ecos.common.common import is_index_green
from settings.ecos_settings import gc_index_settings
from utils.util import generate_docs
from libs.es_obj import ESObj

logger = LogObj().get_logger()


@pytest.fixture(scope='session')
def es_test_data(component_test_data):
    return component_test_data("es")


@pytest.fixture(scope='session')
def es_obj():
    return ESObj(es_test_data['es_ips'], es_test_data['es_port'])


@pytest.fixture(scope='session')
def indices_name(es_obj):
    pool = ThreadPoolExecutor(max_workers=20)
    indices_name = []

    futures = []

    for i in range(es_test_data['indices_num']):
        new_index_name = '{0}-{1}'.format(es_test_data['index_name'], i)
        indices_name.append(new_index_name)
        futures.append(pool.submit(es_obj.create_index, new_index_name, gc_index_settings))

    pool.shutdown()
    for future in as_completed(futures):
        future.result()

    return indices_name


def test_es_index(es_obj, indices_name):
    test_es_index.__doc__ = 'Test start, es stress test !'
    logger.info(test_es_index.__doc__)
    start_time = datetime.datetime.now()

    pool = ThreadPoolExecutor(max_workers=20)
    futures = []
    for index_name in indices_name:
        futures.append(pool.submit(es_obj.bulk_create_docs, index_name,
                                   generate_docs(es_test_data['docs_num']), es_test_data['max_bulk_size']))
    pool.shutdown()
    for future in as_completed(futures):
        future.result()

    logger.debug("Finish index")

    end_time = datetime.datetime.now()
    take_time = end_time - start_time
    logger.info('Index take time: {time}'.format(time=take_time))

    for index_name in indices_name:
        is_index_green(es_obj, index_name)

    logger.info('Index successfully')
