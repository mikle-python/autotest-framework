import yaml
import datetime
from prettytable import PrettyTable
from libs.ssh_obj import SSHObj
from libs.log_obj import LogObj
from utils.decorator import retry, print_for_call
from utils.util import str_to_datetime
from settings.ecos_settings import ETCDCTL


logger = LogObj().get_logger()


class NodeObj(SSHObj):
    def __init__(self, ip, username='root', password='password'):
        super(NodeObj, self).__init__(ip, username, password)

    def get_controllers_info_by_kind(self, controller_kind):
        controllers_info = []
        cmd = 'kubectl get {0} -A -o yaml'.format(controller_kind)
        rtn_dict = self.run_cmd(cmd)
        if rtn_dict['rc'] == 0 and rtn_dict['stderr'] == '':
            if 'No resources found' not in rtn_dict['stdout']:
                all_info = yaml.load(rtn_dict['stdout'], Loader=yaml.FullLoader)['items']
                if isinstance(all_info, list):
                    controllers_info.extend(all_info)
                else:
                    controllers_info.append(all_info)
        else:
            logger.error(rtn_dict)
            raise Exception('Exception occured, result is {0}!'.format(rtn_dict))

        tb = PrettyTable()
        if controller_kind == 'pod':
            tb.field_names = ['Namespace', 'Name', 'READY', 'STATUS', 'RESTARTS', 'AGE', 'PodIP', 'NODE']
        elif controller_kind == 'node':
            tb.field_names = ['Name', 'STATUS', 'ROLES', 'AGE', 'INTERNAL-IP', 'OS-IMAGE', 'KERNEL-VERSION']
        for controller_info in controllers_info:
            controller_info['customization'] = dict()
            name = controller_info['metadata']['name']
            creation_time_stamp = controller_info['metadata']['creationTimestamp']
            tmp_create_time = creation_time_stamp.split('T')
            create_time = str_to_datetime(
                ' '.join([tmp_create_time[0], tmp_create_time[1].strip('Z').split('+')[0]]),
                fmt="%Y-%m-%d %H:%M:%S")
            age = datetime.datetime.now() - create_time
            if controller_kind == 'pod':
                namespace = controller_info['metadata']['namespace']
                ready_flag = 0
                restarts = 0
                if 'containerStatuses' in controller_info['status']:
                    for container_status in controller_info['status']['containerStatuses']:
                        restarts = restarts + container_status['restartCount']
                        if container_status['ready']:
                            ready_flag = ready_flag + 1
                ready = '{0}/{1}'.format(ready_flag, len(controller_info['spec']['containers']))
                phase = controller_info['status']['phase']
                if 'podIP' in controller_info['status']:
                    pod_ip = controller_info['status']['podIP']
                else:
                    pod_ip = None
                if 'nodeName' in controller_info['spec']:
                    node = controller_info['spec']['nodeName']
                else:
                    node = None
                tb.add_row([namespace, name, ready, phase, restarts, age, pod_ip, node])
            elif controller_kind == 'node':
                os_image = controller_info['status']['nodeInfo']['osImage']
                kernel_version = controller_info['status']['nodeInfo']['kernelVersion']
                for address_info in controller_info['status']['addresses']:
                    if address_info['type'] == 'InternalIP':
                        internal_ip = address_info['address']
                controller_info['customization']['internal_ip'] = internal_ip
                role_list = []
                for label_key, label_value in controller_info['metadata']['labels'].items():
                    if 'node-role.kubernetes.io' in label_key and label_value == 'true':
                        role = label_key.split('/')[-1]
                        role_list.append(role)
                if 'master' in role_list:
                    controller_info['customization']['master'] = True
                else:
                    controller_info['customization']['master'] = False
                roles = ','.join(role_list)
                status = controller_info['status']['conditions'][-1]['type']
                if controller_info['status']['conditions'][-1]['status'] == "True":
                    controller_info['customization']['ready'] = True
                else:
                    controller_info['customization']['ready'] = False
                tb.add_row([name, status, roles, age, internal_ip, os_image, kernel_version])
        if controller_kind in ['pod', 'node'] and controllers_info:
            logger.debug('\n{0}'.format(tb))
        return controllers_info

    @property
    def pods_info(self):
        return self.get_controllers_info_by_kind('pod')

    @property
    def nodes_info(self):
        return self.get_controllers_info_by_kind('node')

    @property
    def master_nodes_ip(self):
        master_nodes_ip = []
        for node_info in self.nodes_info:
            if node_info['customization']['master']:
                master_nodes_ip.append(node_info['customization']['internal_ip'])
        return master_nodes_ip

    @property
    def nodes_ip(self):
        nodes_ip = []
        for node_info in self.nodes_info:
            nodes_ip.append(node_info['customization']['internal_ip'])
        return nodes_ip

    @retry(tries=120, delay=5)
    @print_for_call
    def is_pods_running(self):
        pods_not_running = []
        for pod_info in self.pods_info:
            if pod_info['status']['phase'] == 'Succeeded':
                continue
            if pod_info['status']['phase'] != 'Running':
                pods_not_running.append(pod_info['metadata']['name'])
            else:
                containers_not_ready = []
                for container_status_info in pod_info['status']['containerStatuses']:
                    if not container_status_info['ready']:
                        containers_not_ready.append(container_status_info['name'])
                if containers_not_ready:
                    raise Exception('Containers {0} are not ready!'.format(containers_not_ready))
        if pods_not_running:
            raise Exception('Pods {0} are not running!'.format(pods_not_running))
        logger.info('All pods are running and all containers ready!')

    @retry(tries=120, delay=5)
    @print_for_call
    def is_nodes_ready(self):
        nodes_not_ready = []
        for node_info in self.nodes_info:
            if not node_info['customization']['ready']:
                nodes_not_ready.append(node_info['metadata']['name'])
        if nodes_not_ready:
            raise Exception('Nodes {0} are not ready!'.format(nodes_not_ready))
        logger.info('All nodes ready!')

    def delete_pod(self, namespace, pod_name, force=False):
        if force:
            cmd = f"kubectl delete pod -n {namespace} {pod_name} --grace-period=0 --force"
            rtn_dict = self.run_cmd(cmd, timeout=60)
            if rtn_dict['rc'] == 0 and 'resource has been terminated' in rtn_dict['stderr']:
                logger.info(f'POD {pod_name} force deleted!')
            else:
                logger.error(rtn_dict)
                raise Exception(f'POD {pod_name} force delete fail on {self.ip}!')
        else:
            cmd = f"kubectl delete pod -n {namespace} {pod_name}"
            rtn_dict = self.run_cmd(cmd, timeout=120)
            if rtn_dict['rc'] == 0 and rtn_dict['stderr'] == '':
                logger.info(f'POD {pod_name} grace period deleted!')
            else:
                logger.error(rtn_dict)
                raise Exception(f'POD {pod_name} grace period delete fail on {self.ip}!')

    @property
    def etcds_info(self):
        etcd_table = PrettyTable()
        etcd_table.field_names = ['ETCD NODE IP', 'ETCD PORT', 'ETCD STATUS', 'ETCD NODE']
        etcds_info = []
        cmd = f'{ETCDCTL} member list'
        rtn_dict = self.run_cmd(cmd)
        if rtn_dict['rc'] == 0:
            for tmp_info in rtn_dict['stdout'].strip().split('\n'):
                etcd_info = dict()
                tmp_info_list = tmp_info.split(',')
                etcd_addr = tmp_info_list[4].split('://')[1]
                etcd_addr_list = etcd_addr.split(':')
                etcd_info['ip'] = etcd_addr_list[0]
                etcd_info['port'] = etcd_addr_list[1]
                etcd_info['status'] = tmp_info_list[1].strip()
                etcd_info['node'] = tmp_info_list[2].strip()
                etcds_info.append(etcd_info)
                etcd_table.add_row([etcd_info['ip'], etcd_info['port'], etcd_info['status'], etcd_info['node']])
            logger.info(f"ETCD INFOS\n{etcd_table}")
            return etcds_info
        else:
            logger.error(rtn_dict)
            raise Exception('Get etcd info fail, result is {0}!'.format(rtn_dict))

    @retry(tries=60, delay=5)
    @print_for_call
    def is_etcd_ok(self):
        for etcd_info in self.etcds_info:
            if etcd_info['status'] != 'started':
                raise Exception('etcd info: {0}'.format(etcd_info))
            else:
                logger.info('Etcd {0} status is {1}!'.format(etcd_info['ip'], etcd_info['status']))


if __name__ == '__main__':
    import json
    node_obj = NodeObj('192.168.6.241', password='password')
    print(node_obj.master_nodes_ip)
    # print(json.dumps(node_obj.nodes_info, indent=4))
