import argparse


suite_file_parser = argparse.ArgumentParser(add_help=False)
suite_file_parser.add_argument("--suite_file", required=True, action="store", dest="suite_file", default=None,
                               help="suite_file, default:None")

power_options_parser = argparse.ArgumentParser(add_help=False)
power_options_parser.add_argument("--power_options", action="store", dest="power_options",
                                  default=['poweroff', 'reboot', 'shutdown', 'reset', 'suspend'], nargs='+',
                                  help="power_options, default:['poweroff', 'reboot', 'shutdown', 'reset', 'suspend']")


def framework_parser():
    framework_parser = argparse.ArgumentParser(add_help=False)
    framework_group = framework_parser.add_argument_group('framework args')
    framework_group.add_argument("--show_case", action="store_true", dest="show_case", default=False,
                                 help="show cases")
    framework_group.add_argument("--iteration", action="store", dest="iteration", default=1, type=int,
                            help="run iteration:1")
    framework_group.add_argument("--cases", action="store", dest="cases", default=[], nargs='+',
                              help="cases, default:None")
    framework_group.add_argument("--collect", action="store_true", dest="collect", default=False,
                                help="collect log")
    framework_group.add_argument("--performance", action="store_true", dest="performance", default=False,
                                 help="collect performance result")
    framework_group.add_argument("--concurrent", action="store", dest="concurrent", default=1, type=int,
                            help="concurrent:1")
    framework_group.add_argument("--min", action="store", dest="min", default=1, type=int, help="min:1")
    framework_group.add_argument("--max", action="store", dest="max", default=0, type=int, help="max:0")
    framework_group.add_argument("--platform", action="store", dest="platform", default="vmware", help="default:vmware")
    framework_group.add_argument("--log_dir", action="store", dest="log_dir", default=None, help="default:None")
    return framework_parser


def auth_parser():
    auth_parser = argparse.ArgumentParser(add_help=False)
    auth_group = auth_parser.add_argument_group('SSH auth info args')
    auth_group.add_argument("--ip", action="store", dest="ip", default=None, help="default:None")
    auth_group.add_argument("--sys_user", action="store", dest="sys_user", default="root", help="default:root")
    auth_group.add_argument("--sys_pwd", action="store", dest="sys_pwd", default="password",
                                help="default:password")
    auth_group.add_argument("--sys_port", action="store", dest="sys_port", default=22, type=int, help="default: 22")
    auth_group.add_argument("--key_file", action="store", dest="key_file", default=None, help="pem key file path")
    return auth_parser


def vc_parser():
    vc_parser = argparse.ArgumentParser(add_help=False)
    vc_group = vc_parser.add_argument_group('vCenter auth info args')
    vc_group.add_argument("--vc_ip", action="store", dest="vc_ip", default=None, help="default:None")
    vc_group.add_argument("--vc_user", action="store", dest="vc_user", default="administrator@vsphere.local",
                          help="default:administrator@vsphere.local")
    vc_group.add_argument("--vc_pwd", action="store", dest="vc_pwd", default="P@ssw0rd", help="default:P@ssw0rd")
    vc_group.add_argument("--vc_port", action="store", dest="vc_port", default=443, type=int, help="default: 443")
    return vc_parser


def mysql_parser():
    mysql_parser = argparse.ArgumentParser(add_help=False)
    mysql_group = mysql_parser.add_argument_group('mysql auth info args')
    mysql_group.add_argument("--mysql_ip", action="store", dest="mysql_ip", default="192.168.5.7",
                             help="default: 192.168.5.7")
    mysql_group.add_argument("--mysql_user", action="store", dest="mysql_user", default="root", help="default: root")
    mysql_group.add_argument("--mysql_pwd", action="store", dest="mysql_pwd", default="password",
                             help="default:P@ssw0rd")
    mysql_group.add_argument("--mysql_port", action="store", dest="mysql_port", default=3306, type=int,
                             help="default: 3306")
    return mysql_parser


def hwcloud_parser():
    hwcloud_parser = argparse.ArgumentParser(add_help=False)
    hwcloud_group = hwcloud_parser.add_argument_group('Huawei cloud auth info args')
    hwcloud_group.add_argument("--ak", action="store", dest="ak", default="MKWRFCYCEPAMR35AASLJ",
                               help="default:MKWRFCYCEPAMR35AASLJ")
    hwcloud_group.add_argument("--sk", action="store", dest="sk", default="lQxJyKsiSKPLpxJUbAFi3A7H1UHKCL94d7Xd4ZBY",
                               help="default:lQxJyKsiSKPLpxJUbAFi3A7H1UHKCL94d7Xd4ZBY")
    hwcloud_group.add_argument("--region", action="store", dest="region", default=None, help="default:None")
    return hwcloud_parser