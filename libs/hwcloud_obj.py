# coding: utf-8

import traceback
from utils.decorator import retry
from utils.util import sanitize_for_serialization, str_to_datetime
from libs.log_obj import LogObj
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkecs.v2.region.ecs_region import EcsRegion
from huaweicloudsdkecs.v2 import *


logger = LogObj().get_logger()


class HWCloudObj(object):
    _credentials = None
    _ecs_client = None
    _server_request = None

    def __init__(self, ak, sk, region):
        self.ak = ak
        self.sk = sk
        self.region = region

    @property
    def credentials(self):
        if self._credentials is None:
            self._credentials = BasicCredentials(self.ak, self.sk)
        return self._credentials

    @property
    def ecs_client(self):
        if self._ecs_client is None:
            self._ecs_client = EcsClient.new_builder().with_credentials(self.credentials).\
                with_region(EcsRegion.value_of(self.region)).build()
        return self._ecs_client

    @property
    def all_ecs_info(self):
        response = self.ecs_client.list_servers_details(ListServersDetailsRequest())
        if response.status_code == 200:
            return sanitize_for_serialization(response.servers)
        else:
            logger.error(response)
            raise Exception('Exception occured!')

    def get_ecs_info_by_ip(self, ecs_ip):
        for ecs_info in self.all_ecs_info:
            for addresses_info in ecs_info['addresses'].values():
                for address_info in addresses_info:
                    if ecs_ip == address_info['addr']:
                        return ecs_info
        else:
            raise Exception('ECS {0} is not exist!'.format(ecs_ip))

    def get_vm_name_by_ip(self, ecs_ip):
        return self.get_ecs_info_by_ip(ecs_ip)['name']

    def get_ecs_info_by_name(self, ecs_name):
        for ecs_info in self.all_ecs_info:
            if ecs_info['name'] == ecs_name:
                return ecs_info
        else:
            raise Exception('ECS {0} is not exist!'.format(ecs_name))

    def get_ecs_info_by_id(self, ecs_id):
        request = ShowServerRequest()
        request.server_id = ecs_id
        response = self.ecs_client.show_server(request)
        if response.status_code == 200:
            return sanitize_for_serialization(response.server)
        else:
            logger.error(response)
            raise Exception('Exception occured!')

    def batch_stop_ecs(self, ecs_id_list, type="SOFT"):
        request = BatchStopServersRequest()
        list_server_id_servers_os_stop = [ServerId(id=ecs_id) for ecs_id in ecs_id_list]
        os_stop_batch_stop_servers_option = BatchStopServersOption(servers=list_server_id_servers_os_stop, type=type)
        request.body = BatchStopServersRequestBody(os_stop=os_stop_batch_stop_servers_option)
        response = self.ecs_client.batch_stop_servers(request)
        if response.status_code == 200:
            self.wait_job_done(job_id)
            for ecs_id in ecs_id_list:
                self.is_ecs_shutoff(ecs_id)
        else:
            logger.error(response)
            raise Exception('Exception occured!')

    def batch_start_ecs(self, ecs_id_list):
        request = BatchStartServersRequest()
        list_server_id_servers_os_start = [ServerId(id=ecs_id) for ecs_id in ecs_id_list]
        os_start_batch_start_servers_option = BatchStartServersOption(servers=list_server_id_servers_os_start)
        request.body = BatchStartServersRequestBody(os_start=os_start_batch_start_servers_option)
        response = self.ecs_client.batch_start_servers(request)
        if response.status_code == 200:
            self.wait_job_done(job_id)
            for ecs_id in ecs_id_list:
                self.is_ecs_active(ecs_id)
        else:
            logger.error(response)
            raise Exception('Exception occured!')

    def batch_reboot_ecs(self, ecs_id_list, type="SOFT"):
        request = BatchRebootServersRequest()
        list_server_id_servers_reboot = [ServerId(id=ecs_id) for ecs_id in ecs_id_list]
        reboot_batch_reboot_severs_option = BatchRebootSeversOption(servers=list_server_id_servers_reboot, type=type)
        request.body = BatchRebootServersRequestBody(reboot=reboot_batch_reboot_severs_option)
        response = self.ecs_client.batch_reboot_servers(request)
        if response.status_code == 200:
            self.wait_job_done(job_id)
            for ecs_id in ecs_id_list:
                self.is_ecs_active(ecs_id)
        else:
            logger.error(response)
            raise Exception('Exception occured!')

    def batch_opreate_vms(self, vm_names, operation):
        ecs_id_list = [self.get_ecs_info_by_name(vm_name)['id'] for vm_name in vm_names]
        operate = {
            "poweroff": self.batch_stop_ecs(ecs_id_list, 'HARD'),
            "shutdown": self.batch_stop_ecs(ecs_id_list),
            "poweron": self.batch_start_ecs(ecs_id_list),
            "reboot": self.batch_reboot_ecs(ecs_id_list),
            "reset": self.batch_reboot_ecs(ecs_id_list, 'HARD'),
            "suspend": None
        }
        try:
            return operate[operation]
        except Exception as e:
            logger.error('Exception occurred: {err}, please enter right operate type'
                         '(poweroff,poweron,reset,reboot,shutdown)'.format(err=traceback.format_exc()))
            raise e

    def show_job(self, job_id):
        request = ShowJobRequest()
        request.job_id = job_id
        response = self.ecs_client.show_job(request)
        if response.status_code == 200:
            return sanitize_for_serialization(response)
        else:
            logger.error(response)
            raise Exception('Exception occured!')

    @retry(tries=120, delay=5)
    def wait_job_done(self, job_id):
        job_info = self.show_job(job_id)
        job_status = job_info['status']
        job_entities = job_info['entities']
        if job_status == 'SUCCESS':
            logger.info('Job {0} had done, its status is {1}!'.format(job_id, job_status))
        elif job_status == 'FAIL':
            logger.error('Job {0} had done, its status is {1}, error is {2}!'.format(job_id, job_status, job_entities))
        else:
            raise Exception('Job had not done, it is {0}, please wait'.format(job_status))
        begin_time = str_to_datetime(job_info['begin_time'].split('.')[0], fmt="%Y-%m-%dT%H:%M:%S")
        end_time = str_to_datetime(job_info['end_time'].split('.')[0], fmt="%Y-%m-%dT%H:%M:%S")
        take_time = end_time - begin_time
        logger.info('Job {0} done take time is {1}!'.format(job_id, take_time))

    @retry(tries=120, delay=5)
    def is_ecs_active(self, ecs_id):
        ecs_info = self.get_ecs_info_by_id(ecs_id)
        ecs_status = ecs_info['status']
        ecs_name = ecs_info['name']
        if ecs_status != 'ACTIVE':
            raise Exception('ECS {0} is not active, its status is {1}!'.format(ecs_name, ecs_status))
        logger.info('ECS {0} is {1}!'.format(ecs_name, ecs_status))

    @retry(tries=120, delay=5)
    def is_ecs_shutoff(self, ecs_id):
        ecs_info = self.get_ecs_info_by_id(ecs_id)
        ecs_status = ecs_info['status']
        ecs_name = ecs_info['name']
        if ecs_status != 'SHUTOFF':
            raise Exception('ECS {0} is not shutoff, its status is {1}!'.format(ecs_name, ecs_status))
        logger.info('ECS {0} is {1}!'.format(ecs_name, ecs_status))


if __name__ == "__main__":
    ak = "MKWRFCYCEPAMR35AASLJ"
    sk = "lQxJyKsiSKPLpxJUbAFi3A7H1UHKCL94d7Xd4ZBY"
    region = "cn-southwest-2"
    ecs_id_list = ["f55a1c1a-49b4-4e19-905b-80af9c82bd33"]
    job_id = "ff8080817bcb4bd1017bf6a9e8933554"
    hwcloud_obj = HWCloudObj(ak, sk, region)
    ecs_info = hwcloud_obj.get_ecs_info_by_name('ecs-2ef0-0002')
    import json
    print(json.dumps(ecs_info, indent=4))
