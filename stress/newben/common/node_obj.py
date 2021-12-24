import datetime
import os
import sys
import json
import yaml
import time
from utils.util import str_to_datetime
from libs.ssh_obj import SSHObj
from libs.log_obj import LogObj
from utils.decorator import retry, print_for_call
from settings.global_settings import ETCDCTL
from prettytable import PrettyTable
from settings.newben_settings import BOOTSTRAP_PROCESS, CORESERVER_PROCESS, INSTALL_PATH, \
    AGENT_PROCESS, DOCKER_NAI_PROCESS, PROXY_PROCESS, SEAM_PROCESS, WEB_PROCESS, LOG_PROCESS, BOOTSTRAP_DOCKER, \
    CORESERVER_DOCKER, AGENT_DOCKER, DOCKER_NAI_DOCKER, PROXY_DOCKER, WEB_DOCKER, LOG_DOCKER, \
    ETCD_DOCKER, ETCD_PROCESS, SEAM_DOCKER, RQLITE_PROCESS, RQLITE_DOCKER


logger = LogObj().get_logger()


class NodeObj(SSHObj):
    _bootstrap_config_info = None
    _install_config_data = None
    _install_nodes_ip = []

    def __init__(self, ip, username='root', password='password', port=22, key_file=None):
        super(NodeObj, self).__init__(ip, username, password, port, key_file)

    def login(self):
        cmd = 'nbctl login -u admin -p password'
        rtn_dict = self.run_cmd(cmd)
        if rtn_dict['rc'] != 0 or 'admin login success' not in rtn_dict['stdout']:
            raise Exception('Exception occured, error is {0}!'.format(rtn_dict))
        logger.debug('nbctl login success, token is {0}'.format(self.run_cmd('cat /tmp/nb-security')['stdout'].strip()))

    @retry(tries=5, delay=1)
    def get_controllers_info_by_kind(self, controller_kind):
        controllers_info = []
        cmd = 'nbctl get {0} -a -o json'.format(controller_kind)
        rtn_dict = self.run_cmd(cmd, timeout=120)
        if rtn_dict['rc'] == 0 and rtn_dict['stderr'] == '':
            if 'No Resource Found' not in rtn_dict['stdout']:
                all_info = json.loads(rtn_dict['stdout'])
                if isinstance(all_info, list):
                    controllers_info.extend(all_info)
                else:
                    controllers_info.append(all_info)
        elif 'token is expired' in rtn_dict['stdout'] or 'unauthorized' in rtn_dict['stdout'] or \
                'Token used before issued' in rtn_dict['stdout']:
            logger.error('{0}, will relogin!'.format(rtn_dict['stdout']))
            self.login()
            raise Exception('Token is expired, relogin done!')
        else:
            logger.error(rtn_dict)
            raise Exception('Exception occured, result is {0}!'.format(rtn_dict))

        tb = PrettyTable()
        if controller_kind == 'box':
            tb.field_names = ['Workspace', 'Name', 'Kind', 'Type', 'BoxIP', 'WorkerName', 'Phase', 'RestartCount',
                              'CreationTimestamp', 'DeletionTimestamp', 'BootupTime', 'JobDoneTime']
        elif controller_kind == 'app':
            tb.field_names = ['Workspace', 'Name', 'Kind', 'Replicas', 'Phase', 'CreationTimestamp']
        elif controller_kind == 'workerset':
            tb.field_names = ['Name', 'Kind', 'IP', 'Phase', 'AvailableBox', 'CreationTimestamp']
        elif controller_kind == 'worker':
            tb.field_names = ['Name', 'Kind', 'IP', 'Phase', 'AvailableBox', 'CreationTimestamp']
        elif controller_kind == 'boxset':
            tb.field_names = ['Workspace', 'Name', 'Kind', 'Replicas', 'Phase', 'Owner', 'CreationTimestamp']
        elif controller_kind == 'forward':
            tb.field_names = ['Workspace', 'Name', 'Kind', 'boxPort', 'exposePort', 'CreationTimestamp']
        for controller_info in controllers_info:
            name = controller_info['meta']['name']
            kind = controller_info['meta']['kind']
            creation_time_stamp = controller_info['meta']['creationTimestamp']
            if controller_kind == 'box':
                workspace = controller_info['meta']['workspace']
                phase = controller_info['status']['phase']
                controller_type = controller_info['spec']['type']
                restart_count = controller_info['status']['restartCount']
                if 'boxIP' in controller_info['status']:
                    box_ip = controller_info['status']['boxIP']
                else:
                    box_ip = None
                if 'workerName' in controller_info['status']:
                    worker_name = controller_info['status']['workerName']
                else:
                    worker_name = None

                if 'deletionTimestamp' in controller_info['meta']:
                    deletion_time_stamp = controller_info['meta']['deletionTimestamp']
                else:
                    deletion_time_stamp = None

                bootup_time = None
                job_done_time = None
                if phase == 'running':
                    tmp_started_time = controller_info['status']['containerStatuses'][0]['state']['running']['startedAt'].split('T')
                    started_time = str_to_datetime(' '.join([tmp_started_time[0], tmp_started_time[1].strip('Z').split('+')[0]]),
                                                   fmt="%Y-%m-%d %H:%M:%S")
                    tmp_create_time = creation_time_stamp.split('T')
                    create_time = str_to_datetime(' '.join([tmp_create_time[0], tmp_create_time[1].strip('Z').split('+')[0]]),
                                                  fmt="%Y-%m-%d %H:%M:%S")
                    if controller_info['status']['containerStatuses'][0]['lastTerminationState']:
                        try:
                            tmp_finished_time = controller_info['status']['containerStatuses'][0]['lastTerminationState']['terminated']['finishedAt'].split('T')
                        except AttributeError:
                            raise Exception("Appear error,the box is {}, workspace is {}, please check the box,"
                                            " if exist null data".format(name, workspace))
                        else:
                            finished_time = str_to_datetime(' '.join([tmp_finished_time[0], tmp_finished_time[1].strip('Z').split('+')[0]]),
                                                        fmt="%Y-%m-%d %H:%M:%S")
                            controller_info['status']['containerStatuses'][0]['lastTerminationState']['terminated']['finished_time'] = finished_time
                            bootup_time = started_time - finished_time
                    else:
                        bootup_time = started_time - create_time
                elif phase == 'succeeded':
                    tmp_started_time = controller_info['status']['containerStatuses'][0]['state']['terminated']['startedAt'].split(
                        'T')
                    started_time = str_to_datetime(' '.join([tmp_started_time[0], tmp_started_time[1].strip('Z').split('+')[0]]),
                                                   fmt="%Y-%m-%d %H:%M:%S")
                    tmp_finished_time = controller_info['status']['containerStatuses'][0]['state']['terminated'][
                        'finishedAt'].split(
                        'T')
                    finished_time = str_to_datetime(' '.join([tmp_finished_time[0], tmp_finished_time[1].strip('Z').split('+')[0]]),
                                                    fmt="%Y-%m-%d %H:%M:%S")
                    job_done_time = finished_time - started_time
                controller_info['bootup_time'] = bootup_time
                controller_info['job_done_time'] = job_done_time
                tb.add_row([workspace, name, kind, controller_type, box_ip, worker_name, phase, restart_count,
                            creation_time_stamp, deletion_time_stamp, bootup_time, job_done_time])
            elif controller_kind == 'app':
                workspace = controller_info['meta']['workspace']
                replica = controller_info['spec']['template']['spec']['replicas']
                phase = controller_info['status']['phase']
                tb.add_row([workspace, name, kind, replica, phase, creation_time_stamp])
            elif controller_kind == 'workerset':
                if 'ip' in controller_info['status']:
                    ip = controller_info['status']['ip']
                else:
                    ip = None
                phase = controller_info['status']['phase']
                availableBox = controller_info['spec']['workers'][0]['availableBox']
                tb.add_row([name, kind, ip, phase, availableBox, creation_time_stamp])
            elif controller_kind == 'worker':
                if 'ip' in controller_info['status']:
                    ip = controller_info['status']['ip']
                else:
                    ip = None
                phase = controller_info['status']['phase']
                availableBox = controller_info['spec']['availableBox']
                tb.add_row([name, kind, ip, phase, availableBox, creation_time_stamp])
            elif controller_kind == 'boxset':
                workspace = controller_info['meta']['workspace']
                replica = controller_info['spec']['replicas']
                phase = controller_info['status']['phase']
                owner = controller_info['meta']['ownerReference']['name']
                tb.add_row([workspace, name, kind, replica, phase, owner, creation_time_stamp])
            elif controller_kind == 'forward':
                workspace = controller_info['meta']['workspace']
                box_port = controller_info['spec']['rules'][0]['boxPort']
                if 'exposePort' in controller_info['spec']['rules'][0]:
                    expose_port = controller_info['spec']['rules'][0]['exposePort']
                else:
                    expose_port = None
                tb.add_row([workspace, name, kind, box_port, expose_port, creation_time_stamp])
        if controller_kind in ['box', 'app', 'workerset', 'worker', 'boxset', 'forward']:
            logger.debug('\n{0}'.format(tb))
        return controllers_info

    @retry(tries=5, delay=1)
    def nbctl_operate_by_yaml(self, opereation, yaml_file_path):
        controller_yaml_data = self.load_yaml_data(yaml_file_path)
        controller_name = controller_yaml_data['meta']['name']
        controller_kind = controller_yaml_data['meta']['kind']

        cmd = 'nbctl {0} -f {1}'.format(opereation, yaml_file_path)
        rtn_dict = self.run_cmd(cmd)
        if rtn_dict['rc'] == 0 and rtn_dict['stderr'] == '':
            logger.debug(rtn_dict['stdout'])
            logger.info('{0} {1} {2} success!'.format(opereation, controller_kind, controller_name))
            return controller_name
        elif 'token is expired' in rtn_dict['stdout'] or 'unauthorized' in rtn_dict['stdout'] or \
                'Token used before issued' in rtn_dict['stdout']:
            logger.error('{0}, will relogin!'.format(rtn_dict['stdout']))
            self.login()
            raise Exception('Token is expired, relogin done!')
        elif 'etcdserver: request timed out' in rtn_dict:
            logger.warning('Skip, because {0}'.format(rtn_dict['stdout']))
        else:
            logger.error('STDOUT: {0}'.format(rtn_dict['stdout']))
            logger.error('STDERR: {0}'.format(rtn_dict['stderr']))
            logger.error('Return Code: {0}'.format(rtn_dict['rc']))
            raise Exception('{0} {1} {2} fail!'.format(opereation, controller_kind, controller_name))

    @retry(tries=5, delay=1)
    def delete_controller_by_kind(self, controller_kind, controller_name, workspace):
        cmd = 'nbctl delete {0} {1} -w {2}'.format(controller_kind, controller_name, workspace)
        rtn_dict = self.run_cmd(cmd)
        if rtn_dict['rc'] == 0 and rtn_dict['stderr'] == '':
            logger.info('Delete {0} {1} success!'.format(controller_kind, controller_name))
        elif 'token is expired' in rtn_dict['stdout'] or 'unauthorized' in rtn_dict['stdout']:
            logger.error('{0}, will relogin!'.format(rtn_dict['stdout']))
            self.login()
            raise Exception('Token is expired, relogin done!')
        elif 'etcdserver: request timed out' in rtn_dict:
            logger.warning('Skip, because {0}'.format(rtn_dict['stdout']))
        else:
            logger.error('STDOUT: {0}'.format(rtn_dict['stdout']))
            logger.error('STDERR: {0}'.format(rtn_dict['stderr']))
            logger.error('Return Code: {0}'.format(rtn_dict['rc']))
            raise Exception('Exception occured, Delete {0} {1} fail!'.format(controller_kind, controller_name))

    @property
    def workspaces_info(self):
        return self.get_controllers_info_by_kind('workspace')

    @property
    def workersets_info(self):
        return self.get_controllers_info_by_kind('workerset')

    @property
    def workers_info(self):
        return self.get_controllers_info_by_kind('worker')

    @property
    def apps_info(self):
        return self.get_controllers_info_by_kind('app')

    @property
    def boxsets_info(self):
        return self.get_controllers_info_by_kind('boxset')

    @property
    def boxs_info(self):
        return self.get_controllers_info_by_kind('box')

    @property
    def missions_info(self):
        return self.get_controllers_info_by_kind('mission')

    @property
    def forwards_info(self):
        return self.get_controllers_info_by_kind('forward')

    @property
    def storagepool_info(self):
        return self.get_controllers_info_by_kind('storagepool')

    @property
    def jobs_info(self):
        jobs_info = []
        for box_info in self.boxs_info:
            if box_info['meta']['ownerReference']['kind'] == 'mission':
                jobs_info.append(box_info)
        return jobs_info

    @property
    def etcd_info(self):
        etcd_info = dict()
        tmp_etcd_info = self.bootstrap_config_info['store']['servers'].strip().split('//')[-1].split(':')
        etcd_info['ip'] = tmp_etcd_info[0]
        etcd_info['port'] = tmp_etcd_info[1]
        return etcd_info

    @property
    def etcds_info(self):
        etcds_info = []
        cmd = '{0} --endpoints=http://{1}:{2} member list'.format(ETCDCTL, self.ip, 2379)
        result = self.docker_exec(ETCD_DOCKER, cmd)
        for tmp_info in result.split('\n'):
            etcd_info = dict()
            tmp_info_list = tmp_info.split(',')
            etcd_addr = tmp_info_list[4].split('://')[1]
            etcd_addr_list = etcd_addr.split(':')
            etcd_info['ip'] = etcd_addr_list[0]
            etcd_info['port'] = etcd_addr_list[1]
            etcd_info['status'] = tmp_info_list[1].strip()
            etcd_info['node'] = tmp_info_list[2].strip()
            etcds_info.append(etcd_info)
        return etcds_info

    @property
    def workspaces_name(self):
        return self.get_controllers_name('workspace')

    @property
    def workers_name(self):
        return self.get_controllers_name('worker')

    @property
    def workersets_name(self):
        return self.get_controllers_name('workerset')

    @property
    def apps_name(self):
        return self.get_controllers_name('app')

    @property
    def forwards_name(self):
        return self.get_controllers_name('forward')

    @property
    def boxs_name(self):
        return self.get_controllers_name('box')

    def get_controllers_name(self, controller_kind):
        controllers_name = []
        for controller_info in self.get_controllers_info_by_kind(controller_kind):
            controllers_name.append(controller_info['meta']['name'])
        return controllers_name

    @property
    def workersets_ip(self):
        workersets_ip = []
        for workerset_info in self.workersets_info:
            workersets_ip.append(workerset_info['status']['ip'])
        return workersets_ip

    @property
    def workers_ip(self):
        workers_ip = []
        for worker_info in self.workers_info:
            workers_ip.append(worker_info['status']['ip'])
        return workers_ip

    def get_workerset_info_by_ip(self, node_ip):
        for workerset_info in self.workersets_info:
            if workerset_info['status']['ip'] == node_ip:
                return workerset_info
        else:
            raise Exception('Workerset {0} is not exist!'.format(node_ip))

    def get_workerset_name_by_worker(self, worker_name):
        worker_info = self.get_worker_info_by_name(worker_name)
        return worker_info['meta']['ownerReference']['name']

    def get_node_ip_by_worker_name(self, worker_name):
        for worker_info in self.workers_info:
            if worker_info['meta']['name'] == worker_name:
                return worker_info['status']['ip']
        else:
            raise Exception('Worker {0} is not exist!'.format(worker_name))

    def get_box_info_by_name(self, box_name):
        for box_info in self.boxs_info:
            if box_info['meta']['name'] == box_name:
                return box_info
        else:
            raise Exception('Box {0} is not exist!'.format(box_name))

    def get_boxs_info_by_workerset(self, workset_name):
        boxs_info = []
        for box_info in self.boxs_info:
            if box_info['status']['workerName'] == workset_name:
                boxs_info.append(box_info)
        return boxs_info

    def get_boxs_info_by_app(self, app_name):
        boxs_info = []
        for box_info in self.boxs_info:
            if box_info['meta']['annotations']['application-name'] == app_name:
                boxs_info.append(box_info)
        return boxs_info

    def get_worker_info_by_name(self, worker_name):
        for worker_info in self.workers_info:
            if worker_info['meta']['name'] == worker_name:
                return worker_info
        else:
            raise Exception('Worker {0} is not exist!'.format(worker_name))

    def get_apps_info_by_workspace(self, workspace):
        apps_info = []
        for app_info in self.apps_info:
            if app_info['meta']['workspace'] == workspace:
                apps_info.append(app_info)
        return apps_info

    def get_boxs_info_by_workspace(self, workspace):
        boxs_info = []
        for box_info in self.boxs_info:
            if box_info['meta']['workspace'] == workspace:
                boxs_info.append(box_info)
        return boxs_info

    @retry(tries=120, delay=5)
    def is_controllers_running_by_kind(self, controller_kind, workspace=None, controllers_name=None):
        controllers_exception = []
        controllers_info = self.get_controllers_info_by_kind(controller_kind)
        logger.debug('{0} number is {1}!'.format(controller_kind, len(controllers_info)))
        for controller_info in controllers_info:
            if workspace and 'workspace' in controller_info['meta'] and \
                    controller_info['meta']['workspace'] != workspace:
                continue
            controller_name = controller_info['meta']['name']
            if controllers_name and controller_name not in controllers_name:
                continue

            controller_phase = controller_info['status']['phase']
            base_check_point = controller_phase == 'running' and 'deletionTimestamp' not in controller_info['meta']
            if controller_kind == 'box':
                if controller_info['meta']['ownerReference']['kind'] == 'boxset':
                    check_point = base_check_point \
                                  and 'running' in controller_info['status']['containerStatuses'][0]['state'] \
                                  and 'boxIP' in controller_info['status']
                else:
                    continue
            elif controller_kind in ['worker', 'workerset']:
                check_point = base_check_point and 'ip' in controller_info['status']
            else:
                check_point = base_check_point

            if not check_point:
                controllers_exception.append(controller_name)
        if controllers_exception:
            raise Exception('{0} {1} exists exception!'.format(controller_kind, controllers_exception))

    @print_for_call
    def is_workersets_running(self, workersets_name=None):
        self.is_controllers_running_by_kind('workerset', controllers_name=workersets_name)

    @print_for_call
    def is_workers_running(self, workers_name=None):
        self.is_controllers_running_by_kind('worker', controllers_name=workers_name)

    @print_for_call
    def is_boxsets_running(self, workspace=None):
        self.is_controllers_running_by_kind('boxset', workspace)

    @print_for_call
    def is_apps_running(self, workspace=None):
        self.is_controllers_running_by_kind('app', workspace)

    @print_for_call
    def is_appmatrixes_running(self, workspace=None):
        self.is_controllers_running_by_kind('appmatrix', workspace)

    @print_for_call
    def is_boxs_running(self, workspace=None):
        self.is_controllers_running_by_kind('box', workspace)

    @retry(tries=60, delay=5)
    def is_controllers_disconnect_by_kind(self, controller_kind, controllers_name=None):
        if controller_kind not in ['worker', 'workerset']:
            raise Exception('Function {0} do not support {1} kind!'.format(sys._getframe().f_code.co_name,
                                                                           controller_kind))
        controllers_exception = []
        controllers_info = self.get_controllers_info_by_kind(controller_kind)
        logger.debug('{0} number is {1}!'.format(controller_kind, len(controllers_info)))
        for controller_info in controllers_info:
            controller_name = controller_info['meta']['name']
            if controllers_name and controller_name not in controllers_name:
                continue

            controller_phase = controller_info['status']['phase']
            check_point = controller_phase == 'disconnect' and 'deletionTimestamp' not in controller_info['meta'] and \
                          'ip' in controller_info['status']

            if not check_point:
                controllers_exception.append(controller_name)
        if controllers_exception:
            raise Exception('{0} {1} exists exception!'.format(controller_kind, controllers_exception))

    @print_for_call
    def is_workersets_disconnect(self, workersets_name=None):
        self.is_controllers_disconnect_by_kind('workerset', controllers_name=workersets_name)

    @print_for_call
    def is_workers_disconnect(self, workers_name=None):
        self.is_controllers_disconnect_by_kind('worker', controllers_name=workers_name)

    @print_for_call
    def is_box_running_by_name(self, box_name):
        self.is_controllers_running_by_kind('box', controllers_name=[box_name])

    @retry(tries=36, delay=5)
    def is_controllers_not_exist_by_name(self, controller_kind, controller_name_list):
        controllers_name = self.get_controllers_name(controller_kind)
        exist_boxs_name = list(set(controller_name_list).intersection(controllers_name))
        if exist_boxs_name:
            raise Exception('Still exist {0}: {1}!'.format(controller_kind, exist_boxs_name))
        else:
            logger.info('{0} {1} do not exist!'.format(controller_kind, controller_name_list))

    @print_for_call
    def is_boxs_not_exist_by_name(self, box_name_list):
        self.is_controllers_not_exist_by_name('box', box_name_list)

    @print_for_call
    def is_apps_not_exist_by_name(self, app_name_list):
        self.is_controllers_not_exist_by_name('app', app_name_list)

    @print_for_call
    def is_appmatrixes_not_exist_by_name(self, appmatrix_name_list):
        self.is_controllers_not_exist_by_name('appmatrix', appmatrix_name_list)

    @print_for_call
    def is_forwards_not_exist_by_name(self, forward_name_list):
        self.is_controllers_not_exist_by_name('forward', forward_name_list)

    @print_for_call
    def is_apparafiles_not_exist_by_name(self, apparafile_name_list):
        self.is_controllers_not_exist_by_name('apparafile', apparafile_name_list)

    def is_boxs_not_restart(self, before_boxs_info):
        pass

    @retry(tries=120, delay=5)
    @print_for_call
    def is_app_scale_done(self, app_name, replica):
        boxs_info = self.get_boxs_info_by_app(app_name)
        if len(boxs_info) != replica:
            raise Exception('App {0} scale to {1} had not done!'.format(app_name, replica))
        else:
            logger.info('App {0} scale to {1} had done!'.format(app_name, replica))
        boxs_not_running = []
        for box_info in boxs_info:
            box_name = box_info['meta']['name']
            box_phase = box_info['status']['phase']
            if box_phase == 'running':
                logger.debug('Box {0} is {1}!'.format(box_name, box_phase))
            else:
                logger.warning('Box {0} is not running, its status is {1}!'.format(box_name,
                                                                                   box_phase))
                boxs_not_running.append(box_name)

        if boxs_not_running:
            raise Exception('Boxs {0} are not running!'.format(boxs_not_running))

    @print_for_call
    def is_boxs_bootup_time_quick(self, workspace=None):
        very_slowly_boxs = []
        slowly_boxs = []
        for box_info in self.boxs_info:
            if workspace and box_info['meta']['workspace'] != workspace:
                continue
            box_name = box_info['meta']['name']
            box_bootup_time = box_info['bootup_time']
            if box_bootup_time.seconds > 120:
                logger.error('Box {0} boot up is very slowly, boot up time is {1}!'.format(box_name, box_bootup_time))
                very_slowly_boxs.append(box_name)
            elif box_bootup_time.seconds > 60:
                logger.warning('Box {0} boot up is slowly, boot up time is {1}!'.format(box_name, box_bootup_time))
                slowly_boxs.append(box_name)
            else:
                logger.info('Box {0} boot up is quickly, boot up time is {1}!'.format(box_name, box_bootup_time))

        if slowly_boxs:
            logger.warning('{0} boxs {1} boot up are slowly, their boot up time more than 1 minutes!'.format(
                len(slowly_boxs), slowly_boxs))

        if very_slowly_boxs:
            raise Exception('{0} boxs {1} boot up are very slowly, their boot up time more than 2 minutes!'.format(
                len(very_slowly_boxs), very_slowly_boxs))

    @retry(tries=360, delay=10)
    @print_for_call
    def is_jobs_succeeded(self, workspace=None):
        jobs_failed = []
        jobs_pending = []
        jobs_running = []
        jobs_other = []
        for job_info in self.jobs_info:
            if workspace and job_info['meta']['workspace'] != workspace:
                continue
            job_name = job_info['meta']['name']
            job_phase = job_info['status']['phase']
            if job_phase == 'succeeded':
                logger.info('Job {0} had succeeded, its status is {1}!'.format(job_name, job_phase))
            elif job_phase == 'failed':
                logger.error('Job {0} had failed, its status is {1}!'.format(job_name, job_phase))
                jobs_failed.append(job_name)
            elif job_phase == 'running':
                logger.warning('Job {0} is running, its status is {1}!'.format(job_name, job_phase))
                jobs_running.append(job_name)
            elif job_phase == 'pending':
                logger.warning('Job {0} is pending, its status is {1}!'.format(job_name, job_phase))
                jobs_pending.append(job_name)
            else:
                logger.error('Job {0} unknown status, its status is {1}!'.format(job_name, job_phase))
                jobs_other.append(job_name)

        if jobs_failed or jobs_pending or jobs_running or jobs_other:
            raise Exception('All jobs had not succeeded, failed: {0}, pending: {1}, running: {2}, '
                            'other: {3}!'.format(jobs_failed, jobs_pending, jobs_running, jobs_other))
        else:
            logger.info('All jobs had succeeded!')

    @retry(tries=60, delay=5)
    def is_etcd_ok(self):
        for etcd_info in self.etcds_info:
            if etcd_info['status'] != 'started':
                raise Exception('etcd info: {0}'.format(etcd_info))
            else:
                logger.info('Etcd {0} status is {1}!'.format(etcd_info['ip'], etcd_info['status']))

    @retry(tries=36, delay=5)
    @print_for_call
    def is_forwards_ok(self, workspace=None, forwards_name=None):
        not_ok_forwards = []
        for forward_info in self.forwards_info:
            forward_name = forward_info['meta']['name']
            if forwards_name and forward_name not in forwards_name:
                continue
            if workspace and forward_info['meta']['workspace'] != workspace:
                continue
            if 'exposePort' not in forward_info['spec']['rules'][0]:
                logger.debug(forward_info)
                logger.warning('Forward {0} expose had not done yet!'.format(forward_name))
                not_ok_forwards.append(forward_name)
            else:
                logger.info('Forward {0} expose had done!'.format(forward_name))
        if not_ok_forwards:
            raise Exception('Forwards {0} were not ok!'.format(not_ok_forwards))
        logger.info('All forward were ok!')

    @retry(tries=60, delay=5)
    @print_for_call
    def is_add_nodes_succeeded(self, nodes_ip):
        workersets_ip = self.workersets_ip
        workers_ip = self.workers_ip
        not_add_nodes_ip = []
        for node_ip in nodes_ip:
            if node_ip not in workersets_ip or node_ip not in workers_ip:
                not_add_nodes_ip.append(node_ip)
        if not_add_nodes_ip:
            raise Exception('Add nodes failed, not add nodes ip are {0}!'.format(not_add_nodes_ip))
        else:
            logger.info('Add nodes {0} succeed!'.format(nodes_ip))

    @retry(tries=60, delay=5)
    @print_for_call
    def is_delete_nodes_succeeded(self, nodes_ip):
        workersets_ip = self.workersets_ip
        workers_ip = self.workers_ip
        not_delete_nodes_ip = []
        for node_ip in nodes_ip:
            if node_ip in workersets_ip or node_ip in workers_ip:
                not_delete_nodes_ip.append(node_ip)
        if not_delete_nodes_ip:
            raise Exception('Delete nodes failed, not delete nodes ip are {0}!'.format(not_delete_nodes_ip))
        else:
            logger.info('Delete nodes {0} done!'.format(nodes_ip))

    @retry(tries=120, delay=5)
    @print_for_call
    def is_storagepool_available(self, provisioners):
        not_available_storagepool = []
        for sp in self.storagepool_info:
            if sp['spec']['provisioner'] in provisioners:
                if sp['status']['phase'] == 'unavailable':
                    not_available_storagepool.append(sp['meta']['name'])
        if not_available_storagepool:
            raise Exception('Unavailable storagepool are {0}!'.format(not_available_storagepool))
        else:
            logger.info('All {} storagepool are available!'.format(provisioners))

    @property
    def nodes_ip(self):
        nodes_ip = []
        for workerset_info in self.workersets_info:
            nodes_ip.append(workerset_info['status']['ip'])

        if self.etcd_info['ip'] not in nodes_ip:
            nodes_ip.append(self.etcd_info['ip'])
        return nodes_ip

    def delete_mission(self, mission_name, workspace):
        self.delete_controller_by_kind('mission', mission_name, workspace)

    def delete_app(self, app_name, workspace):
        self.delete_controller_by_kind('app', app_name, workspace)

    def delete_appmatrix(self, appmarix_name, workspace):
        self.delete_controller_by_kind('appmatrix', appmarix_name, workspace)

    @retry(tries=5, delay=2)
    def delete_box(self, box_name, workspace):
        self.delete_controller_by_kind('box', box_name, workspace)

    def delete_forward(self, forward_name, workspace):
        self.delete_controller_by_kind('forward', forward_name, workspace)

    def delete_apparafile(self, apparafile_name, workspace):
        self.delete_controller_by_kind('apparafile', apparafile_name, workspace)

    def get_forwards_info_by_workspace(self, workspace):
        forwards_info = []
        for forward_info in self.forwards_info:
            if forward_info['meta']['workspace'] == workspace:
                forwards_info.append(forward_info)
        return forwards_info

    def get_forward_info_by_name(self, forward_name):
        for forward_info in self.forwards_info:
            if forward_info['meta']['name'] == forward_name:
                return forward_info
        else:
            raise Exception('Forward {0} is not exist!'.format(forward_name))

    def maintain_workerset(self, workerset_name):
        cmd = 'nbctl maintain workerset {0}'.format(workerset_name)
        rtn_dict = self.run_cmd(cmd)
        if rtn_dict['rc'] == 0 and rtn_dict['stderr'] == '':
            logger.debug(rtn_dict['stdout'])
            logger.info('Workerset {0} enter maintain mode done!'.format(workerset_name))
        else:
            logger.error(rtn_dict)
            raise Exception('Workerset {0} enter maintain mode fail!'.format(workerset_name))

    def exit_maintain_workerset(self, workerset_name):
        cmd = 'nbctl maintain workerset {0} --unset'.format(workerset_name)
        rtn_dict = self.run_cmd(cmd)
        if rtn_dict['rc'] == 0 and rtn_dict['stderr'] == '':
            logger.debug(rtn_dict['stdout'])
            logger.info('Workerset {0} exit maintain mode done!'.format(workerset_name))
        else:
            logger.error(rtn_dict)
            raise Exception('Workerset {0} exit maintain mode fail!'.format(workerset_name))

    @retry(tries=60, delay=5)
    @print_for_call
    def is_enter_maintain_by_ip(self, node_ip):
        workerset_info = self.get_workerset_info_by_ip(node_ip)
        workerset_phase = workerset_info['status']['phase']
        if workerset_phase == 'maintained':
            logger.debug('Workerset {0} had entered maintain mode!'.format(node_ip))
        else:
            raise Exception('Workerset {0} had not entered maintain mode, its status is {1}!'.format(node_ip,
                                                                                                     workerset_phase))

    @retry(tries=60, delay=5)
    @print_for_call
    def is_exit_maintain_by_ip(self, node_ip):
        workerset_info = self.get_workerset_info_by_ip(node_ip)
        workerset_phase = workerset_info['status']['phase']
        if workerset_phase == 'running':
            logger.debug('Workerset {0} had exited maintain mode!'.format(node_ip))
        else:
            raise Exception('Workerset {0} had not exited maintain mode, its status is {1}!'.format(node_ip,
                                                                                                     workerset_phase))

    @property
    def bootstrap_config_info(self):
        if self._bootstrap_config_info is None:
            bootstrap_command = self.get_docker_info_by_name(BOOTSTRAP_DOCKER)['command']
            bootstra_config_file = bootstrap_command.split('=')[-1].strip('"')
            self._bootstrap_config_info = self.load_yaml_data(bootstra_config_file)
        return self._bootstrap_config_info

    @property
    def coreserver_node_ip(self):
        if not isinstance(self.bootstrap_config_info['coreserver'], dict):
            return self.bootstrap_config_info['coreserver'].split('//')[-1].split(':')[0]
        else:
            return self.ip

    def get_jobs_info_by_workspace(self, workspace):
        jobs_info = []
        for job_info in self.jobs_info:
            if job_info['meta']['workspace'] == workspace:
                jobs_info.append(job_info)
        return jobs_info

    def get_job_info_by_name(self, job_name):
        for job_info in self.jobs_info:
            if job_info['meta']['name'] == job_name:
                return job_info
        else:
            raise Exception('Job {0} is not exist!'.format(job_name))

    def get_missions_info_by_workspace(self, workspace):
        missions_info = []
        for mission_info in self.missions_info:
            if mission_info['meta']['workspace'] == workspace:
                missions_info.append(mission_info)
        return missions_info

    def get_jobs_info_by_mission(self, mission_name):
        jobs_info = []
        for job_info in self.jobs_info:
            if job_info['meta']['ownerReference']['name'] == mission_name:
                jobs_info.append(job_info)
        return jobs_info

    @retry(tries=120, delay=5)
    @print_for_call
    def is_mission_not_exist(self, mission_name):
        for mission_info in self.missions_info:
            mission_phase = mission_info['status']['phase']
            if mission_info['meta']['name'] == mission_name:
                raise Exception('Mission {0} is still exist, its status is {1}!'.format(mission_name, mission_phase))
        logger.info('Mission {0} is not exist!'.format(mission_name))

    @property
    def install_config_data(self):
        if self._install_config_data is None:
            install_config_file = os.path.join(INSTALL_PATH, 'config.yaml')
            self._install_config_data = self.load_yaml_data(install_config_file)
        return self._install_config_data

    @property
    def install_nodes_ip(self):
        if not self._install_nodes_ip:
            for node_info in self.install_config_data['nodes']:
                self._install_nodes_ip.append(node_info['address'])
        return self._install_nodes_ip

    def update_node(self, option, install_file, nodes_ip):
        cmd = 'cd {0};./nbd -c {1} {2} {3}'.format(INSTALL_PATH, install_file, option, ' '.join(nodes_ip))
        rtn_dict = self.run_cmd(cmd)
        if rtn_dict['rc'] == 0:
            logger.debug(rtn_dict['stdout'])
            logger.debug(rtn_dict['stderr'])
            logger.info('{0} nodes {1} done!'.format(option, nodes_ip))
        else:
            logger.error(rtn_dict)
            raise Exception('{0} nodes {1} failed!'.format(option, nodes_ip))

    def get_controller_yaml(self, controller_kind, controller_name, workspace=None):
        if workspace:
            cmd = 'nbctl get {0} {1} -w {2} -o yaml'.format(controller_kind, controller_name, workspace)
        else:
            cmd = 'nbctl get {0} {1} -o yaml'.format(controller_kind, controller_name)
        rtn_dict = self.run_cmd(cmd)
        if rtn_dict['rc'] == 0 and rtn_dict['stderr'] == '':
            controller_yaml_data = yaml.load(rtn_dict['stdout'], Loader=yaml.FullLoader)
            return controller_yaml_data
        else:
            logger.error(rtn_dict)
            raise Exception('Get app {0} yaml fail!'.format(controller_name))

    def update_replica(self, app_name, workspace, replica):
        app_yaml_data = self.get_controller_yaml('app', app_name, workspace)
        app_yaml_data['spec']['template']['spec']['replicas'] = replica
        return app_yaml_data

    def nbctl_create(self, yaml_file_path):
        self.nbctl_operate_by_yaml('create', yaml_file_path)

    def nbctl_update(self, yaml_file_path):
        self.nbctl_operate_by_yaml('update', yaml_file_path)

    @property
    def etcdctl_docker_path(self):
        return self.docker_exec(ETCD_DOCKER, 'which etcdctl')

    def ping_app(self, docker_name, app_info):
        app_name = app_info['meta']['name']
        workspace = app_info['meta']['workspace']
        result = self.docker_exec(docker_name, 'ping -c 1 {0}.{1}'.format(app_name, workspace))
        ping_info = dict()
        ping_info['time'] = result.split('\n')[-1].split('=')[-1].split('/')[1]
        ping_info['unit'] = result.split('\n')[-1].split('=')[-1].split('/')[-1].split()[-1]
        return ping_info

    def get_ping_apps_info(self, docker_name, apps_info):
        all_ping_info = []
        tb = PrettyTable()
        tb.field_names = ['Workspace', 'AppName', 'DockerName', 'PingTime']
        for app_info in apps_info:
            ping_info = self.ping_app(docker_name, app_info)
            app_name = app_info['meta']['name']
            workspace = app_info['meta']['workspace']
            ping_time = '{0}{1}'.format(ping_info['time'], ping_info['unit'])
            tb.add_row([workspace, app_name, docker_name, ping_time])
            all_ping_info.append(ping_info)
        logger.debug('\n{0}'.format(tb))
        return all_ping_info

    def get_docker_version(self, docker_name):
        docker_info = self.get_docker_info_by_name(docker_name)
        command = '{0} -v'.format(docker_info['command'].strip('"').split()[0])
        result = self.docker_exec(docker_name, command)
        return json.loads(result.split('version')[-1].strip())

    def get_binary_version(self, binary_path):
        cmd = '{0} -v'.format(binary_path)
        rtn_dict = self.run_cmd(cmd)
        if rtn_dict['rc'] == 0 and rtn_dict['stderr'] == '':
            return json.loads(rtn_dict['stdout'].strip().split('version')[-1].strip())
        else:
            logger.error(rtn_dict)
            raise Exception('{0}: get {1} version failed!'.format(self.ip, binary_path))

    @print_for_call
    def is_coreserver_up(self):
        self.is_process_up_by_name(CORESERVER_PROCESS)
        self.is_docker_ok_by_name(CORESERVER_DOCKER)

    @print_for_call
    def is_bootstrap_up(self):
        self.is_process_up_by_name(BOOTSTRAP_PROCESS)
        self.is_docker_ok_by_name(BOOTSTRAP_DOCKER)

    @print_for_call
    def is_seam_up(self, single=False):
        if not single:
            self.is_process_up_by_name(SEAM_PROCESS)
            self.is_docker_ok_by_name(SEAM_DOCKER)

    @print_for_call
    def is_agent_up(self):
        self.is_process_up_by_name(AGENT_PROCESS)
        self.is_docker_ok_by_name(AGENT_DOCKER)

    @print_for_call
    def is_docker_nai_up(self):
        self.is_process_up_by_name(DOCKER_NAI_PROCESS)
        self.is_docker_ok_by_name(DOCKER_NAI_DOCKER)

    @print_for_call
    def is_proxy_up(self, single=False):
        if not single:
            self.is_process_up_by_name(PROXY_PROCESS)
            self.is_docker_ok_by_name(PROXY_DOCKER)

    @print_for_call
    def is_web_up(self):
        self.is_process_up_by_name(WEB_PROCESS)
        self.is_docker_ok_by_name(WEB_DOCKER)

    @print_for_call
    def is_rqlite_up(self, single=False):
        if not single:
            self.is_process_up_by_name(RQLITE_PROCESS)
            self.is_docker_ok_by_name(RQLITE_DOCKER)

    @print_for_call
    def is_log_up(self, single=False):
        if not single:
            self.is_process_up_by_name(LOG_PROCESS)
            self.is_docker_ok_by_name(LOG_DOCKER)

    @print_for_call
    def is_etcd_up(self):
        self.is_process_up_by_name(ETCD_PROCESS)
        self.is_docker_ok_by_name(ETCD_DOCKER)
        self.is_etcd_ok()

    def get_docker_fault_check_time(self, box_name):
        cmd = 'docker logs nb-bootstrap 2>&1 | grep "have been unhealthy,time" |grep {0}'.format(box_name)
        rtn_dict = self.run_cmd(cmd)
        if rtn_dict['rc'] == 0:
            time_str = rtn_dict['stdout'].split('\x1b')[0].split()[-1]
            datetime_str = '{0} {1}'.format(datetime.datetime.now().strftime("%Y-%m-%d"), time_str)
            return str_to_datetime(datetime_str, fmt="%Y-%m-%d %H:%M:%S.%f")
        else:
            logger.error(rtn_dict)
            raise Exception('Get docker fault check time failed!')

    def get_docker_boot_start_time(self, docker_id):
        cmd = 'docker logs nb-bootstrap 2>&1 | grep "start time" | grep "start container" |grep {0}'.format(docker_id)
        rtn_dict = self.run_cmd(cmd)
        if rtn_dict['rc'] == 0:
            time_str = rtn_dict['stdout'].split('\x1b')[0].split()[-1]
            datetime_str = '{0} {1}'.format(datetime.datetime.now().strftime("%Y-%m-%d"), time_str)
            return str_to_datetime(datetime_str, fmt="%Y-%m-%d %H:%M:%S.%f")
        else:
            logger.error(rtn_dict)
            raise Exception('Get docker boot start time failed!')

    def get_docker_boot_end_time(self, docker_id):
        cmd = 'docker logs nb-bootstrap 2>&1 | grep "end time" | grep "start container" |grep {0}'.format(docker_id)
        rtn_dict = self.run_cmd(cmd)
        if rtn_dict['rc'] == 0:
            time_str = rtn_dict['stdout'].split('\x1b')[0].split()[-1]
            datetime_str = '{0} {1}'.format(datetime.datetime.now().strftime("%Y-%m-%d"), time_str)
            return str_to_datetime(datetime_str, fmt="%Y-%m-%d %H:%M:%S.%f")
        else:
            logger.error(rtn_dict)
            raise Exception('Get docker boot end time failed!')

    def get_box_create_done_time(self, box_name):
        cmd = 'docker logs nb-bootstrap 2>&1 | grep "success create box" | grep {0}'.format(box_name)
        rtn_dict = self.run_cmd(cmd)
        if rtn_dict['rc'] == 0:
            time_str = rtn_dict['stdout'].split('\x1b')[0].split()[-1]
            datetime_str = '{0} {1}'.format(datetime.datetime.now().strftime("%Y-%m-%d"), time_str)
            return str_to_datetime(datetime_str, fmt="%Y-%m-%d %H:%M:%S.%f")
        else:
            logger.error(rtn_dict)
            raise Exception('Get box create done time failed!')

    @retry(tries=120, delay=5)
    @print_for_call
    def is_box_stopped(self, box_name):
        for box_info in self.boxs_info:
            if box_name in box_info['meta']['name']:
                if box_info['status']['isStop'] and box_info['status']['phase'] == "failed":
                    logger.info("Box {} has stopped".format(box_info['meta']['name']))

                    ft1 = "%Y-%m-%dT%H:%M:%S+08:00"
                    ft2 = "%Y-%m-%d %H:%M:%S"
                    tmp_time_1 = time.strptime(box_info['status']['containerStatuses'][0]['state']['terminated']
                                               ['finishedAt'], ft1)
                    tmp_time_2 = time.strftime(ft2, tmp_time_1)
                    tmp_time_3 = time.strptime(tmp_time_2, ft2)
                    finished_timestamp = int(time.mktime(tmp_time_3))
                    return finished_timestamp - 28800
                else:
                    raise Exception("Box {} has not stopped, status is [isStop:{}, phase:{}]".
                                    format(box_info['meta']['name'], box_info['status']['isStop'],
                                           box_info['status']['phase']))

    @retry(tries=120, delay=3)
    @print_for_call
    def is_box_running_new(self, box_name):
        boxes_info = self.boxs_info
        for box_info in boxes_info:
            if box_name in box_info['meta']['name']:
                if box_info['status']['phase'] == 'running' and 'deletionTimestamp' not in box_info['meta'] \
                        and 'running' in box_info['status']['containerStatuses'][0]['state']:
                    logger.info("The {} has already running !".format(box_info['meta']['name']))
                    break
                else:
                    raise Exception('{} exists exception, box status is {}!'.format(box_info['meta']['name'],
                                                                                    box_info['status']['phase']))
            elif box_info != boxes_info[-1]:
                continue
            else:
                raise Exception("Not found the {}".format(box_name))

    @print_for_call
    def is_gpu_healthy(self, gpu_quantity, gpu_path=None):
        if gpu_path:
            check_calculate_if_exist = "ls {}|grep calculate-resource".format(gpu_path)
            check_gpu = "{}/calculate-resource|awk 'NR>1 {{print $1,$6}}'".format(gpu_path)
        else:
            check_calculate_if_exist = "ls |grep calculate-resource"
            check_gpu = "./calculate-resource|awk 'NR>1 {{print $1,$6}}'"
        calculate_if_exist_results = self.run_cmd(check_calculate_if_exist)
        if calculate_if_exist_results['rc'] == 0 and calculate_if_exist_results['stdout']:
            logger.info("calculate-resource exist in current path,then check the gpu if lost")
        elif not calculate_if_exist_results['stdout'] and calculate_if_exist_results['rc'] == 1 and \
                not calculate_if_exist_results['stderr']:
            logger.warning("Not exist calculate-resource, ignore check gpu")
            return
        else:
            raise Exception("Run cmd:<{}> appear error, the output is {}".format(check_calculate_if_exist,
                                                                                 calculate_if_exist_results))
        check_point = False
        gpu_lost_list = {}
        check_gpu_results = self.run_cmd(check_gpu)

        if check_gpu_results['rc'] == 0 and check_gpu_results['stdout']:
            check_gpu_output = check_gpu_results['stdout'].strip().split("\n")
        else:
            raise Exception("Run cmd:<{}> appear error, the output is {}".format(check_gpu, check_gpu_results))

        for check_gpu_result in check_gpu_output:
            if int(check_gpu_result.split(' ')[-1].split('/')[-1]) != gpu_quantity:
                gpu_lost_list[check_gpu_result.split(' ')[0]] = check_gpu_result.split(' ')[-1]
                check_point = True
        if check_point:
            raise Exception("Appear gpu lost, check below results...\n{}".format(gpu_lost_list))
        else:
            logger.info("All gpu are healthy !")

    def is_box_restarted(self, box_name, before_restart_count):
        box_restart_count = self.get_box_info_by_name(box_name)['status']['restartCount']
        if box_restart_count > before_restart_count:
            return True
        else:
            return False

    @property
    def running_boxes_quantity(self):
        box_running_number = 0
        for box in self.boxs_info:
            if box['status']['phase'] == 'running':
                box_running_number += 1
        return box_running_number

    @property
    def seam_br_ip(self):
        cmd = "ip addr show dev seam-br|grep inet|awk '{print $2}'"
        rtn_dict = self.run_cmd(cmd)
        if rtn_dict['rc'] == 0 and rtn_dict['stderr'] == '':
            seam_br_ip = rtn_dict['stdout'].split('/')[0].strip()
        else:
            logger.warning(rtn_dict)
            seam_br_ip = None
        return seam_br_ip


if __name__ == '__main__':
    nb_ip = '10.0.3.74'
    nb_user = 'root'
    nb_pwd = 'password'
    node_obj = NodeObj(nb_ip, nb_user, nb_pwd)
    print(node_obj.etcds_info)