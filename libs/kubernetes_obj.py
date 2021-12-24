# coding: utf-8
from kubernetes import config, client
from kubernetes.stream import stream
from kubernetes.client.rest import ApiException
from libs.log_obj import LogObj
from utils.decorator import retry
import base64
from datetime import datetime

logger = LogObj().get_logger()


class KubernetesObj(object):
    is_connected = None
    _corev1api = None
    _appsv1betaapi = None
    _extensionsv1betaapi = None
    _appsv1api = None

    def __init__(self, host=None, config_path=None, secret=None, namespace='default'):
        self.config_path = config_path
        self.host = host
        self.secret = secret
        self.namespace = namespace

    def connect(self):
        client.configuration.assert_hostname = False
        try:
            config.load_kube_config(self.config_path)
        except Exception:
            client.Configuration.set_default(self.client_config)
        self.is_connected = True

    @property
    def client_config(self):
        configuration = client.Configuration()
        configuration.host = self.host
        configuration.verify_ssl = False
        configuration.debug = False
        configuration.api_key = {"authorization": "Bearer " + self.secret}
        return configuration

    @property
    def corev1api(self):
        if self._corev1api is None:
            if self.is_connected is None:
                self.connect()
            self._corev1api = client.CoreV1Api()
        return self._corev1api

    @property
    def appsv1betaapi(self):
        if self._appsv1betaapi is None:
            if self.is_connected is None:
                self.connect()
            self._appsv1betaapi = client.AppsV1beta1Api()
        return self._appsv1betaapi

    @property
    def extensionsv1betaapi(self):
        if self._extensionsv1betaapi is None:
            if self.is_connected is None:
                self.connect()
            self._extensionsv1betaapi = client.ExtensionsV1beta1Api()
        return self._extensionsv1betaapi

    @property
    def appsv1api(self):
        if self._appsv1api is None:
            if self.is_connected is None:
                self.connect()
            self._appsv1api = client.AppsV1Api()
        return self._appsv1api

    def get_pods_info(self, label_selector=None):
        if label_selector:
            all_info = self.corev1api.list_namespaced_pod(
                namespace=self.namespace,
                label_selector=label_selector
            )
        else:
            all_info = self.corev1api.list_namespaced_pod(
                namespace=self.namespace
            )

        # print(all_info.to_dict()['items'])
        # for pod_info in all_info.to_dict()['items']:
        return all_info.to_dict()['items']

        # pods_info = []
        # for pod_info in all_info.items:
        #     tmp_info = dict()
        #     tmp_info['name'] = pod_info.metadata.name
        #     tmp_info['labels'] = pod_info.metadata.labels
        #     tmp_info['creation_timestamp'] = pod_info.metadata.creation_timestamp
        #     tmp_info['deletion_timestamp'] = pod_info.metadata.deletion_timestamp
        #     now_time = datetime.now(tz=tmp_info['creation_timestamp'].tzinfo)
        #     pod_age = int((now_time - tmp_info['creation_timestamp']).total_seconds())
        #     if pod_age > 86400:
        #         d_info = divmod(pod_age, 86400)
        #         h_info = divmod(d_info[1], 3600)
        #         m_info = divmod(h_info[1], 60)
        #         tmp_info['age'] = '{d}d{h}h{m}m{s}s'.format(d=int(d_info[0]), h=int(h_info[0]), m=int(m_info[0]),
        #                                                     s=int(m_info[1]))
        #     elif pod_age > 3600 and pod_age < 86400:
        #         h_info = divmod(pod_age, 3600)
        #         m_info = divmod(h_info[1], 60)
        #         tmp_info['age'] = '{h}h{m}m{s}s'.format(h=int(h_info[0]), m=int(m_info[0]), s=int(m_info[1]))
        #     elif pod_age > 60 and pod_age < 3600:
        #         m_info = divmod(pod_age, 60)
        #         tmp_info['age'] = '{m}m{s}s'.format(m=int(m_info[0]), s=int(m_info[1]))
        #     else:
        #         tmp_info['age'] = '{s}s'.format(s=pod_age)
        #     tmp_info['owner_info'] = []
        #     if pod_info.metadata.owner_references is not None:
        #         for owner_reference in pod_info.metadata.owner_references:
        #             sub_tmp_info = dict()
        #             sub_tmp_info['kind'] = owner_reference.kind
        #             sub_tmp_info['name'] = owner_reference.name
        #
        #             tmp_info['owner_info'].append(sub_tmp_info)
        #     tmp_info['host_ip'] = pod_info.status.host_ip
        #     tmp_info['pod_ip'] = pod_info.status.pod_ip
        #     tmp_info['status'] = pod_info.status.phase
        #     tmp_info['node_name'] = pod_info.spec.node_name
        #     tmp_info['node_selector'] = pod_info.spec.node_selector
        #     tmp_info['volumes'] = []
        #     for volume_info in pod_info.spec.volumes:
        #         tmp_dict = dict()
        #         tmp_dict['name'] = volume_info.name
        #         if volume_info.persistent_volume_claim:
        #             tmp_dict['pvc_name'] = volume_info.persistent_volume_claim.claim_name
        #         else:
        #             tmp_dict['pvc_name'] = None
        #
        #         if volume_info.host_path:
        #             tmp_dict['host_path'] = volume_info.host_path.path
        #         else:
        #             tmp_dict['host_path'] = None
        #         tmp_info['volumes'].append(tmp_dict)
        #
        #     tmp_info['containers'] = []
        #     for container_info in pod_info.spec.containers:
        #         tmp_dict = dict()
        #         tmp_dict['name'] = container_info.name
        #         tmp_dict['image'] = container_info.image
        #         tmp_dict['volume_mount_info'] = []
        #         for volume_mount_info in container_info.volume_mounts:
        #             sub_tmp_dict = dict()
        #             sub_tmp_dict['name'] = volume_mount_info.name
        #             sub_tmp_dict['mount_path'] = volume_mount_info.mount_path
        #             tmp_dict['volume_mount_info'].append(sub_tmp_dict)
        #
        #         if pod_info.status.container_statuses is not None:
        #             for container_status in pod_info.status.container_statuses:
        #                 if container_info.name == container_status.name:
        #                     tmp_dict['ready'] = container_status.ready
        #                     tmp_dict['restarts'] = container_status.restart_count
        #
        #                     if container_status.container_id is not None:
        #                         tmp_dict['container_id'] = container_status.container_id.split('//')[-1]
        #                     else:
        #                         tmp_dict['container_id'] = container_status.container_id
        #         tmp_info['containers'].append(tmp_dict)
        #     pods_info.append(tmp_info)
        # return pods_info

    def get_deployments_info(self, label_selector=None):
        if label_selector:
            all_info = self.appsv1api.list_namespaced_deployment(
                namespace=self.namespace,
                label_selector=label_selector
            )
        else:
            all_info = self.appsv1api.list_namespaced_deployment(
                namespace=self.namespace
            )
        return all_info.to_dict()['items']
        # deployments_info = []
        # for deployment_info in all_info.items:
        #     tmp_info = dict()
        #     tmp_info['name'] = deployment_info.metadata.name
        #     tmp_info['replicas'] = deployment_info.spec.replicas
        #     tmp_info['ready'] = deployment_info.status.ready_replicas
        #     tmp_info['labels'] = deployment_info.metadata.labels
        #     tmp_info['container'] = []
        #     for container in deployment_info.spec.template.spec.containers:
        #         sub_tmp_info = dict()
        #         sub_tmp_info['name'] = container.name
        #         sub_tmp_info['image'] = container.image
        #         tmp_info['container'].append(sub_tmp_info)
        #     deployments_info.append(tmp_info)
        # return deployments_info

    def get_daemon_sets_info(self, label_selector=None):
        if label_selector:
            all_info = self.appsv1api.list_namespaced_daemon_set(
                namespace=self.namespace,
                label_selector=label_selector
            )
        else:
            all_info = self.appsv1api.list_namespaced_daemon_set(
                namespace=self.namespace
            )
        return all_info.to_dict()['items']
        # daemon_sets_info = []
        # for daemon_set_info in all_info.items:
        #     tmp_info = dict()
        #     tmp_info['name'] = daemon_set_info.metadata.name
        #     tmp_info['ready'] = daemon_set_info.status.number_ready
        #     tmp_info['available'] = daemon_set_info.status.number_available
        #     tmp_info['labels'] = daemon_set_info.metadata.labels
        #     tmp_info['container'] = []
        #     for container in daemon_set_info.spec.template.spec.containers:
        #         sub_tmp_info = dict()
        #         sub_tmp_info['name'] = container.name
        #         sub_tmp_info['image'] = container.image
        #         tmp_info['container'].append(sub_tmp_info)
        #
        #     daemon_sets_info.append(tmp_info)
        # return daemon_sets_info

    def get_stateful_sets_info(self, label_selector=None):
        if label_selector:
            all_info = self.appsv1api.list_namespaced_stateful_set(
                namespace=self.namespace,
                label_selector=label_selector
            )
        else:
            all_info = self.appsv1api.list_namespaced_stateful_set(
                namespace=self.namespace
            )
        return all_info.to_dict()['items']
        # stateful_sets_info = []
        # for stateful_set_info in all_info.items:
        #     tmp_info = dict()
        #     tmp_info['name'] = stateful_set_info.metadata.name
        #     tmp_info['service_name'] = stateful_set_info.spec.service_name
        #     tmp_info['replicas'] = stateful_set_info.spec.replicas
        #     tmp_info['ready'] = stateful_set_info.status.ready_replicas
        #     tmp_info['labels'] = stateful_set_info.metadata.labels
        #     tmp_info['container'] = []
        #     for container in stateful_set_info.spec.template.spec.containers:
        #         sub_tmp_info = dict()
        #         sub_tmp_info['name'] = container.name
        #         sub_tmp_info['image'] = container.image
        #         tmp_info['container'].append(sub_tmp_info)
        #     stateful_sets_info.append(tmp_info)
        # return stateful_sets_info

    def get_nodes_info(self, label_selector=None):
        if label_selector:
            all_info = self.corev1api.list_node(label_selector=label_selector)
        else:
            all_info = self.corev1api.list_node()
        return all_info.to_dict()['items']
        # nodes_info = []
        # for node_info in all_info.items:
        #     tmp_info = dict()
        #     tmp_info['name'] = node_info.metadata.name
        #     tmp_info['labels'] = node_info.metadata.labels
        #     tmp_info['ip'] = node_info.metadata.annotations['projectcalico.org/IPv4Address'].split('/')[0]
        #     for condition in node_info.status.conditions:
        #         if condition.type == 'Ready':
        #             tmp_info['status'] = condition.status
        #             break
        #
        #     tmp_info['images'] = []
        #     for image_info in node_info.status.images:
        #         for image_name in image_info.names:
        #             if '@sha256' not in image_name:
        #                 tmp_info['images'].append(image_name)
        #
        #     nodes_info.append(tmp_info)
        # return nodes_info

    def get_pvs_info(self):
        all_info = self.corev1api.list_persistent_volume()
        pvs_info = []
        for pv_info in all_info.items:
            tmp_info = {
                'name': pv_info.metadata.name,
                'access_modes': pv_info.spec.access_modes,
                'capacity': pv_info.spec.capacity['storage'],
                'claim_ref': pv_info.spec.claim_ref,
                'csi': pv_info.spec.csi,
                'persistent_volume_reclaim_policy': pv_info.spec.persistent_volume_reclaim_policy,
                'storage_class_name': pv_info.spec.storage_class_name,
                'volume_mode': pv_info.spec.volume_mode,
                'status': {
                    'message': pv_info.status.message,
                    'phase': pv_info.status.phase,
                    'reason': pv_info.status.reason
                }
            }

            if pv_info.spec.csi:
                tmp_info['csi'] = {
                    'driver': pv_info.spec.csi.driver,
                    'fs_type': pv_info.spec.csi.fs_type,
                    'volume_attributes': pv_info.spec.csi.volume_attributes
                }

                if 'policies' in tmp_info['csi']['volume_attributes']:
                    del tmp_info['csi']['volume_attributes']['policies']

            if pv_info.spec.claim_ref:
                tmp_info['claim_ref'] = {
                    'kind': pv_info.spec.claim_ref.kind,
                    'name': pv_info.spec.claim_ref.name,
                    'namespace': pv_info.spec.claim_ref.namespace
                }

            pvs_info.append(tmp_info)

        return pvs_info

    def get_pvcs_info(self, label_selector=None):
        if label_selector:
            all_info = self.corev1api.list_namespaced_persistent_volume_claim(namespace=self.namespace,
                                                                              label_selector=label_selector)
        else:
            all_info = self.corev1api.list_namespaced_persistent_volume_claim(namespace=self.namespace)

        pvcs_info = []
        for pvc_info in all_info.items:
            tmp_info = {
                'name': pvc_info.metadata.name,
                'labels': pvc_info.metadata.labels,
                'annotations': pvc_info.metadata.annotations,
                'volume_name': pvc_info.spec.volume_name,
                'volume_mode': pvc_info.spec.volume_mode,
                'storage_class_name': pvc_info.spec.storage_class_name
            }
            pvcs_info.append(tmp_info)

        return pvcs_info

    def get_services_info(self, label_selector=None):
        if label_selector:
            all_info = self.corev1api.list_service_for_all_namespaces(label_selector=label_selector)
        else:
            all_info = self.corev1api.list_service_for_all_namespaces()

        services_info = []
        for service_info in all_info.items:
            tmp_info = {}
            tmp_info['name'] = service_info.metadata.name
            tmp_info['type'] = service_info.spec.type
            tmp_info['cluster_ip'] = service_info.spec.cluster_ip
            tmp_info['external_ips'] = service_info.spec.external_i_ps
            tmp_info['ports'] = service_info.spec.ports
            tmp_info['ingress_ips'] = []
            if service_info.status.load_balancer.ingress is not None:
                for ingress_info in service_info.status.load_balancer.ingress:
                    tmp_info['ingress_ips'].append(ingress_info.ip)

            services_info.append(tmp_info)

        return services_info

    def get_secrets_info(self, label_selector=None):
        if label_selector:
            all_info = self.corev1api.list_namespaced_secret(namespace=self.namespace, label_selector=label_selector)
        else:
            all_info = self.corev1api.list_namespaced_secret(namespace=self.namespace)

        secrets_info = []
        for secret_info in all_info.items:
            tmp_info = {}
            tmp_info['name'] = secret_info.metadata.name
            if secret_info.data is not None:
                for key, value in secret_info.data.items():
                    tmp_info[key] = base64.b64decode(value).decode('UTF-8')

                secrets_info.append(tmp_info)

        return secrets_info

    def set_image_for_daemon_set(self, daemon_set_name, container_name, image):
        daemon_set_spec_template_spec_containers = [
            client.V1Container(
                name=container_name,
                image=image
            )
        ]

        daemon_set_spec_template_spec = client.V1PodSpec(
            containers=daemon_set_spec_template_spec_containers
        )

        daemon_set_spec_template = client.V1PodTemplateSpec(
            spec=daemon_set_spec_template_spec
        )

        daemon_set_spec = client.V1beta1DaemonSetSpec(
            template=daemon_set_spec_template
        )

        daemon_set = client.V1beta1DaemonSet(
            spec=daemon_set_spec
        )

        self.appsv1api.patch_namespaced_daemon_set(
            name=daemon_set_name,
            namespace=self.namespace,
            body=daemon_set
        )

    def set_image_for_deployment(self, deployment_name, container_name, image):
        deployment_spec_template_spec_containers = [
            client.V1Container(
                name=container_name,
                image=image
            )
        ]

        deployment_spec_template_spec = client.V1PodSpec(
            containers=deployment_spec_template_spec_containers
        )

        deployment_spec_template = client.V1PodTemplateSpec(
            spec=deployment_spec_template_spec
        )

        deployment_spec = client.AppsV1beta1DeploymentSpec(
            template=deployment_spec_template
        )

        deployment = client.ExtensionsV1beta1Deployment(
            spec=deployment_spec
        )

        self.appsv1api.patch_namespaced_deployment(
            name=deployment_name,
            namespace=self.namespace,
            body=deployment
        )

    def set_image_for_stateful_set(self, stateful_set_name, container_name, service_name, image):
        stateful_set_spec_template_spec_containers = [
            client.V1Container(
                name=container_name,
                image=image
            )
        ]

        stateful_set_spec_template_spec = client.V1PodSpec(
            containers=stateful_set_spec_template_spec_containers
        )

        stateful_set_spec_template = client.V1PodTemplateSpec(
            spec=stateful_set_spec_template_spec
        )

        stateful_set_spec = client.V1beta1StatefulSetSpec(
            template=stateful_set_spec_template,
            service_name=service_name
        )

        stateful_set = client.V1beta1StatefulSet(
            spec=stateful_set_spec
        )

        self.appsv1api.patch_namespaced_stateful_set(
            name=stateful_set_name,
            namespace=self.namespace,
            body=stateful_set
        )

    def set_replicas_for_deployment(self, name, replicas):
        self.appsv1api.patch_namespaced_deployment(
            name=name,
            namespace=self.namespace,
            body={
                "spec": {
                    "replicas": replicas
                }
            }
        )

    def set_replicas_for_stateful_set(self, name, replicas):
        self.appsv1api.patch_namespaced_stateful_set(
            name=name,
            namespace=self.namespace,
            body={
                "spec": {
                    "replicas": replicas
                }
            }
        )

    def delete_stateful_set(self, stateful_set_name):
        try:
            self.appsv1api.delete_namespaced_stateful_set(stateful_set_name, self.namespace,
                                                          body=client.V1DeleteOptions())
        except Exception as e:
            raise e

    def delete_pvc(self, pvc_name):
        try:
            self.corev1api.delete_namespaced_persistent_volume_claim(pvc_name, self.namespace,
                                                                     body=client.V1DeleteOptions())
        except Exception as e:
            raise e

    def delete_pv(self, pv_name):
        try:
            self.corev1api.delete_persistent_volume(pv_name, body=client.V1DeleteOptions())
        except Exception as e:
            raise e

    def delete_service(self, service_name):
        try:
            self.corev1api.delete_namespaced_service(service_name, self.namespace, body=client.V1DeleteOptions())
        except Exception as e:
            raise e

    def delete_pod(self, pod_name, grace_period_seconds=5184000):
        logger.debug('Delete pod {name}!'.format(name=pod_name))
        try:
            self.corev1api.delete_namespaced_pod(
                namespace=self.namespace,
                name=pod_name,
                grace_period_seconds=grace_period_seconds,
                body={}
            )
        except Exception as e:
            if 'Not Found' in str(e):
                logger.warning(e)
            else:
                raise e

    def set_service_type(self, service_name, service_type):
        try:
            self.corev1api.patch_namespaced_service(
                name=service_name,
                namespace=self.namespace,
                body={
                    "spec": {
                        "type": service_type
                    }
                }
            )
        except Exception as e:
            raise e

    def set_service_external_ips(self, service_name, external_ips):
        """
        edit a service external_ips, location as follow

        spec:
          clusterIP: 10.233.2.3
          externalIPs:
          - 10.25.119.69

        :param service_name:
        :param external_ips: a list of ips
        :return:
        """

        try:
            assert isinstance(external_ips, list)
            self.corev1api.patch_namespaced_service(
                name=service_name,
                namespace=self.namespace,
                body={
                    "spec": {
                        "externalIPs": external_ips
                    }
                }
            )
        except Exception as e:
            raise e

    def create_service(self, service_type, selector, service_name, port_list=None, external_ips=None, cluster_ip=None,
                       node_port=None):
        service_spec_clusterip = None
        service_spec_ports = None
        service_spec_externalips = None
        service_spec_external_traffic_policy = None
        service_spec_type = None
        service_spec_session_affinity = 'ClientIP'
        service_spec_selector = selector

        # Cluster ip
        if service_type == 'cluster_ip':
            service_spec_clusterip = cluster_ip
            if port_list is not None:
                service_spec_ports = [
                    client.V1ServicePort(
                        name='p{}'.format(port),
                        protocol='TCP',
                        port=port,
                        target_port=port
                    ) for port in port_list
                ]

        # External ip
        elif service_type == 'external_ip':
            service_spec_externalips = external_ips
            if port_list is not None:
                service_spec_ports = [
                    client.V1ServicePort(
                        name='p{}'.format(port),
                        protocol='TCP',
                        port=port,
                        target_port=port
                    ) for port in port_list
                ]

        # network 3 and 4 do NOT need service

        # Node port
        elif service_type == 'node_port':
            service_spec_clusterip = cluster_ip
            service_spec_external_traffic_policy = 'Cluster'
            if port_list is not None:
                service_spec_ports = [
                    client.V1ServicePort(
                        name='p{}'.format(port),
                        protocol='TCP',
                        port=port,
                        target_port=port,
                        node_port=node_port
                    ) for port in port_list
                ]
                service_spec_type = 'NodePort'

        service_spec = client.V1ServiceSpec(
            selector=service_spec_selector,
            ports=service_spec_ports,
            cluster_ip=service_spec_clusterip,
            external_i_ps=service_spec_externalips,
            external_traffic_policy=service_spec_external_traffic_policy,
            type=service_spec_type,
            session_affinity=service_spec_session_affinity
        )

        service_metadata = client.V1ObjectMeta(
            name=service_name
        )

        service = client.V1Service(
            metadata=service_metadata,
            spec=service_spec
        )

        try:
            self.corev1api.create_namespaced_service(
                namespace=self.namespace,
                body=service,
                pretty=True
            )
        except Exception as e:
            raise e

    def get_configmap_data_by_name(self, configmap_name):
        configmap = self.corev1api.read_namespaced_config_map(
            namespace=self.namespace,
            name=configmap_name
        )

        return configmap.data

    def update_configmap_data(self, name, data):
        self.corev1api.patch_namespaced_config_map(
            namespace=self.namespace,
            name=name,
            body={
                'data': data
            }
        )

    def run_cmd(self, cmd, pod_name, container_name=None, timeout=360):
        rtn_dict = dict()
        rtn_dict['stdout'] = ''
        rtn_dict['stderr'] = ''

        logger.debug('Run {cmd} on {pod_name}'.format(cmd=cmd, pod_name=pod_name))

        try:
            if container_name:
                resp = stream(self.corev1api.connect_get_namespaced_pod_exec, name=pod_name, namespace=self.namespace,
                              command=['/bin/sh'], container=container_name, stderr=True, stdin=True, stdout=True,
                              tty=False, _preload_content=False)
            else:
                resp = stream(self.corev1api.connect_get_namespaced_pod_exec, name=pod_name, namespace=self.namespace,
                              command=['/bin/sh'], stderr=True, stdin=True, stdout=True, tty=False,
                              _preload_content=False)

            while resp.is_open():
                resp.update(timeout=timeout)

                if resp.peek_stdout():
                    rtn_dict['stdout'] = resp.read_stdout().strip()
                if resp.peek_stderr():
                    rtn_dict['stderr'] = resp.read_stderr().strip()

                resp.write_stdin("{}\n ".format(cmd))
                break

            resp.close()

        except ApiException as e:
            raise e
        return rtn_dict

    def update_node_label(self, node_name, labels):
        logger.info('Update node {name} labels: {labels}'.format(name=node_name, labels=labels))
        self.corev1api.patch_node(
            node_name,
            {
                'metadata': {
                    'labels': labels
                }
            }
        )

    def disable_node_label(self, node_name, node_label):
        self.update_node_label(node_name, labels={node_label: 'false'})

    def enable_node_label(self, node_name, label_name):
        self.update_node_label(node_name, labels={label_name: 'true'})

    def get_secret_info_by_name(self, secret_name):
        for secret_info in self.get_secrets_info():
            if secret_info['name'] == secret_name:
                return secret_info
        else:
            raise Exception('Secret {name} is not exist!'.format(name=secret_name))

    def get_node_info_by_name(self, node_name, label_selector=None):
        for node_info in self.get_nodes_info(label_selector):
            if node_info['name'] == node_name:
                return node_info
        else:
            raise Exception('Node {name} is not exist!'.format(name=node_name))

    def get_pod_info_by_name(self, pod_name, label_selector=None):
        for pod_info in self.get_pods_info(label_selector):
            if pod_info['name'] == pod_name:
                return pod_info
        else:
            raise Exception('Pod {name} is not exist!'.format(name=pod_name))

    def get_pods_info_by_pvc(self, pvc_name, label_selector=None):
        pods_info = []
        for pod_info in self.get_pods_info(label_selector):
            for volume_info in pod_info['volumes']:
                if volume_info['pvc_name'] == pvc_name:
                    pods_info.append(pod_info)
                    break

        return pods_info

    @retry(tries=120, delay=5)
    def is_pod_ready_by_name(self, pod_name):
        try:
            pod_info = self.get_pod_info_by_name(pod_name)
        except Exception as e:
            raise e
        else:
            if pod_info['deletion_timestamp']:
                raise Exception('Pod {name} is terminating!'.format(name=pod_name))
            pod_name = pod_info['name']
            pod_host_ip = pod_info['host_ip']
            pod_status = pod_info['status']
            if pod_status != 'Running':
                raise Exception(
                    'Pod {name} is not running on {ip}, pod status is {status}, wait state change to running!'.format(
                        name=pod_name, ip=pod_host_ip, status=pod_status))
            else:
                for container_info in pod_info['containers']:
                    container_name = container_info['name']
                    if not container_info['ready']:
                        raise Exception(
                            'Container {c_name} is not ready on {p_name} pod and {ip}, wait change to ready!'.format(
                                c_name=container_name, p_name=pod_name, ip=pod_host_ip))
                logger.info('Pod {p_name} is ready on {ip}!'.format(p_name=pod_name, ip=pod_info['host_ip']))

    @retry(tries=120, delay=5)
    def is_pod_terminated_by_name(self, pod_name):
        try:
            pod_info = self.get_pod_info_by_name(pod_name)
        except Exception as e:
            logger.debug(e)
            logger.info('Pod had been terminated!')
        else:
            if pod_info['deletion_timestamp']:
                raise Exception('Pod {name} is terminating!'.format(name=pod_name))


if __name__ == '__main__':
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IkkySTI6VTcySjpXQVdDOjdMRVE6QkhaMzpKNUdSOkFSQ1I6Q0UyTTpSQktXOlkzQUM6QUpVUTpTV0tSIn0=.eyJpc3MiOiJ2ZW51cy10b2tlbi1pc3N1ZXIiLCJzdWIiOiJhZG1pbiIsImF1ZCI6WyIiXSwiZXhwIjoiMjAyMS0wOC0yN1QyN1QwODowODo0MyIsIm5vbmNlIjoiU0FBd09uRU14dTJSRHViWiIsImlkIjoxLCJ1c2VybmFtZSI6ImFkbWluIn0=.IySzlMVaxJOcImGxGjpONzhMs68rNyCasQ6KVnaHxctBpnsxQszbRoAZ7F_jWNobGDB_5yFhX7v45IIT-FSvDFl01w4x5Df1Teir1Ai2K_QnlBp4mna7iT6lyJKXHPJ-TxK6wpmkgoCUtGZVpM5L1DW3D5NsQ4duCn6c6FQx134='
    kubernetes_obj = KubernetesObj('https://192.168.1.236:6443', secret=token)
    print(kubernetes_obj.get_pods_info())
