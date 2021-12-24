# Components process
BOOTSTRAP_PROCESS = '/nb-bootstrap'
CORESERVER_PROCESS = '/nb-coreserver'
AGENT_PROCESS = '/nb-agent'
DOCKER_NAI_PROCESS = '/docker-nai'
PROXY_PROCESS = '/proxy'
SEAM_PROCESS = '/seam'
WEB_PROCESS = '/nb-web'
RQLITE_PROCESS = 'rqlited'
LOG_PROCESS = '/nb-log'
ETCD_PROCESS = 'etcd'

NB_PROCESSES = [
    BOOTSTRAP_PROCESS,
    CORESERVER_PROCESS,
    AGENT_PROCESS,
    DOCKER_NAI_PROCESS,
    PROXY_PROCESS,
    SEAM_PROCESS,
    WEB_PROCESS,
    LOG_PROCESS,
    ETCD_PROCESS
]

COLLECT_CORE_DUMP_PROCESSED = [BOOTSTRAP_PROCESS, CORESERVER_PROCESS, AGENT_PROCESS]


# Components docker name
BOOTSTRAP_DOCKER = 'nb-bootstrap'
CORESERVER_DOCKER = 'nb-coreserver'
AGENT_DOCKER = 'nb-agent'
DOCKER_NAI_DOCKER = 'docker-nai'
PROXY_DOCKER = 'nb-proxy'
SEAM_DOCKER = 'nb-seam'
WEB_DOCKER = 'nb-web'
RQLITE_DOCKER = 'rqlite'
LOG_DOCKER = 'nb-log'
ETCD_DOCKER = 'etcd'

NB_DOCKERS = [
    BOOTSTRAP_DOCKER, CORESERVER_DOCKER, AGENT_DOCKER, DOCKER_NAI_DOCKER,
    PROXY_DOCKER, SEAM_DOCKER, WEB_DOCKER, LOG_DOCKER
]

MISSION_YAML_PATH = '/root/lc/mission_yaml/'
APP_YAML_PATH = '/root/lc/app_yaml/'
APPMATRIX_YAML_PATH = '/root/lc/appmatrix_yaml/'
APPARAFILE_YAML_PATH = '/root/lc/apparafile_yaml/'
FORWARD_YAML_PATH = '/root/lc/forward_yaml/'
INSTALL_YAML_PATH = '/root/lc/install_yaml/'
INSTALL_PATH = '/root/install/'

# Database
NB_DB = "newben"
NB_APP_TABLE = "app"