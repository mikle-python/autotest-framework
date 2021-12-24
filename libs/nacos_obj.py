import nacos
from libs.log_obj import LogObj
from utils.decorator import print_for_call, retry

logger = LogObj().get_logger()


class NacosObj(object):
    _nacos_session = None

    def __init__(self, server_addresses, namespace, username, password):
        self.server_addresses = server_addresses
        self.namespace = namespace
        self.username = username
        self.password = password

    @property
    def nacos_session(self):
        if self._nacos_session is None:
            self._nacos_session = nacos.NacosClient(self.server_addresses, namespace=self.namespace,
                                                    username=self.username, password=self.password)
        return self._nacos_session

    @retry(tries=10, delay=10)
    @print_for_call
    def publish_config(self, data_id, group, content, config_type):
        if self.nacos_session.publish_config(data_id, group, content, config_type=config_type):
            logger.info(f"Add config:{data_id} to group:{group} successfully !")
        else:
            logger.warning(f"Add config:{data_id} to group:{group} fail !")
            raise Exception(f"Add config:{data_id} to group:{group} fail !")

    @retry(tries=10, delay=10)
    @print_for_call
    def search_config(self, data_id, group):
        self.nacos_session.get_config(data_id, group)
        logger.info(f"Search from dataId:{data_id} group:{group} successfully !")

    @property
    def list_configs(self):
        for _, config in self.nacos_session.get_configs(no_snapshot=True).items():
            if _ == 'pageItems':
                return config

    @property
    def get_data_id_with_groups(self):
        data_id_with_group = []
        for config in self.list_configs:
            data_id_with_group.append({'data_id': config['dataId'], 'group': config['group']})
        return data_id_with_group

    @retry(tries=5, delay=10)
    @print_for_call
    def remove_config(self, data_id, group):
        if self.nacos_session.remove_config(data_id, group):
            logger.info(f"Remove config:{data_id} from group:{group} successfully !")
        else:
            logger.warning(f"Remove config:{data_id} from group:{group} fail !")

    @retry(tries=10, delay=10)
    @print_for_call
    def register_instance(self, service_name, ip, port, cluster, metadata):
        if self.nacos_session.add_naming_instance(service_name, ip, port, cluster, metadata=metadata):
            logger.info(f"Register instance {service_name} successfully !")
        else:
            logger.warning(f"Register instance {service_name} fail !")
            raise Exception(f"Register instance {service_name} fail !")

    def query_instances(self, service_name, ip, port):
        self.nacos_session.get_naming_instance(service_name, ip, port)

    def add_watcher(self, data_id, group, cb_list):
        self.nacos_session.add_config_watchers(data_id, group, cb_list)


if __name__ == "__main__":
    SERVER_ADDRESSES = "http://192.168.2.5:31089"
    NAMESPACE = ""
    username = 'nacos'
    password = 'nacos'

    publish_config = {
        'data_id': 'test3233',
        'group': 'DEFAULT_GROUP',
        'config_type': 'text'
    }

    nacos1 = NacosObj(SERVER_ADDRESSES, NAMESPACE, username, password)
    c = nacos1.get_data_id_with_groups
    print(len(c))
    # for i in range(1, 100):
    #     nacos1.publish_config(data_id="jdust"+str(i), group='DEFAULT_GROdUP', content=u'test', config_type='text')
    # print(nacos1.list_configs())
    # # print(nacos1.register_instance("naocs-22", "10.233.104.185", 8848, 'DEFAULT', publish_config))
