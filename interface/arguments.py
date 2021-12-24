import argparse
from common.arguments import framework_parser, suite_file_parser, auth_parser


data_file_parser = argparse.ArgumentParser(add_help=False)
data_file_parser.add_argument("--data_file", required=True, action="store", dest="data_file", default=None,
                              help="data_file, default:None")


def parse_arg():
    """Init all the command line arguments."""
    parser = argparse.ArgumentParser(description='interface')
    subparsers = parser.add_subparsers()

    sub_parser = subparsers.add_parser('cli', parents=[data_file_parser, suite_file_parser, framework_parser(),
                                                       auth_parser()],
                                       help='args.')
    sub_parser.set_defaults(action='cli')

    sub_parser = subparsers.add_parser('api', parents=[data_file_parser, suite_file_parser, framework_parser(),
                                                       auth_parser()],
                                       help='args.')
    sub_parser.set_defaults(action='api')

    sub_parser = subparsers.add_parser('tool', parents=[data_file_parser, framework_parser()], help='args.')
    sub_parser.set_defaults(action='tool')

    args = parser.parse_args()

    return args