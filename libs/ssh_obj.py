# coding: utf-8
import os
import json
import random
import socket
import time

import yaml
import paramiko
import traceback

import utils.times
from libs.log_obj import LogObj
from concurrent.futures import ThreadPoolExecutor, as_completed
from paramiko.ssh_exception import SSHException
from utils.decorator import lock, retry, print_for_call

logger = LogObj().get_logger()


class SSHObj(object):
    _ssh = None
    _sftp = None

    def __init__(self, ip, username, password, port=22, key_file=None, conn_timeout=60):
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port
        self.key_file = key_file
        self.conn_timeout = conn_timeout

    @property
    @lock
    @retry(tries=5, delay=5)
    def ssh(self):
        if self._ssh is None or self._ssh.get_transport() is None or not self._ssh.get_transport().is_active():
            logger.info('{0}: Init ssh'.format(self.ip))
            self._ssh = paramiko.SSHClient()
            self._ssh.load_system_host_keys()
            self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            try:
                if self.key_file is not None:
                    pkey = paramiko.RSAKey.from_private_key_file(self.key_file)
                    self._ssh.connect(self.ip, self.port, self.username, self.password, timeout=self.conn_timeout,
                                      pkey=pkey)
                else:
                    self._ssh.connect(self.ip, self.port, self.username, self.password, timeout=self.conn_timeout)
            except SSHException as e:
                logger.warning('{0}: SSH session exception occured!'.format(self.ip))
                self._ssh = None
                raise e
            except Exception as e:
                logger.warning('{0}: SSH connect fail, error is {1}!'.format(self.ip, traceback.format_exc()))
                raise e

        return self._ssh

    @property
    def sftp(self):
        #         if self._sftp is None:
        #             self._sftp = paramiko.SFTPClient.from_transport(self.ssh.get_transport())
        self._sftp = self.ssh.open_sftp()

        return self._sftp

    def run_cmd(self, cmd, sudo=False, timeout=None):
        rtn_dict = {}
        if self.key_file is not None:
            self.password = None
        if sudo:
            cmd = 'sudo {cmd}'.format(cmd=cmd)
        logger.debug('{0}: {1}'.format(self.ip, cmd))
        try:
            if sudo and self.password is not None:
                stdin, stdout, stderr = self.ssh.exec_command(cmd, get_pty=True, timeout=timeout)
                stdin.write(self.password + '\n')
                stdin.flush()
            else:
                stdin, stdout, stderr = self.ssh.exec_command(cmd, timeout=timeout)

            rtn_dict['stdout'] = stdout.read().decode("utf8", "ignore")
            rtn_dict['stderr'] = stderr.read().decode("utf8", "ignore")
            rtn_dict['rc'] = stdout.channel.recv_exit_status()
        except SSHException as e:
            logger.error('{0}: Run cmd {1} occured SSHException, error is {2}, will re-inited ssh session!'.format(
                self.ip, cmd, traceback.format_exc()))
            self._ssh = None
            raise e
        except Exception as e:
            logger.error('{0}: Run cmd {1} fail, error is {2}!'.format(self.ip, cmd, traceback.format_exc()))
            raise e
        return rtn_dict

    def multi_run_cmd(self, cmd_list):
        pool = ThreadPoolExecutor(max_workers=8)
        futures = []
        rtn_list = []

        for cmd in cmd_list:
            futures.append(pool.submit(self.run_cmd, cmd))

        pool.shutdown()
        for future in as_completed(futures):
            rtn_list.append(future.result())

        return rtn_list

    @retry(tries=20, delay=10)
    def remote_scp_put(self, local_path, remote_path):
        """
        scp put --paramiko
        @params:
          (char) host_ip
          (char) remote_path
          (char) local_path
          (char) username
          (char) password
        @output:
          (void)
        """
        logger.debug('scp %s %s@%s:%s' % (local_path, self.username, self.ip, remote_path))

        try:
            self.sftp.put(local_path, remote_path)
        except Exception as e:
            logger.error(traceback.format_exc())
            raise e
        finally:
            self.sftp.close()
            self.ssh.close()

    @retry(tries=20, delay=10)
    def remote_scp_get(self, local_path, remote_path):
        """
        scp put --paramiko
        @params:
          (char) host_ip
          (char) remote_path
          (char) local_path
          (char) username
          (char) password
        @output:
          (void)
        """
        logger.debug('scp %s@%s:%s %s' % (self.username, self.ip, remote_path, local_path))

        try:
            self.sftp.get(remote_path, local_path)
        except Exception as e:
            logger.error(traceback.format_exc())
            raise e
        finally:
            self.sftp.close()
            self.ssh.close()

    @property
    def cpu_type(self):
        cmd = 'uname -m'
        rtn_dict = self.run_cmd(cmd)
        if rtn_dict['rc'] == 0 and rtn_dict['stderr'] == '':
            return rtn_dict['stdout'].strip()
        else:
            raise Exception('Get {0} cpu type fail!'.format(self.ip))

    def force_reboot(self):
        cmd = 'echo "b" > /proc/sysrq-trigger'
        try:
            self.run_cmd(cmd, timeout=10)
        except socket.timeout:
            logger.info('Force reboot {0} done!'.format(self.ip))
        except Exception as e:
            logger.debug('Exception occured, error is {0}!'.format(e))
            raise e

    def get_pid_by_name(self, process_name):
        cmd = 'ps -ef|grep {0}|grep -v grep'.format(process_name)
        rtn_dict = self.run_cmd(cmd, timeout=60)
        if rtn_dict['rc'] == 0 and rtn_dict['stderr'] == '':
            return rtn_dict['stdout'].split()[1]
        else:
            logger.error('Get process {0} pid fail, error is {1}!'.format(process_name, rtn_dict))
            return None

    def kill_process(self, pid):
        cmd = 'kill -9 {0}'.format(pid)
        rtn_dict = self.run_cmd(cmd)
        if rtn_dict['rc'] == 0 and rtn_dict['stderr'] == '':
            logger.info('Kill {0} done on {1}!'.format(pid, self.ip))
        else:
            logger.error(rtn_dict)
            raise Exception('Kill {0} fail on {1}!'.format(pid, self.ip))

    def kill_service_by_name(self, process_name):
        cmd = "ps -ef|grep {0}|grep -v grep|awk '{{print $2}}'|xargs kill -9".format(process_name)
        rtn_dict = self.run_cmd(cmd, timeout=60)
        if rtn_dict['rc'] == 0 and rtn_dict['stderr'] == '':
            logger.info('Kill {0} done on {1}!'.format(process_name, self.ip))
        elif rtn_dict['rc'] == 123:
            logger.warning(f"Not found the {process_name}'s pid!")
            logger.warning(rtn_dict)
        else:
            logger.error(rtn_dict)
            raise Exception('Kill {0} fail on {1}!'.format(process_name, self.ip))

    def docker_exec(self, docker_name, command):
        cmd = 'docker exec -i {0} {1}'.format(docker_name, command)
        rtn_dict = self.run_cmd(cmd)
        if rtn_dict['rc'] == 0 and rtn_dict['stderr'] == '':
            return rtn_dict['stdout'].strip()
        else:
            logger.error(rtn_dict)
            raise Exception('{0}: docker exec {1} failed into {2} docker!'.format(self.ip, command, docker_name))

    def docker_build(self, dockerfile_path, repository_tag):
        cmd = 'docker build -f {0} -t {1} .'.format(dockerfile_path, repository_tag)
        rtn_dict = self.run_cmd(cmd)
        if rtn_dict['rc'] == 0 and rtn_dict['stderr'] == '':
            return rtn_dict['stdout'].strip()
        else:
            logger.error(rtn_dict)
            raise Exception('{0}: docker build {1} failed!'.format(self.ip, dockerfile_path))

    def docker_save(self, pkg_name, repository_tag):
        cmd = 'docker save -o {0} {1}'.format(pkg_name, repository_tag)
        rtn_dict = self.run_cmd(cmd)
        if rtn_dict['rc'] == 0 and rtn_dict['stderr'] == '':
            logger.info('{0}: docker save {0} done!'.format(self.ip, pkg_name))
        else:
            logger.error(rtn_dict)
            raise Exception('{0}: docker save {0} failed!'.format(self.ip, pkg_name))

    def docker_cp(self, path1, path2):
        cmd = 'docker cp {0} {1}'.format(path1, path2)
        rtn_dict = self.run_cmd(cmd)
        if rtn_dict['rc'] == 0 and rtn_dict['stderr'] == '':
            logger.info('Docker cp {0} to {1} done!'.format(path1, path2))
        else:
            logger.error(rtn_dict)
            raise Exception('Docker cp {0} to {1} failed!'.format(path1, path2))

    @property
    def images(self):
        cmd = 'docker images --format "{{.Repository}}:{{.Tag}}"'
        rtn_dict = self.run_cmd(cmd)
        if rtn_dict['rc'] == 0 and rtn_dict['stderr'] == '':
            return rtn_dict['stdout'].strip().split('\n')

    def docker_pull(self, image):
        cmd = 'docker pull {0}'.format(image)
        rtn_dict = self.run_cmd(cmd)
        if rtn_dict['rc'] == 0 and rtn_dict['stderr'] == '':
            logger.debug(rtn_dict['stdout'])
            logger.info('Docker pull image {0} to {1} done!'.format(image, self.ip))
        else:
            logger.error(rtn_dict)
            raise Exception('Docker pull image {0} to {1} fail!'.format(image, self.ip))

    def docker_tag(self, remote_image, local_image):
        cmd = 'docker tag {0} {1}'.format(remote_image, local_image)
        rtn_dict = self.run_cmd(cmd)
        if rtn_dict['rc'] == 0 and rtn_dict['stderr'] == '':
            logger.debug(rtn_dict['stdout'])
            logger.info('Docker tag image {0} to {1} done!'.format(local_image, self.ip))
        else:
            logger.error(rtn_dict)
            raise Exception('Docker tag image {0} to {1} fail!'.format(local_image, self.ip))

    def docker_push(self, image):
        cmd = 'docker push {0}'.format(image)
        rtn_dict = self.run_cmd(cmd)
        if rtn_dict['rc'] == 0 and rtn_dict['stderr'] == '':
            logger.debug(rtn_dict['stdout'])
            logger.info('Docker push image {0} to {1} done!'.format(image, self.ip))
        else:
            logger.error(rtn_dict)
            raise Exception('Docker push image {0} to {1} fail!'.format(image, self.ip))

    def docker_logs(self, docker_name, log_dir):
        log_file_path = os.path.join('{0}/'.format(log_dir), '{0}.log'.format(docker_name))
        cmd = 'docker logs {0} > {1} 2>&1'.format(docker_name, log_file_path)
        rtn_dict = self.run_cmd(cmd)
        if rtn_dict['rc'] == 0 and rtn_dict['stderr'] == '':
            logger.info('Collect docker {0} logs to {1}:{2} done!'.format(docker_name, self.ip, log_file_path))
        else:
            logger.error(rtn_dict)
            raise Exception('Collect docker {0} logs to {1}:{2} failed!'.format(docker_name, self.ip, log_file_path))

    def dockers_kill(self, component_name):
        cmd = f"docker ps |grep '{component_name}'|awk '{{print $1}}'|xargs docker kill "
        rtn_dict = self.run_cmd(cmd, timeout=60)
        if rtn_dict['rc'] == 0 and rtn_dict['stderr'] == '':
            logger.info(f'Docker kill {component_name} done on {self.ip}!')
        elif rtn_dict['rc'] == 123:
            logger.warning(f"Not found the {component_name}'s container!")
            logger.warning(rtn_dict)
        else:
            logger.error(rtn_dict)
            raise Exception(f'Docker kill {component_name} fail on {self.ip}!')

    def docker_inspect(self, docker_name):
        cmd = 'docker inspect {0}'.format(docker_name)
        rtn_dict = self.run_cmd(cmd)
        if rtn_dict['rc'] == 0 and rtn_dict['stderr'] == '':
            return json.loads(rtn_dict['stdout'])
        else:
            logger.error(rtn_dict)
            raise Exception('docker inspect {0} failed!'.format(docker_name))

    def clean_docker_log(self, docker_name):
        docker_info = self.docker_inspect(docker_name)[0]
        docker_log_path = docker_info['LogPath']
        cmd = 'echo > {0}'.format(docker_log_path)
        rtn_dict = self.run_cmd(cmd)
        if rtn_dict['rc'] == 0:
            logger.info('clean docker {0} log done!'.format(docker_name))
        else:
            logger.error(rtn_dict)
            raise Exception('Clean docker {0} log failed!'.format(docker_name))

    @property
    def dockers_info(self):
        dockers_info = []
        cmd = 'docker ps -a --no-trunc --format "{{.Names}}==={{.Command}}==={{.ID}}==={{.State}}==={{.Status}}===' \
              '{{.RunningFor}}==={{.CreatedAt}}"'
        rtn_dict = self.run_cmd(cmd, timeout=60)
        if rtn_dict['rc'] == 0 and rtn_dict['stderr'] == '':
            all_info = rtn_dict['stdout'].strip().split('\n')
            key_list = ['name', 'command', 'id', 'state', 'status', 'running_for', 'created_at']
            for docker_info in all_info:
                docker_info_list = docker_info.split('===')
                dockers_info.append(dict(zip(key_list, docker_info_list)))
        else:
            logger.error(rtn_dict)
            raise Exception('Get {0} dockers fail!'.format(self.ip))
        return dockers_info

    @property
    def dockers_name(self):
        dockers_name = []
        for docker_info in self.dockers_info:
            dockers_name.append(docker_info['name'])
        return dockers_name

    def get_docker_info_by_name(self, docker_name):
        for docker_info in self.dockers_info:
            if docker_info['name'] == docker_name:
                return docker_info
        else:
            raise Exception('Docker {0} is not exist!'.format(docker_name))

    @retry(tries=60, delay=5)
    def is_docker_ok_by_name(self, docker_name):
        docker_info = self.get_docker_info_by_name(docker_name)
        docker_state = docker_info['state']
        docker_status = docker_info['status']
        docker_created_at = docker_info['created_at']

        if docker_state != 'running':
            raise Exception('{0} dockers {1} is not running, its state is {2}!'.format(self.ip, docker_name,
                                                                                       docker_state))
        else:
            logger.info('{0} dockers {1} is running, its status is {2}, it is create at {3}!'.format(self.ip,
                                                                                                     docker_name,
                                                                                                     docker_status,
                                                                                                     docker_created_at))

    def make_dir(self, dir_path):
        cmd = 'ls {0}'.format(dir_path)
        rtn_dict = self.run_cmd(cmd)
        if rtn_dict['rc'] == 0 and rtn_dict['stderr'] == '':
            logger.info('Dir {0} had existed on {1}, the files inside are {2}!'.format(dir_path, self.ip,
                                                                                       rtn_dict['stdout'].strip()))
        else:
            logger.debug(rtn_dict)
            logger.info('Dir {0} is not exist on {1}, will create it!'.format(dir_path, self.ip))
            cmd = 'mkdir -p {0}'.format(dir_path)
            rtn_dict = self.run_cmd(cmd)
            if rtn_dict['rc'] == 0:
                logger.info('Make dir {0} done!'.format(dir_path))
            else:
                logger.error(rtn_dict)
                raise Exception('Make dir {0} fail!'.format(dir_path))

    def collect_process_core_dump(self, process_name, core_dump_dir):
        pid = self.get_pid_by_name(process_name)
        if pid:
            cmd = 'gcore -o {0}/{1}.core {2}'.format(core_dump_dir, process_name, pid)
            rtn_dict = self.run_cmd(cmd)
            logger.debug(rtn_dict)
            if rtn_dict['rc'] == 0 and 'Saved corefile' in rtn_dict['stdout']:
                logger.info(rtn_dict['stdout'])
                logger.info('Collect {0} {1} core dump file to {2} done!'.format(self.ip, process_name,
                                                                                 core_dump_dir))
            else:
                logger.error(rtn_dict)
                raise Exception('Collect {0} {1} core dump file to {2} fail!'.format(self.ip, process_name,
                                                                                     core_dump_dir))

    def load_yaml_data(self, yaml_file):
        cmd = 'cat {0}'.format(yaml_file)
        rtn_dict = self.run_cmd(cmd, timeout=60)
        if rtn_dict['rc'] == 0 and rtn_dict['stderr'] == '':
            yaml_data = yaml.load(rtn_dict['stdout'], Loader=yaml.FullLoader)
            return yaml_data
        else:
            logger.error(rtn_dict)
            raise Exception('Get {0} yaml {1} data fail!'.format(self.ip, yaml_file))

    def compress(self, package_file_path, dir_path):
        cmd = 'tar -zcvPf {0} {1}'.format(package_file_path, dir_path)
        rtn_dict = self.run_cmd(cmd)
        if rtn_dict['rc'] == 0 and rtn_dict['stderr'] == '':
            logger.info('Compress {0} to {1} done!'.format(dir_path, package_file_path))
        else:
            logger.error(rtn_dict)
            raise Exception('Compress {0} to {1} failed!'.format(dir_path, package_file_path))

    def get_service_status_by_name(self, service_name):
        cmd = 'systemctl status {0}'.format(service_name)
        rtn_dict = self.run_cmd(cmd, timeout=30)
        if rtn_dict['stderr'] == '':
            for stdout in rtn_dict['stdout'].split('\n'):
                if 'Active' in stdout:
                    return stdout.split()[1]
        else:
            logger.error(rtn_dict)
            raise Exception('Get service {0} status failed!'.format(service_name))

    @retry(tries=120, delay=5)
    def is_service_active_by_name(self, service_name):
        status = self.get_service_status_by_name(service_name)
        if status != 'active':
            raise Exception('{0}: Service {1} is not active, its status is {2}!'.format(self.ip, service_name, status))
        logger.info('{0}: Service {1} is {2}!'.format(self.ip, service_name, status))

    @print_for_call
    def is_docker_active(self):
        self.is_service_active_by_name('docker')

    @retry(tries=60, delay=5)
    def is_process_up_by_name(self, process_name):
        cmd = 'ps -ef|grep {0}|grep -v grep'.format(process_name)
        rtn_dict = self.run_cmd(cmd, timeout=30)
        if rtn_dict['rc'] != 0 or process_name not in rtn_dict['stdout']:
            logger.error(rtn_dict)
            raise Exception('{0} {1} process is not up yet!'.format(self.ip, process_name))
        else:
            logger.info(rtn_dict['stdout'])
            logger.info('{0} {1} process is up!'.format(self.ip, process_name))

    def extract(self, package_file_path, extract_path='.'):
        cmd = 'tar -xvf {} -C {}'.format(package_file_path, extract_path)
        rtn_dict = self.run_cmd(cmd)
        if rtn_dict['rc'] == 0 and rtn_dict['stderr'] == '':
            logger.info('Extract {0} to {1} done!'.format(package_file_path, extract_path))
        else:
            logger.error(rtn_dict)
            raise Exception('Extract {0} to {1} failed!'.format(package_file_path, extract_path))

    def dd_file(self, device='zero', file_path='/mnt', count='1024', bs='1MB'):
        file_name = '{}_{}_{}'.format('dd', int(time.time() * 1000), random.randint(1, 10000))
        all_file_path = '{}/{}'.format(file_path, file_name)
        cmd = 'dd if=/dev/{} of={} count={} bs={}'.format(device, all_file_path, count, bs)
        rtn_dict = self.run_cmd(cmd)

        if rtn_dict['rc'] == 0 and 'copied' in rtn_dict['stderr']:
            logger.info('DD size {} file done'.format(count + 'x' + bs))
            return "Exist space"
        elif rtn_dict['rc'] == 1 and "No space left on device" in rtn_dict['stderr']:
            logger.warning("The storage of {} has no available volume".format(file_path))
            return "No space"
        else:
            logger.error(rtn_dict)
            raise Exception('DD size is {} file fail'.format(count + 'x' + bs))

    def dd_file_until_no_space(self, device='zero', file_path='/mnt', count='1024', bs='1MB'):
        exist_space = True
        while exist_space:
            results = self.dd_file(device, file_path, count, bs)
            if "No space" == results:
                exist_space = False
            utils.times.sleep(0.5)
        logger.info("The storage has used fully")

    def remove_file(self, file_path):
        cmd = "rm -rf {}".format(file_path)
        rtn_dict = self.run_cmd(cmd)

        if rtn_dict['stderr'] == '' and rtn_dict['rc'] == 0:
            logger.info("The file {} has deleted".format(file_path))
        else:
            logger.error(rtn_dict)
            raise Exception("The file {} delete fail".format(file_path))

    @retry(tries=360, delay=10)
    def is_ceph_health_ok(self):
        cmd = "ceph -s"
        rtn_dict = self.run_cmd(cmd, timeout=60)

        if rtn_dict['rc'] == 0 and 'HEALTH_OK' in rtn_dict['stdout']:
            logger.info("The ceph cluster's health is ok")
        else:
            logger.warning(rtn_dict)
            raise Exception("The ceph's health is error")

    def sync_storage(self, docker_name, storage_path):
        command = "cd {};sync".format(storage_path)

        cmd = "docker exec -i {0} bash -c '{1}'".format(docker_name, command)
        rtn_dict = self.run_cmd(cmd, timeout=60)
        if rtn_dict['rc'] == 0:
            logger.info("Sync successfully")
        else:
            logger.warning(rtn_dict)
            raise Exception("Sync appear error")


if __name__ == '__main__':
    ssh_obj = SSHObj('192.168.5.61', 'root', 'password')
    results = ssh_obj.dockers_name
    print(results)

    # cmd = 'docker images|awk \'NR>1{print $1\":\"$2}\''
    # rtn_dict = ssh_obj.run_cmd(cmd)
    # for image in rtn_dict['stdout'].split():
    #     image_tar = '{0}.tar'.format(image.split(':')[0].split('/')[-1])
    #     cmd = 'docker save -o /home/dockerimages/{0} {1}'.format(image_tar, image)
    #     rtn_dict = ssh_obj.run_cmd(cmd)
    #     print(rtn_dict)
