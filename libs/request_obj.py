# !/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import urllib3
import ssl
from libs.log_obj import LogObj

logger = LogObj().get_logger()

ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings()


class RequstObj(object):
    def call(self, req_method, req_url, param=None, data=None, file=None, headers=None):
        """
        call rest api
        :param req_method: eg: POST,PUT,DELETE,GET
        :param req_url:
        :param data:
        :param headers:
        :return:
        """

        message = '{0} {1}'.format(req_method.upper(), req_url)
        message = '{0}\n{1}'.format(message, data) if data else message
        logger.info(message)

        try:
            response = requests.request(req_method, req_url, headers=headers, params=param, data=data, files=file,
                                        verify=False)
            return response
        except Exception as e:
            raise e


if __name__ == '__main__':
    import json
    import jsonpath

    url = 'http://192.168.5.8:3306'
    request_obj = RequstObj()
    response = request_obj.call('get', url)
    print(response)
