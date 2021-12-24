import pytest
from libs.log_obj import LogObj
from libs.redis_obj import RedisObj
from utils.util import generate_random_string, generate_doc


logger = LogObj().get_logger()


@pytest.fixture(scope='session')
def redis_test_data(component_test_data):
    return component_test_data("redis")


@pytest.fixture(scope='session')
def redis_obj(redis_test_data):
    return RedisObj(redis_test_data['redis_ip'], redis_test_data['redis_port'], redis_test_data['redis_pwd'])


@pytest.fixture(scope='function')
def redis_docs(redis_test_data):
    templates = []
    docs = dict()
    for num in range(1, redis_test_data['redis_data_quantity'] + 1):
        docs[generate_random_string(20)] = str(generate_doc())
        if len(docs) == 500 or num == redis_test_data['redis_data_quantity']:
            templates.append(docs)
            docs = {}
    return templates


def test_redis(redis_obj, redis_docs):
    test_redis.__doc__ = 'Test start, redis stress test !'
    logger.info(test_redis.__doc__)
    redis_obj.mutil_write_redis_data(redis_docs)

    redis_obj.redis_ping_ok()
