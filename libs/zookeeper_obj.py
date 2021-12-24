# -*- coding: utf-8 -*-

# @File    : zookeeper_obj.py
# @Date    :  2021-09-27 下午3:33
# @Author  : wangkun

from kazoo.client import KazooClient, KazooState
from kazoo.exceptions import NodeExistsError, NoNodeError
from libs.log_obj import LogObj
from utils.decorator import print_for_call, retry

logger = LogObj().get_logger()


class ZooKeeperObj(object):
    _zk_session = None

    def __init__(self, zk_hosts):
        self.zk_hosts = zk_hosts

    @property
    def zk_session(self):
        if self._zk_session is None:
            self._zk_session = KazooClient(hosts=self.zk_hosts)
            self._zk_session.start()

        return self._zk_session

    def state_listener(self, state):
        if state == KazooState.LOST:
            self.zk_session.start()
        elif state == KazooState.SUSPENDED:
            self.zk_session.start()
        else:
            pass

    @retry(10, 10)
    @print_for_call
    def create_node(self, path, value):
        try:
            if self.zk_session.exists(path):
                logger.warning("Node <{}> has exist , don't create again!".format(path))
            else:
                self.zk_session.create(path, value)
                logger.info("Create node <{}> success !".format(path))
        except NoNodeError:
            logger.warning("The father of node:<{}>'s has not exist , please create the father node firstly!".format(path))

    @print_for_call
    def get_node(self, path):
        try:
            data, stat = self.zk_session.get(path)
            return data.decode("utf8")
        except NoNodeError:
            logger.warning("Node <{}> not exist, please create it first !".format(path))

    def update_node(self, path, new_value):
        if self.zk_session.exists(path):
            try:
                self.zk_session.set(path, new_value)
            except TypeError:
                logger.warning("The parameter of <new_value> must be byte string, please reset it !")
        else:
            logger.warning("Node <{}> has not exist, please create it first !".format(path))

    def node_if_exist(self, path):
        return self.zk_session.exists(path)

    def del_node(self, path, recursive=False):
        return self.zk_session.delete(path, recursive=recursive)

    @retry(10, 10)
    def create_multiple_part_node(self, path, value):
        try:
            if self.zk_session.exists(path):
                logger.warning("Node <{}> has exist , don't create again!".format(path))
            else:
                if self.zk_session.ensure_path(path):
                    self.update_node(path, value)
                    logger.info("Create node <{}> success !".format(path))
                else:
                    raise Exception("Create multiple part node fail !")
        except Exception as e:
            raise e


if __name__ == "__main__":
    zk_hosts = "192.168.1.236:31777"
    import datetime
    zk = ZooKeeperObj(zk_hosts)
    start_time = datetime.datetime.now()
    for i in range(1, 10):
        zk.create_multiple_part_node("/h/22/{}".format(i), b"hhh")
    end_time = datetime.datetime.now()

    print("cost is :{}".format(end_time-start_time))