import pytest
import os
from libs.log_obj import LogObj
from stress.newben.common.node_obj import NodeObj
from stress import arguments
from utils.util import time_str
from stress.newben.common.common import collect_nb_docker_logs, collect_nb_processes_core_dump
from settings.global_settings import PROJECT_PATH


logger = LogObj().get_logger()
args = arguments.parse_arg()


def test_collect_log(node1_obj):
    tmp_time_str = time_str()
    log_file_dir = LogObj._instance.log_dir
    nb_log_dir = '/root/neiltest_log/'
    log_dir = os.path.join(nb_log_dir, tmp_time_str)
    collect_nb_docker_logs(node1_obj, log_dir)
    for node_ip in node1_obj.nodes_ip:
        node_obj = NodeObj(node_ip, node1_obj.username, node1_obj.password)
        package_name = '{0}-{1}.tar.gz'.format('_'.join(node_ip.split('.')), tmp_time_str)
        package_file_path = os.path.join(nb_log_dir, package_name)
        local_package_file_path = os.path.join(log_file_dir, package_name)
        node_obj.compress(package_file_path, log_dir)
        node_obj.remote_scp_get(local_package_file_path, package_file_path)
        logger.info('Copy log files to local {0} done!'.format(local_package_file_path))
        node_obj.run_cmd('rm -rf {0}'.format(nb_log_dir))


def test_collect_core_dump(node1_obj):
    core_dump_dir = os.path.join('/root/neiltest_core_dump/', time_str())
    collect_nb_processes_core_dump(node1_obj, core_dump_dir)


