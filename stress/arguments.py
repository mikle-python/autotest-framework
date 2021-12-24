import argparse
from common.arguments import framework_parser, auth_parser, vc_parser, mysql_parser, hwcloud_parser, \
    power_options_parser


def newben_parser():
    newben_parser = argparse.ArgumentParser(add_help=False)
    newben_group = newben_parser.add_argument_group('newben platform args')
    newben_group.add_argument("--workspace", action="store", dest="workspace", default="system", help="default:system")
    newben_group.add_argument("--single", action="store_true", dest="single", default=False, help="single node")
    newben_group.add_argument("--not_delete", action="store_true", dest="not_delete", default=False,
                              help="not delete node")
    newben_group.add_argument("--image", action="store", dest="image", default=None, help="default:None")
    newben_group.add_argument("--worker", action="store", dest="worker", default=None, help="default:None")
    newben_group.add_argument("--ippool", action="store", dest="ippool", default="seam-cni", help="default:seam-cni")
    newben_group.add_argument("--replicas", action="store", dest="replicas", default=1, type=int, help="replicas:1")
    newben_group.add_argument("--app_cpu", action="store", dest="app_cpu", default=100, type=int, help="app cpu: 100")
    newben_group.add_argument("--app_memory", action="store", dest="app_memory", default=100, type=int,
                              help="app_memory: 100M")
    newben_group.add_argument("--all_services", action="store_true", dest="all_services", default=False,
                              help="all services")
    newben_group.add_argument("--all_nodes", action="store_true", dest="all_nodes", default=False, help="all nodes")
    newben_group.add_argument("--network_limit", action="store_true", dest="network_limit", default=False,
                              help="network_limit")
    newben_group.add_argument("--ceph_monitor_ip", action="store", dest="ceph_monitor_ip", default=None,
                              help="default:ceph_monitor_ip")
    newben_group.add_argument("--ceph_nodes_ip", action="store", dest="ceph_nodes_ip", default=[], nargs='+',
                              help="ceph_nodes_ip")
    return newben_parser


def redis_parser():
    redis_parser = argparse.ArgumentParser(add_help=False)
    redis_group = redis_parser.add_argument_group('redis auth info args')
    redis_group.add_argument("--redis_ip", action="store", dest="redis_ip", default=None, help="default:None")
    redis_group.add_argument("--redis_port", action="store", dest="redis_port", default='6379',
                          help="default: 6379")
    redis_group.add_argument("--redis_pwd", action="store", dest="redis_pwd", default="password",
                             help="default:password")

    redis_group.add_argument("--redis_data_quantity", action="store", dest="redis_data_quantity", default=100000,
                             type=int, help="default:100000 data")
    return redis_parser


def kafka_parser():
    kafka_parser = argparse.ArgumentParser(add_help=False)
    kafka_group = kafka_parser.add_argument_group('kafka auth info args')
    kafka_group.add_argument("--brokers", action="store", dest="brokers", default=None,
                             help="default:None set like ip:port and you can set multiple server,"
                                  "you can use <,> to separate,like ip1:port1,ip2:port2")
    kafka_group.add_argument("--client_quantity", action="store", dest="client_quantity", default=1, type=int,
                             help="default: 1")
    kafka_group.add_argument("--group_id", action="store", dest="group_id", default="test_kafka_group",
                             help="default: test_kafka_group")
    kafka_group.add_argument("--topic", action="store", dest="topic", default="test_kafka",
                             help="default: test_kafka")
    kafka_group.add_argument("--topic_quantity", action="store", dest="topic_quantity", default=1000, type=int,
                             help="default: 1000")
    kafka_group.add_argument("--message_quantity", action="store", dest="message_quantity", default=10000,
                             type=int, help="default:10000 data")
    kafka_group.add_argument("--message_min_size", action="store", dest="message_min_size", default=10240,
                             type=int, help="default:10240 bit")
    kafka_group.add_argument("--message_max_size", action="store", dest="message_max_size", default=102400,
                             type=int, help="default:102400 bit")
    kafka_group.add_argument("--mode", action="store", dest="mode", default='producer',
                            help="default: producer, if use consumer mode ,set it consumer ")
    return kafka_parser


def es_parser():
    es_parser = argparse.ArgumentParser(add_help=False)
    es_group = es_parser.add_argument_group('es auth info args')
    es_group.set_defaults(action='es')
    es_group.add_argument("--es_ips", action="store", dest="es_ips", default=[], nargs='+',
                          help="es ip list, default:None")
    es_group.add_argument("--es_port", action="store", dest="es_port", default=None, type=int,
                          help="es port,default:None")
    es_group.add_argument("--es_user", action="store", dest="es_user", default="root", help="default:root")
    es_group.add_argument("--es_pwd", action="store", dest="es_pwd", default="password", help="default:password")
    es_group.add_argument("--docs_num", action="store", dest="docs_num", default=100000, type=int,
                          help="documents number,default:100000")
    es_group.add_argument("--indices_num", action="store", dest="indices_num", default=50, type=int,
                          help="indices number,default:50")
    es_group.add_argument("--max_bulk_size", action="store", dest="max_bulk_size", default=1000, type=int,
                          help="max_bulk_size,default:1000")
    es_group.add_argument("--index_name", action="store", dest="index_name", default="gc_index",
                          help="base index name, default: gc_index")

    return es_parser


def nacos_parser():
    nacos_parser = argparse.ArgumentParser(add_help=False)
    nacos_group = nacos_parser.add_argument_group('nacos auth info args')
    nacos_group.add_argument("--server_address", action="store", dest="server_address", default=None,
                             help="default:None")
    nacos_group.add_argument("--namespace", action="store", dest="namespace", default='',
                          help="default:''")
    nacos_group.add_argument("--username", action="store", dest="username", default="nacos",
                             help="default:nacos")
    nacos_group.add_argument("--password", action="store", dest="password", default="nacos",
                             help="default:nacos")
    nacos_group.add_argument("--config_quantity", action="store", dest="config_quantity", default=1000,
                             type=int, help="default:1000 configs")
    nacos_group.add_argument("--instance_quantity", action="store", dest="instance_quantity", default=1000,
                             type=int, help="default:1000 instances")

    return nacos_parser


def minio_parser():
    minio_parser = argparse.ArgumentParser(add_help=False)
    minio_group = minio_parser.add_argument_group('minio auth info args')
    minio_group.add_argument("--end_point", action="store", dest="end_point", default=None, help="default:None")
    minio_group.add_argument("--access_key", action="store", dest="access_key", default='useruser',
                             help="default: useruser")
    minio_group.add_argument("--secret_key", action="store", dest="secret_key", default='password',
                             help="default: password")
    minio_group.add_argument("--secure", action="store", dest="secure", default=False, help="default: False")
    minio_group.add_argument("--bucket_name", action="store", dest="bucket_name", default='gc-minio-test',
                             help="default: gc-minio-test")
    minio_group.add_argument("--file_upload_path", action="store", dest="file_upload_path",
                             default='/home/gc_upload_test', help="default: /home/gc_upload_test")
    minio_group.add_argument("--file_download_path", action="store", dest="file_download_path",
                             default='/home/gc_download_test', help="default: /home/gc_download_test")
    minio_group.add_argument("--min_size", action="store", dest="min_size", default=1, type=int, help="default: 1")
    minio_group.add_argument("--max_size", action="store", dest="max_size", default=1024, type=int,
                             help="default: 1024")
    minio_group.add_argument("--minio_files_quantity", action="store", dest="minio_files_quantity", default=10000,
                             type=int, help="default:10000 files")
    return minio_parser


def zookeeper_parser():
    zookeeper_parser = argparse.ArgumentParser(add_help=False)
    zookeeper_group = zookeeper_parser.add_argument_group('zookeeper auth info args')
    zookeeper_group.add_argument("--zk_hosts", action="store", dest="zk_hosts", default=None, help="default:None")
    zookeeper_group.add_argument("--zk_path_name", action="store", dest="zk_path_name", default='/gc_zk_test',
                                 help="default: /gc_zk_test")
    zookeeper_group.add_argument("--max_node_value", action="store", dest="max_node_value", default=1024, type=int,
                                 help="default: 1024")
    zookeeper_group.add_argument("--min_node_value", action="store", dest="min_node_value", default=1, type=int,
                                 help="default: 1")
    zookeeper_group.add_argument("--node_quantity", action="store", dest="node_quantity", default=1000, type=int,
                                 help="default: 1000")
    return zookeeper_parser


def parse_arg():
    """Init all the command line arguments."""
    parser = argparse.ArgumentParser(description='stress')
    subparsers = parser.add_subparsers()
    sub_parser = subparsers.add_parser('newben', parents=[framework_parser(), auth_parser(), vc_parser(),
                                                          newben_parser(), mysql_parser(), power_options_parser],
                                       help='args.')
    sub_parser.set_defaults(action='newben')
    sub_parser.add_argument("--app_type", action="store", dest="app_type", default="nginx", help="default:nginx")
    sub_parser.add_argument("--share_storage_vms", action="store", dest="share_storage_vms", default=[], nargs='+',
                              help="share_storage_vms, default:None")
    sub_parser.add_argument("--add_nodes_ip", action="store", dest="add_nodes_ip", default=[], nargs='+',
                            help="add_nodes_ip, default:[]")
    sub_parser.add_argument("--app_command", action="store", dest="app_command", default=None,
                            help="app_command, default:None")
    sub_parser.add_argument("--box", action="store", dest="box", default=None, help="default:None")
    sub_parser.add_argument("--mission_type", action="store", dest="mission_type", default="tensorflow",
                            help="default:tensorflow")
    sub_parser.add_argument("--train_code_path", action="store", dest="train_code_path",
                            default="3/test-not-delete/tf-s", help="default: 3/test-not-delete/tf-s")
    sub_parser.add_argument("--train_data_path", action="store", dest="train_data_path", default="3/datasets/mnist",
                            help="default: 3/datasets/mnist")
    sub_parser.add_argument("--train_output_path", action="store", dest="train_output_path", default="3/output/",
                            help="default: 3/output/")
    sub_parser.add_argument("--job_time", action="store", dest="job_time", default=None, type=int, help="job_time")
    sub_parser.add_argument("--api_server", action="store", dest="api_server", default=None,
                            help="api_server, like -> http://127.0.0.1:28080")
    sub_parser.add_argument("--ai_api_username", action="store", dest="ai_api_username", default="admin",
                            help="ai_api_username, default is admin")
    sub_parser.add_argument("--ai_api_password", action="store", dest="ai_api_password", default="password",
                            help="ai_api_password, default is password")
    sub_parser.add_argument("--train_mission_command", action="store", dest="train_mission_command",
                            default="python===mnist.py", help="train_mission_command, default: python===mnist.py, "
                                                              "use'===' to separate arguments")
    sub_parser.add_argument("--min_wait", action="store", dest="min_wait", default=1, type=int,
                            help="min_wait, default is 1")
    sub_parser.add_argument("--max_wait", action="store", dest="max_wait", default=10, type=int,
                            help="min_wait, default is 10")
    sub_parser.add_argument("--gpu_quantity", action="store", dest="gpu_quantity", default=4, type=int,
                            help="gpu_quantity, default is 4")
    sub_parser.add_argument("--kind", action="store", dest="kind", default=None, help="default:None")
    sub_parser.add_argument("--cmds", action="store", dest="cmds", default=[], nargs='+', help="cmds, default:None")

    sub_parser = subparsers.add_parser('ecos', parents=[framework_parser(), auth_parser(), vc_parser(),
                                                        hwcloud_parser(), redis_parser(), kafka_parser(), es_parser(),
                                                        nacos_parser(), minio_parser(), zookeeper_parser()],
                                       help='args.')
    sub_parser.set_defaults(action='ecos')
    sub_parser.add_argument("--power_master", action="store_true", dest="power_master", default=False,
                            help="collect log")
    sub_parser.add_argument("--reboot_components", action="store_true", dest="reboot_components",
                            default="mysql,redis,nacos,minio,kafka,zookeeper",
                            help="Default are [mysql,redis,nacos,minio,kafka,zookeeper], "
                                 "you can specific the component to reboot, multiple components use ',' to separate")

    sub_parser = subparsers.add_parser('devops', parents=[framework_parser(), auth_parser()], help='args.')
    sub_parser.set_defaults(action='devops')

    args = parser.parse_args()
    return args