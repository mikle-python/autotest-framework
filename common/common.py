import random
import os
import re
import yaml
import psutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict, OrderedDict
from utils.decorator import retry
from utils.util import run_cmd, time_str
from utils.times import str_to_datetime
from settings.global_settings import WINDOWS, LOCAL_TEMP_PATH
from libs.log_obj import LogObj
from libs.ssh_obj import SSHObj
from zipfile import ZipFile
from tarfile import TarFile

logger = LogObj().get_logger()


@retry(tries=120, delay=3)
def is_ping_ok(ip):
    if WINDOWS:
        cmd = 'ping -n 3 {0}'.format(ip)
    else:
        cmd = 'ping -c 3 {0}'.format(ip)
    rtn_dict = run_cmd(cmd)
    if rtn_dict['rc'] != 0:
        logger.error(rtn_dict)
        raise Exception('Ping {0} is not ok!'.format(ip))
    else:
        logger.info('Ping {0} is ok!'.format(ip))


def dump_yaml_data(yaml_data, yaml_file_path=None):
    if not yaml_file_path:
        yaml_file_name = '{0}-{1}.yaml'.format(time_str(), random.randint(0, 99999))
        if not os.path.exists(LOCAL_TEMP_PATH):
            os.makedirs(LOCAL_TEMP_PATH)
        yaml_file_path = os.path.join(LOCAL_TEMP_PATH, yaml_file_name)
    with open(yaml_file_path, mode='w') as file_obj:
        yaml.dump(yaml_data, stream=file_obj, sort_keys=False)
    return yaml_file_path


def load_yaml(yaml_file_path):
    with open(yaml_file_path, mode='r', encoding='utf-8') as file_obj:
        yaml_data = yaml.load(file_obj, Loader=yaml.FullLoader)
    return yaml_data


def get_cpu_usage():
    cpu_usage = defaultdict(float)
    cpu_usage['percent'] = psutil.cpu_percent()
    scputimes = psutil.cpu_times_percent()
    cpu_usage['user'] = scputimes.user
    cpu_usage['system'] = scputimes.system
    cpu_usage['idle'] = scputimes.idle
    if not WINDOWS:
        cpu_usage['iowait'] = scputimes.iowait
        cpu_usage['nice'] = scputimes.nice
    return cpu_usage


def get_memory_usage():
    memory_usage = defaultdict(int)
    svmem = psutil.virtual_memory()
    memory_usage['total'] = svmem.total
    memory_usage['available'] = svmem.available
    memory_usage['percent'] = svmem.percent
    memory_usage['used'] = svmem.used
    memory_usage['free'] = svmem.free
    if not WINDOWS:
        memory_usage['buffers'] = svmem.buffers
        memory_usage['cached'] = svmem.cached
    return memory_usage


def compress_files(compress_path, file_path, write_mode='a', new_file_name=None, compress_type='tar'):
    if compress_type == 'zip':
        with ZipFile(compress_path, write_mode) as compress_obj:
            compress_obj.write(file_path, new_file_name)
        logger.info("The {} has compress to {}".format(file_path, compress_path))

    elif compress_type == 'tar':
        with TarFile(compress_path, write_mode) as compress_obj:
            compress_obj.add(file_path, new_file_name)
        logger.info("The {} has compress to {}".format(file_path, compress_path))
    return compress_path


def extract_files(compress_path, extract_folder=None):
    if not extract_folder:
        extract_folder = os.getcwd()
    with ZipFile(compress_path, 'r') as extract_obj:
        extract_obj.extractall(extract_folder)
    logger.info("The {} extract files done")
    return extract_folder


def collect_docker_logs(nodes_ip, dockers_name_pattern):
    new_time_str = time_str()
    base_log_dir = '/root/neiltest_log/'
    log_dir = os.path.join(base_log_dir, new_time_str)
    pool = ThreadPoolExecutor(max_workers=10)
    futures = []

    for node_ip in nodes_ip:
        ssh_obj = SSHObj(node_ip, 'root', 'password')
        ssh_obj.make_dir(log_dir)
        dockers_name = ssh_obj.dockers_name
        for docker_name_pattern in dockers_name_pattern:
            for docker_name in dockers_name:
                if docker_name_pattern in docker_name:
                    futures.append(pool.submit(ssh_obj.docker_logs, docker_name, log_dir))
    pool.shutdown()
    for future in as_completed(futures):
        future.result()

    for node_ip in nodes_ip:
        ssh_obj = SSHObj(node_ip, 'root', 'password')
        package_name = '{0}-{1}.tar.gz'.format('_'.join(node_ip.split('.')), new_time_str)
        package_file_path = os.path.join(base_log_dir, package_name)
        local_package_file_path = os.path.join(LogObj._instance.log_dir, package_name)
        ssh_obj.compress(package_file_path, log_dir)
        ssh_obj.remote_scp_get(local_package_file_path, package_file_path)
        logger.info('Copy log files to local {0} done!'.format(local_package_file_path))
        ssh_obj.run_cmd('rm -rf {0}'.format(base_log_dir))

    logger.info('All logs have been collected to {0} of each node!'.format(log_dir))


def get_iostats(device, ip, username, password, count=1):
    device_name = device.split('/')[-1]
    cmd = "iostat -mxcdt -p {device} -y 1 {count}".format(device=device, count=count)
    ssh_obj = SSHObj(ip, username, password)
    rtn_dict = ssh_obj.run_cmd(cmd)
    iostats = {}
    if rtn_dict['rc'] == 0:
        time_pattern = r"\d{1,2}/\d{1,2}/\d{2,4}\s+\d{1,2}:\d{1,2}:\d{1,2}"
        stdout_list = rtn_dict['stdout'].strip().split('\n')
        for stdout in stdout_list:
            m = re.search(time_pattern, stdout)
            if m:
                time_str = m.group()
                c_time = str_to_datetime(time_str, fmt='%m/%d/%Y %I:%M:%S')
                iostats[c_time] = dict()

            if device_name in stdout:
                device_io_stat_list = stdout.split()
                r_iops = int(float(device_io_stat_list[3]))
                w_iops = int(float(device_io_stat_list[4]))
                r_throughput = int(float(device_io_stat_list[5]))
                w_throughput = int(float(device_io_stat_list[6]))
                util = float(device_io_stat_list[-1])

                iostats[c_time]['r_iops'] = r_iops
                iostats[c_time]['w_iops'] = w_iops
                iostats[c_time]['r_throughput'] = r_throughput
                iostats[c_time]['w_throughput'] = w_throughput
                iostats[c_time]['util'] = util
    return iostats


if __name__ == '__main__':
    iostats = get_iostats('/dev/sda', '192.168.5.5', 'root', 'password')
    print(iostats)