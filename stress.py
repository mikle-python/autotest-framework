import os
import pytest
from stress import arguments
from runner import run
from libs.log_obj import LogObj
from utils.times import time_str

args = arguments.parse_arg()
project = 'stress'

result = run(project, args)
logger = LogObj().get_logger()
if result != pytest.ExitCode.OK and result != pytest.ExitCode.INTERRUPTED:
    if args.ip and args.collect and args.action == 'newben':
        logger.info('Collect log start!')
        from stress.newben.common.common import collect_nb_docker_logs
        from stress.newben.common.node_obj import NodeObj

        new_time_str = time_str()
        node1_obj = NodeObj(args.ip, args.sys_user, args.sys_pwd)
        nodes_ip = node1_obj.nodes_ip
        nb_log_dir = '/root/neiltest_log/'
        log_dir = os.path.join(nb_log_dir, new_time_str)
        collect_nb_docker_logs(node1_obj, log_dir)
        for node_ip in nodes_ip:
            node_obj = NodeObj(node_ip, node1_obj.username, node1_obj.password)
            package_name = '{0}-{1}.tar.gz'.format('_'.join(node_ip.split('.')), new_time_str)
            package_file_path = os.path.join(nb_log_dir, package_name)
            local_package_file_path = os.path.join(LogObj._instance.log_dir, package_name)
            node_obj.compress(package_file_path, log_dir)
            node_obj.remote_scp_get(local_package_file_path, package_file_path)
            logger.info('Copy log files to local {0} done!'.format(local_package_file_path))
            node_obj.run_cmd('rm -rf {0}'.format(nb_log_dir))