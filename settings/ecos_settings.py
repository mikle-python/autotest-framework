import random
import string
import time
import uuid

# COMPONENTS NAME
DEPLOYMENTS = ['calico-kube-controllers', 'coredns', 'metrics-server', 'openebs-admission-server',
                 'openebs-apiserver', 'openebs-localpv-provisioner', 'openebs-ndm-operator', 'openebs-provisioner',
                 'openebs-snapshot-operator', 'tiller-deploy', 'alertmanager', 'es-exporter', 'es-ingest', 'grafana',
                 'kube-state-metrics', 'venus-kibana', 'venus-mysql', 'venus-os-package', 'venus-ecos-service-manage',
                 'venus-ecos-ui', 'venus-package-manager', 'venus-plugin-app', 'venus-plugin-auth-center',
                 'venus-plugin-configrator',
                 'venus-plugin-ingress', 'venus-plugin-license', 'venus-plugin-logging', 'venus-plugin-market',
                 'venus-plugin-monitor', 'venus-plugin-namespace', 'venus-plugin-node', 'venus-plugin-node-manage',
                 'venus-plugin-registry-manager', 'venus-plugin-user-center', 'venus-plugin-volume-manager',
                 'venus-plugin-web', 'venus-registry', 'venus-repository-server']
STATEFULSETS = ['es-data', 'es-master', 'prometheus']
DAEMONSETS = ['prometheus-node-exporter', 'venus-filebeat', 'calico-node', 'kube-proxy', 'openebs-ndm']
PAAS_COMPONENTS = ['mysql', 'redis', 'nacos', 'minio', 'kafka', 'zookeeper']

ECOS_COMPONENTS = DEPLOYMENTS + STATEFULSETS + DAEMONSETS
ALL_COMPONENTS = ECOS_COMPONENTS + PAAS_COMPONENTS

# ECOS PLATFORM，COMPONENTS PROCESS
CALICO_KUBE_CONTROLLERS = 'kube-controllers'
COREDNS = 'coredns'
METRICS_SERVER = 'metrics-server'
OPENEBS_ADMISSION_SERVER = 'admission-server'
OPENEBS_APISERVER = 'openebs-apiserver'
OPENEBS_LOCALPV_PROVISIONER = 'provisioner-localpv'
OPENEBS_NDM_OPERATOR = 'ndo'
OPENEBS_PROVISIONER = 'openebs-provisioner'
OPENEBS_SNAPSHOT_OPERATOR = 'snapshot-'
TILLER_DEPLOY = 'tiller'
ALERTMANAGER = '/etc/alertmanager'
ES_EXPORTER = 'elasticsearch_exporter'
ES_INGEST = 'es-ingest'
GRAFANA = 'grafana'
KUBE_STATE_METRICS = 'kube-state-metrics'
VENUS_KIBANA = '/usr/share/kibana/bin/'
VENUS_MYSQL = 'mysqld'
VENUS_OS_PACKAGE = 'httpd'
VENUS_PAAS_SERVICE_MANAGE = 'venus-ecos-service-manage'
VENUS_PAAS_UI = 'nginx'
VENUS_PACKAGE_MANAGER = 'venus-package-manager'
VENUS_PLUGIN_APP = 'venus-plugin-app'
VENUS_PLUGIN_AUTH_CENTER = 'venus-plugin-auth-center'
VENUS_PLUGIN_CONFIGRATOR = 'venus-plugin-configrator'
VENUS_PLUGIN_INGRESS = 'venus-plugin-ingress'
VENUS_PLUGIN_LICENSE = 'venus-plugin-license'
VENUS_PLUGIN_LOGGING = 'venus-plugin-logging'
VENUS_PLUGIN_MARKET = 'venus-plugin-market'
VENUS_PLUGIN_MONITOR = 'venus-plugin-monitor'
VENUS_PLUGIN_NAMESPACE = 'venus-plugin-namespace'
VENUS_PLUGIN_NODE = 'venus-plugin-node'
VENUS_PLUGIN_NODE_MANAGE = 'venus-plugin-node-manage'
VENUS_PLUGIN_REGISTRY_MANAGER = 'venus-plugin-registry-manager'
VENUS_PLUGIN_USER_CENTER = 'venus-plugin-user-center'
VENUS_PLUGIN_VOLUME_MANAGER = 'venus-plugin-volume-manager'
VENUS_PLUGIN_WEB = 'nginx'  # 是否需要使用另外一种方法
VENUS_REGISTRY = "'registry serve'"
VENUS_REPOSITORY_SERVER = 'venus-package-server'
ES = 'elasticsearch'  # 是否需要使用另外一种方法
PROMETHEUS = 'prometheus'
PROMETHEUS_NODE_EXPORTER = 'node_exporter'
VENUS_FILEBEAT = 'filebeat'
CALICO_NODE = 'runsv'
KUBE_PROXY = 'kube-proxy'
OPENEBS_NDM = '/usr/sbin/ndm'

ECOS_PROCESSES = [CALICO_KUBE_CONTROLLERS, COREDNS, METRICS_SERVER, OPENEBS_ADMISSION_SERVER, OPENEBS_APISERVER,
                  OPENEBS_LOCALPV_PROVISIONER, OPENEBS_NDM_OPERATOR, OPENEBS_PROVISIONER, OPENEBS_SNAPSHOT_OPERATOR,
                  TILLER_DEPLOY, ALERTMANAGER, ES_EXPORTER, ES_INGEST, GRAFANA, KUBE_STATE_METRICS, VENUS_KIBANA,
                  VENUS_MYSQL, VENUS_OS_PACKAGE, VENUS_PAAS_SERVICE_MANAGE, VENUS_PAAS_UI, VENUS_PACKAGE_MANAGER,
                  VENUS_PLUGIN_APP, VENUS_PLUGIN_AUTH_CENTER, VENUS_PLUGIN_CONFIGRATOR, VENUS_PLUGIN_INGRESS,
                  VENUS_PLUGIN_LICENSE, VENUS_PLUGIN_LOGGING, VENUS_PLUGIN_MARKET, VENUS_PLUGIN_MONITOR,
                  VENUS_PLUGIN_NAMESPACE, VENUS_PLUGIN_NODE, VENUS_PLUGIN_NODE_MANAGE, VENUS_PLUGIN_REGISTRY_MANAGER,
                  VENUS_PLUGIN_USER_CENTER, VENUS_PLUGIN_VOLUME_MANAGER, VENUS_PLUGIN_WEB, VENUS_REGISTRY,
                  VENUS_REPOSITORY_SERVER, ES, PROMETHEUS, PROMETHEUS_NODE_EXPORTER, VENUS_FILEBEAT,
                  CALICO_NODE, KUBE_PROXY, OPENEBS_NDM]

# PAAS PLATFORM, COMPONENTS PROCESS
PAAS_REDIS = "redis"
PAAS_MYSQL = 'mysqld'
PAAS_NACOS = 'nacos'
PAAS_MINIO = 'minio'
PAAS_KAFKA = 'kafka'
PAAS_ZOOKEEPER = 'zookeeper'

PAAS_PROCESSES = [PAAS_REDIS, PAAS_MYSQL, PAAS_NACOS, PAAS_MINIO, PAAS_KAFKA, PAAS_ZOOKEEPER]

# ALL PROCESSES
ALL_PROCESSES = ECOS_PROCESSES + PAAS_PROCESSES

# ETCD COMMAND
ETCDCTL = 'etcdctl_v3'

# REDIS DATA TEMPLATE


def generate_random_int(max_size, min_size=3):
    try:
        return random.randint(min_size, max_size)
    except Exception as e:
        print("Not supporting {0} as valid sizes!".format(max_size))
        raise e


def generate_random_string(max_size, minsize=3):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(generate_random_int(max_size, min_size=minsize)))


def generate_doc():

    doc = {
        "doc_c_time": int(time.time() * 1000),
        "id": str(uuid.uuid4()),
        "GCname": generate_random_string(15),
        "tenant": generate_random_string(5),
        "name": '{0}.{1}'.format(generate_random_string(10), generate_random_string(3)),
        "name_term": '{0}.{1}'.format(generate_random_string(10), generate_random_string(3)),
        "last_used_time": int(time.time() * 1000),
        "uid": random.randint(0,10),
        "denied": [],
        "app_id": str(uuid.uuid4()),
        "app_name": generate_random_string(10),
        "gid": random.randint(0, 10),
        "doc_i_time": int(time.time() * 1000),
    }

    return doc


# ES_settings
Settings = {
    "index.mapping.total_fields.limit": "10000",
    "index.refresh_interval": "5s",
    "index.number_of_shards": "1",
    "index.max_docvalue_fields_search": "200",
    "index.number_of_replicas": "1"
}

Mappings = {
	"properties": {
		"doc_c_time": {
			"type": "keyword"
		},
		"doc_i_time": {
			"type": "keyword"
		},
		"gc_id": {
			"type": "keyword"
		},
		"is_file": {
			"type": "boolean"
		},
		"is_folder": {
			"type": "boolean"
		},
		"path": {
			"type": "keyword"
		},
		"size": {
			"type": "long"
		},
		"uid": {
			"type": "keyword"
		},
		"gid": {
			"type": "keyword"
		},
		"ctime": {
			"type": "date",
			"format": "epoch_second"
		},
		"mtime": {
			"type": "date",
			"format": "epoch_second"
		},
		"atime": {
			"type": "date",
			"format": "epoch_second"
		},
		"last_used_time": {
			"type": "date",
			"format": "epoch_second"
		},
		"app_id": {
			"type": "keyword"
		},
		"app_name": {
			"type": "keyword"
		},
		"file_id": {
			"type": "keyword"
		}
}
}

gc_index_settings = {"settings": Settings, "mappings": Mappings}

