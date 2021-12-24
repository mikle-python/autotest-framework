# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import six


# Platform
POSIX = os.name == "posix"
WINDOWS = os.name == "nt"
LINUX = sys.platform.startswith("linux")
MACOS = sys.platform.startswith("darwin")
FREEBSD = sys.platform.startswith("freebsd")
OPENBSD = sys.platform.startswith("openbsd")
NETBSD = sys.platform.startswith("netbsd")
BSD = FREEBSD or OPENBSD or NETBSD
SUNOS = sys.platform.startswith(("sunos", "solaris"))
AIX = sys.platform.startswith("aix")

# Python version
PYTHON_MAJOR_VERSION = sys.version_info.major

# Mysql Settings
MYSQL_HOST = '192.168.5.7'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'password'

# Binarys
ETCDCTL = 'etcdctl'
TEMP_ETCDCTL = '/tmp/etcdctl'


REMOTE_REGISTRY = 'registry.ghostcloud.cn'
LOCAL_REGISTRY = 'registry.cluster.local'
PROJECT_PATH = os.path.join(os.getcwd().split('ghostcloudtest')[0], 'ghostcloudtest/')
LOCAL_TEMP_PATH = os.path.join(PROJECT_PATH, 'tmp/')

# DB Settings
SOCKET_DB = 'socket'
SOCKET_SERVER_TABLE = 'socket_server'

# Socket Settings
SOCKET_SERVER_PORT = 50007


PRIMITIVE_TYPES = (float, bool, bytes, six.text_type) + six.integer_types