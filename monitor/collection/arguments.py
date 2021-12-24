import argparse
from common.arguments import framework_parser


def parse_arg():
    """Init all the command line arguments."""
    parser = argparse.ArgumentParser(description='monitor', parents=[framework_parser()])
    parser.add_argument("--interval", action="store", dest="interval", default=10, type=int, help="interval time:1")
    args = parser.parse_args()
    return args
