import argparse
from common.arguments import suite_file_parser, framework_parser, auth_parser


def web_auth_parser():
    web_auth_parser = argparse.ArgumentParser(add_help=False)
    web_auth_group = web_auth_parser.add_argument_group('Web auth info args')
    web_auth_group.add_argument("--ip", action="store", dest="ip", default=None, help="default:None")
    web_auth_group.add_argument("--user", action="store", dest="user", default="admin", help="default:admin")
    web_auth_group.add_argument("--password", action="store", dest="password", default="adminP@ssw0rd",
                                help="default:adminP@ssw0rd")
    return web_auth_parser


def parse_arg():
    """Init all the command line arguments."""
    parser = argparse.ArgumentParser(description='interface')
    subparsers = parser.add_subparsers()

    sub_parser = subparsers.add_parser('devops', parents=[suite_file_parser, framework_parser(), auth_parser()],
                                       help='args.')
    sub_parser.set_defaults(action='devops')

    sub_parser = subparsers.add_parser('newben', parents=[suite_file_parser, framework_parser(), auth_parser()],
                                       help='args.')
    sub_parser.set_defaults(action='newben')

    args = parser.parse_args()
    return args
