#!/usr/bin/python
#coding=utf-8

import redis
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from libs.log_obj import LogObj
from utils.decorator import retry, print_for_call
from redis.exceptions import ReadOnlyError, ConnectionError

logger = LogObj().get_logger()


class RedisObj(object):
    _session = None

    def __init__(self, host, ports, password):
        self.host = host
        self.ports = ports
        self.password = password

    @property
    def session(self):
        if self._session is None:
            ports_list = self.ports.split(',')
            for port in ports_list:
                try:
                    role = redis.StrictRedis(host=self.host, port=port, password=self.password).info()['role']
                    if role == 'master':
                        self._session = redis.StrictRedis(host=self.host, port=port, password=self.password)
                        logger.info(f"Connect the redis master server with [ip:{self.host} port:{port}].")
                        break
                    else:
                        logger.warning(f"The role of redis server [ip:{self.host} port:{port}] is {role}.")
                except ConnectionError:
                    logger.warning(f"Connect the server with [ip:{self.host} port:{port}] appear ConnectionError.")
                    continue

        if self._session is None:
            raise Exception("No valid redis master get, please check the server port and update the master port!")

        return self._session

    def write_redis_single_data(self, redis_key, redis_value):
        self.session.set(redis_key, redis_value)

    @print_for_call
    def write_redis_multiple_data(self, kv):
        logger.info(f"Start insert {len(kv)} documents ...")
        try:
            self.session.mset(kv)
        except ReadOnlyError:
            self._session = None
            self.session.mset(kv)

        logger.info(f"Insert {len(kv)} documents done...")

    def mutil_write_redis_data(self, docs_info):
        futures = []
        client_pool = ThreadPoolExecutor(max_workers=50)

        start_time = datetime.datetime.now()

        logger.info(f"insert data to redis server: {self.host}")
        for doc in docs_info:
            futures.append(client_pool.submit(self.write_redis_multiple_data, doc))

        client_pool.shutdown()
        for future in as_completed(futures):
            future.result()

        logger.info(f"Finish insert data to redis server: {self.host}")
        end_time = datetime.datetime.now()
        take_time = end_time - start_time
        logger.info('Insert take time: {time}'.format(time=take_time))

    def redis_cluster_nodes(self):
        return self.session.cluster('nodes')

    @retry(tries=120, delay=30)
    @print_for_call
    def redis_ping_ok(self):
        if self.session.ping():
            logger.info("Redis server ping successfully !")
        else:
            logger.warning("Redis server ping failed !")
            raise Exception("redis server connect fail !")

    def redis_memory_stats(self):
        return self.session.memory_stats()

    def redis_db_size(self):
        print(id(self.session))
        return self.session.dbsize()

    @property
    def redis_info(self):
        print(id(self.session))
        return self.session.info()


if __name__ == '__main__':
    host = '192.168.2.5'
    port = '31975,31974,31976'
    password = 'password'
    redis_client = RedisObj(host, port, password)

    # docs = handle_docs(10000)
    # docs = {'1': '2', '2': '3'}
    # redis_client.write_redis_multiple_data(docs)
    redis_client.write_redis_multiple_data({'te2st': '{1:1}'})
