#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from utils.decorator import print_for_call
import json
from superelasticsearch import SuperElasticsearch
import superelasticsearch
from elasticsearch.exceptions import TransportError
from libs.log_obj import LogObj
from elasticsearch import serializer
from utils.decorator import lock

# =============================
# --- Global
# =============================
logger = LogObj().get_logger()
ES_CONN_TIMEOUT = 300
ES_OPERATION_TIMEOUT = '60m'


class MyJSONSerializer(serializer.JSONSerializer):
    def default(self, data):
        if isinstance(data, set):
            return list(data)
        if isinstance(data, bytes):
            return str(data, encoding='utf-8')
        return serializer.JSONSerializer.default(self, data)


superelasticsearch.json = MyJSONSerializer()


class ESObj(object):
    _session = None
    target_index = None
    update_index_list = None

    def __init__(self, ip_list, port, user=None, password=None):
        self.ips = ip_list
        self.port = port
        self.user = user
        self.password = password

    def set_target_index(self, index_name):
        self.target_index = index_name

    def set_update_index_list(self, index_name_list):
        self.update_index_list = index_name_list

    @property
    @lock
    def session(self):
        if self._session is None:
            logger.info('Connect ES {0}:{1}, es user is {2}, es password is {3}'.format(self.ips, self.port, self.user,
                                                                                        self.password))
            if self.user and self.password:
                self._session = SuperElasticsearch(self.ips, timeout=ES_CONN_TIMEOUT,
                                                   http_auth=(self.user, self.password), port=self.port,
                                                   serializer=MyJSONSerializer())
            else:
                self._session = SuperElasticsearch(self.ips, port=self.port, timeout=ES_CONN_TIMEOUT,
                                                   serializer=MyJSONSerializer())

        return self._session

    @property
    def ping(self):
        return self.session.ping()

    @property
    def health(self):
        return self.ping and 'red' not in self.session.cat.health().split()[3]

    @property
    def status(self):
        return self.session.cat.health().split()[3]

    @property
    def nodes(self):
        nodes = []
        for node_info in self.nodes_info:
            nodes.append(node_info['ip'])

        return nodes

    @property
    def nodes_info(self):
        nodes_info = []
        for node_info in self.session.cat.nodes().strip().split('\n'):
            tmp_list = node_info.split()
            node_ip = tmp_list[0]
            node_name = tmp_list[-1]
            if tmp_list[-2] == '-':
                node_type = 'data'
            elif tmp_list[-2] == '*':
                node_type = 'master'
            tmp_info = dict()
            tmp_info['ip'] = node_ip
            tmp_info['name'] = node_name
            tmp_info['type'] = node_type
            nodes_info.append(tmp_info)

        return nodes_info

    @property
    def indices_name(self):
        es_indices_names = []
        for es_indices in self.session.cat.indices().strip().split('\n'):
            es_indices_names.append(es_indices.split()[2])

        return es_indices_names

    def get_cat_index_info(self, index_name=None):
        cat_result_list = self.session.cat.indices(index=index_name, v=True).split('\n')
        index_info = dict()
        if cat_result_list:
            if index_name is None:
                index_info = []
                for i in range(1, len(cat_result_list)):
                    index_info.append(dict(zip(cat_result_list[0].split(), cat_result_list[i].split())))
            else:
                index_info = dict(zip(cat_result_list[0].split(), cat_result_list[1].split()))

        return index_info

    @property
    def cluster_allocation_explain(self):
        response = self.session.cluster.allocation_explain()

        return response

    def cluster_state(self, index_name=None):
        response = self.session.cluster.state(index=index_name)

        return response

    def get_cluster_settings(self):
        response = self.session.cluster.get_settings()

        return response

    def put_cluster_settings(self, body):
        response = self.session.cluster.put_settings(body=body)

        return response

    def create_index(self, index_name, index_settings=None):
        if self.is_index_exist(index_name):
            logger.debug('{0} index exist!'.format(index_name))
            return True

        logger.debug("The target index {} does not exist, create it first".format(index_name))
        logger.debug("Start creating index {} {}".format(index_name, index_settings))
        try:
            rtn = self.session.indices.create(index_name, index_settings)
            logger.debug("Create index {0} finished".format(index_name))
            return rtn
        except TransportError as e:
            logger.debug(e)
            if 'exists' in e.info:
                return True
            raise e

    def create_template(self, template_name, index_settings):
        logger.debug("Start creating template {} {}".format(template_name, index_settings))
        try:
            return self.session.indices.put_template(template_name, index_settings, master_timeout=ES_OPERATION_TIMEOUT)
        except TransportError as e:
            logger.debug(e)
            if 'exists' in e.info:
                return True
            raise e

    def does_template_exist(self, template_name):
        return self.session.indices.exists_template(template_name)

    def delete_index(self, index_name):
        return self.session.indices.delete(index_name)

    def is_index_exist(self, index_name):
        return self.session.indices.exists(index_name)

    def get_all_types(self, index_name):
        return self.session.indices.get_mapping(index_name)[index_name]['mappings'].keys()

    def delete_doc_type(self, index_name, doc_type):
        return self.session.delete_by_query(index_name,
                                            {"query": {"match_all": {}}},
                                            doc_type=doc_type,
                                            wait_for_completion=True,
                                            refresh=True)

    def delete_match_docs(self, index_name, doc_type, condition_dict_list):
        logger.debug("Delete docs where index_name: {}, doc_type: {} and conditions: {}".format(
            index_name, doc_type, json.dumps(condition_dict_list))
        )
        search_body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            condition_dict.get('type_', 'term'): {
                                condition_dict['key']: condition_dict['value']
                            }
                        } for condition_dict in condition_dict_list
                    ]
                }
            }
        }

        if doc_type:
            return self.session.delete_by_query(index_name,
                                                search_body,
                                                doc_type=doc_type,
                                                wait_for_completion=True,
                                                refresh=True,
                                                conflicts='proceed')
        else:
            return self.session.delete_by_query(index_name,
                                                search_body,
                                                wait_for_completion=True,
                                                refresh=True,
                                                conflicts='proceed')

    def index_doc(self, index_name, doc_data_dict):
        return self.session.index(
            index=index_name,
            # doc_type=doc_type,
            body=doc_data_dict,
            timeout=ES_OPERATION_TIMEOUT
        )

    def create_doc(self, index_name, doc_type, doc_data_dict, id_):
        return self.session.index(
            id=id_,
            index=index_name,
            doc_type=doc_type,
            body=doc_data_dict,
            timeout=ES_OPERATION_TIMEOUT
        )

    def bulk_create_docs(self, index_name, doc_data_dict_list, max_bulk_size=20000, refresh=True):
        num = 0
        pre_num = 0
        bulk = None
        #         for doc_data_dict in generate_docs(docs_num):
        for doc_data_dict in doc_data_dict_list:
            num += 1
            if num % max_bulk_size == 1:
                bulk = self.session.bulk_operation()

            bulk.index(
                index=index_name,
                #doc_type='doc',
                body=doc_data_dict
            )

            if num % max_bulk_size == 0:
                logger.debug(f"Start sending from items {pre_num} to {num} to {index_name}]")
                pre_num = num
                if bulk.execute(timeout=ES_OPERATION_TIMEOUT, refresh=refresh):
                    logger.debug("Finished sending these items")
                else:
                    return False
        logger.debug("Total file number: {}".format(num))
        if num != pre_num:
            logger.debug("Start sending from items {} to {} to ElasticSearch Server".format(pre_num, num))
            rc = bulk.execute(timeout=ES_OPERATION_TIMEOUT, refresh=refresh)
            if rc:
                logger.debug("Finished")
            return rc
        else:
            return False

    def bulk_update_docs(self, index_name, doc_type, doc_data_dict_list, max_bulk_size=2000, refresh=True,
                         index_if_not_exist=True):
        num = 0
        pre_num = 0
        bulk = None
        for doc_data_dict in doc_data_dict_list:
            num += 1
            if num % max_bulk_size == 1:
                bulk = self.session.bulk_operation()
            body = {
                "doc": doc_data_dict,
                "doc_as_upsert": True
            } if index_if_not_exist else {
                "doc": doc_data_dict
            }

            if 'to_delete' in doc_data_dict:
                bulk.delete(
                    id=doc_data_dict['id_'],
                    index=index_name,
                    doc_type='doc'
                )
            else:
                bulk.update(
                    id=doc_data_dict.pop("id_"),
                    index=index_name,
                    doc_type='doc',
                    body=body
                )

            if num % max_bulk_size == 0:
                logger.debug("Start sending from items {} to {} to ElasticSearch Server".format(pre_num, num))
                pre_num = num
                if bulk.execute(timeout=ES_OPERATION_TIMEOUT, refresh=refresh):
                    logger.debug("Finished sending these items")
                else:
                    return False
        logger.debug("Total file number: {}".format(num))
        if num != pre_num:
            logger.debug("Start sending from items {} to {} to ElasticSearch Server".format(pre_num, num))
            rc = bulk.execute(timeout=ES_OPERATION_TIMEOUT, refresh=refresh)
            if rc:
                logger.debug("Finished")
            return rc
        else:
            return False

    def refresh(self, index_name=None):
        return self.session.indices.refresh(index_name)

    def flush(self, index_name=None, wait_if_ongoing=True):
        return self.session.indices.flush(index=index_name, wait_if_ongoing=wait_if_ongoing)

    def thread_pool(self, thread_type=None):
        return self.session.cat.thread_pool(thread_type).split("\n")

    @property
    def index_queue_num(self):
        queue_num = 0
        for node_bulk_thread_info in self.thread_pool(thread_type="bulk"):
            if node_bulk_thread_info:
                logger.debug(node_bulk_thread_info)
                queue_num += int(node_bulk_thread_info.split()[3])
        return queue_num

    def delete_doc(self):
        pass

    def search(self, index=None, body=None, scroll=None):
        if body is None:
            body = {"query": {"match_all": {}}, 'size': 15}

        rtn = self.session.search(index=index, body=body, scroll=scroll)
        if index:
            logger.info('Search from {index} take times: {time}ms'.format(index=index, time=rtn['took']))
            logger.info('Search from {index} hits docs: {num}'.format(index=index, num=rtn['hits']['total']))
        else:
            logger.info('Search take times: {time}ms'.format(time=rtn['took']))
            logger.info('Search hits docs: {num}'.format(num=rtn['hits']['total']))

        return rtn

    @print_for_call
    def clear_cache(self, index=None):
        return self.session.indices.clear_cache(index=index)

    def stats(self, index=None):
        return self.session.indices.stats(index=index)

    def count(self, index=None, doc_type=None, body=None):
        return self.session.count(index=index, doc_type=doc_type, body=body)

    def scroll(self, scroll_id, scroll='30m'):
        return self.session.scroll(scroll_id=scroll_id, scroll=scroll)


if __name__ == "__main__":
    es_ips = ['192.168.2.5']
    es_port = 32222
    es_user = 'root'
    es_pwd = 'password'
    es_obj = ESObj(es_ips, es_port, es_user, es_pwd)




#     body = {"transient" :{"cluster.routing.allocation.enable": "none"}}
#     print(es_obj.get_cluster_settings())

#     es_obj.delete_index('vizion--onlinekibana--.kibanaauthapp3_4vizion--onlinekibana--')
# #     print(es_obj.es_indices_names)
#     from cases.vizion.tools import generate_random_string
#     for _ in range(5):
#         index = 'pzindex-1'
# #         print(es_obj.clear_cache(index=index))
#
#         pattern = "*{str}*".format(str=generate_random_string(5))
#         print(pattern)
#
#         body = {
#           "query": {
#             "bool": {
#               "must": {
#                 "bool": {
#                   "should": [
#                     {
#                       "wildcard": {
#                         "file": {
#                           "wildcard": pattern
#                         }
#                       }
#                     }
#                   ]
#                 }
#               }
#             }
#           }
#         }
#
#         es_obj.search(index=index, body=body)
#         logger.debug(es_obj.stats(index))

