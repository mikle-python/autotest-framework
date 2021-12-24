# !/usr/bin/env python
# -*- coding: utf-8 -*-

import etcd3
from utils.decorator import lock
from libs.log_obj import LogObj


logger = LogObj().get_logger()


class EtcdObj(object):
    _session = None

    def __init__(self, ip, port, ca_cert=None, cert_key=None, cert_cert=None):
        self.ip = ip
        self.port = port
        self.ca_cert = ca_cert
        self.cert_key = cert_key
        self.cert_cert = cert_cert

    @property
    @lock
    def session(self):
        if self._session is None:
            self._session = etcd3.client(host=self.ip, port=self.port, ca_cert=self.ca_cert,
                                         cert_key=self.cert_key, cert_cert=self.cert_cert)
        return self._session

    @property
    def members(self):
        return self.session.members

    def get(self, key):
        return self.session.get(key)

    def watch(self, key):
        return self.session.watch(key)

    def watch_once(self, key, timeout=None):
        return self.session.watch_once(key, timeout=timeout)

    def watch_prefix(self, key):
        return self.session.watch_prefix(key)

    def get_prefix(self, key_prefix):
        return self.session.get_prefix(key_prefix)

    def delete_prefix(self, key_prefix):
        return self.session.delete_prefix(key_prefix)


if __name__ == '__main__':
    etcd_obj = EtcdObj('192.168.5.16', '2379')
    print(etcd_obj.watch_once('/newben/apps/worker/demo'))