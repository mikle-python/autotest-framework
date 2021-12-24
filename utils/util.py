#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import traceback
import subprocess
import time
import re
import random
import string
import datetime
import socket
import json
import pytz
import zipfile
import uuid
import decimal
import six
from progressbar import ProgressBar, Percentage, Bar, RotatingMarker, ETA
from libs.log_obj import LogObj
from settings.global_settings import PRIMITIVE_TYPES, WINDOWS


logger = LogObj().get_logger()


def run_cmd(cmd, timeout=None):
    """
    create a sub process and run commands --subprocess
    :param cmd:
    :return:(dict) cmd return info
    """

    logger.debug('Subprocess.check_output: {cmd}'.format(cmd=cmd))
    rtn_dict = dict()
    rtn_dict['rc'] = 0
    rtn_dict['stdout'] = None
    rtn_dict['stderr'] = None
    try:
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True, timeout=timeout)
        rtn_dict['stdout'] = result.decode('UTF-8', "ignore")
    except subprocess.CalledProcessError as error:
        rtn_dict['stderr'] = error.output.decode('UTF-8', "ignore")
        rtn_dict['rc'] = error.returncode
    except Exception as e:
        logger.error('Exception occurred: {err}'.format(err=traceback.format_exc()))
        rtn_dict['rc'] = -1
        rtn_dict['stderr'] = str(e)

    return rtn_dict


def invert_dict_key_value(dict_data):
    """
    invert the dict: key <==> value
    :param dict_data:
    :return:(dict) new_dict_data
    """

    rtn_dict = {}
    for k, v in dict_data.items():
        rtn_dict[v] = k
    return rtn_dict


def hostname():
    cmd = 'hostname'
    rtn_dict = run_cmd(cmd)
    return rtn_dict['stdout'].strip()


def ip_to_num(ip):
    """
    convert ip(ipv4) address to a int num
    :param ip:
    :return: int num
    """

    lp = [int(x) for x in ip.split('.')]
    return lp[0] << 24 | lp[1] << 16 | lp[2] << 8 | lp[3]


def num_to_ip(num):
    """
    convert int num to ip(ipv4) address
    :param num:
    :return:
    """

    ip = ['', '', '', '']
    ip[3] = (num & 0xff)
    ip[2] = (num & 0xff00) >> 8
    ip[1] = (num & 0xff0000) >> 16
    ip[0] = (num & 0xff000000) >> 24
    return '%s.%s.%s.%s' % (ip[0], ip[1], ip[2], ip[3])


def generate_string(length):
    base_string = string.ascii_letters + string.digits
    base_string_len = len(base_string)
    multiple = 1
    if base_string_len < length:
        multiple = (length // base_string_len) + 1

    return ''.join(random.sample(base_string * multiple, length))


def generate_random_int(max_size, min_size=3):
    try:
        return random.randint(min_size, max_size)
    except Exception as e:
        print("Not supporting {0} as valid sizes!".format(max_size))
        raise e


# Generate a random string with length of 1 to provided param
def generate_random_string(max_size, min_size=3):
    return ''.join(random.choice(string.ascii_letters + string.digits)
                   for _ in range(generate_random_int(max_size, min_size=min_size)))


def generate_random_lower_string(max_size):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(generate_random_int(max_size)))


def strsize_to_size(str_size):
    """
    convert str_size such as 1K,1M,1G,1T to size 1024 (byte)
    :param str_size:such as 1K,1M,1G,1T
    :return:size (byte)
    """

    str_size = str(str_size) if not isinstance(str_size, str) else str_size

    if not bool(re.search('[a-z_A-Z]', str_size)):
        return int(str_size)

    if not bool(re.search('[0-9]', str_size)):
        raise Exception('Not support string size: {}'.format(str_size))

    regx = re.compile(r'(\d+)\s*([a-z_A-Z]+)', re.I)
    tmp_size_unit = regx.findall(str_size)[0]
    tmp_size = int(tmp_size_unit[0])
    tmp_unit = tmp_size_unit[1]
    if bool(re.search('K', tmp_unit, re.IGNORECASE)):
        size_byte = tmp_size * 1024
    elif bool(re.search('M', tmp_unit, re.IGNORECASE)):
        size_byte = tmp_size * 1024 * 1024
    elif bool(re.search('G', tmp_unit, re.IGNORECASE)):
        size_byte = tmp_size * 1024 * 1024 * 1024
    elif bool(re.search('T', tmp_unit, re.IGNORECASE)):
        size_byte = tmp_size * 1024 * 1024 * 1024 * 1024
    else:
        raise Exception("Error string size, just support KB/MB/GB/TB (IGNORECASE)")

    return size_byte


def str_to_datetime(st, fmt="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.strptime(st, fmt)


def datetime_to_str(dt, fmt="%Y-%m-%d %H:%M:%S"):
    return dt.strftime(fmt)


def convert_timezone(dtime, tz=pytz.timezone('Asia/Shanghai')):
    return dtime.astimezone(tz=tz)


def time_str():
    return datetime_to_str(datetime.datetime.now(), fmt='%Y-%m-%d-%H-%M-%S')


def get_localhost_ip():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(('8.8.8.8', 80))
        ip = sock.getsockname()[0]
    finally:
        sock.close()
    return ip


def file_to_zip(source_dir, zip_file):
    file_obj = open(zip_file, 'w')
    file_obj.close()
    with zipfile.ZipFile(zip_file, "w") as zipfile_obj:
        for parent, dir_names, file_names in os.walk(source_dir):
            for file_name in file_names:
                zipfile_obj.write(os.path.join(parent, file_name))


def dd(if_path, of_path, bs, count, skip=None, seek=None, oflag=None):
    """
    dd read write
    :param if_path: read path
    :param of_path: write path
    :param bs:
    :param count:
    :param skip: read offset
    :param seek: write offset
    :param oflag: eg: direct
    :param timeout: run_cmd timeout second
    :return:
    """

    dd_cmd = "{tool} if={if_path} of={of_path} bs={bs} count={count}".format(tool=DD, if_path=if_path, of_path=of_path,
                                                                             bs=bs, count=count)
    if oflag:
        dd_cmd = "{cmd} oflag={oflag}".format(cmd=dd_cmd, oflag=oflag)
    if skip:
        dd_cmd = "{cmd} skip={skip}".format(cmd=dd_cmd, skip=skip)
    if seek:
        dd_cmd = "{cmd} seek={seek}".format(cmd=dd_cmd, seek=seek)

    rtn_dict = run_cmd(dd_cmd)

    if rtn_dict['rc'] != 0:
        logger.error(rtn_dict)
        raise Exception('dd fail!')


def txt_w(file_path_name, file_size, line_size=128, mode='w+'):
    """
    create original file, each line with line_number, and specified line size
    :param path_name:
    :param total_size:
    :param line_size:
    :param mode: w+ / a+
    :return:
    """

    logger.info('Create file: {name}'.format(name=file_path_name))
    original_path = os.path.split(file_path_name)[0]
    if not os.path.isdir(original_path):
        try:
            os.makedirs(original_path)
        except OSError as e:
            raise Exception(e)

    line_count = file_size // line_size
    unaligned_size = file_size % line_size
    try:
        with open(file_path_name, mode) as f:
            for line_num in range(line_count):
                random_sting = '{str}\n'.format(str=generate_string(line_size - 2 - len(str(line_num))))
                f.write('{line_num}:{random_s}'.format(line_num=line_num, random_s=random_sting))
            if unaligned_size > 0:
                f.write(generate_string(unaligned_size))
            f.flush()
            os.fsync(f.fileno())

    except Exception as e:
        logger.error('Create file {name} fail, file size is {size}!'.format(name=file_path_name, size=file_size))
        raise e


def dd_w(file_path_name, file_size):
    if WINDOWS:
        if_path = '/dev/random'
    else:
        if_path = '/dev/urandom'

    block_size_list = ['512', '1k', '4k', '16k', '64k', '512k', '1M']
    bs = random.choice(block_size_list)
    bs_size = strsize_to_size(bs)
    if file_size < 1024 * 1024:
        count = 1
        bs_size = file_size
    else:
        count = file_size // bs_size

    dd(if_path, file_path_name, bs_size, count)


class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return datetime_to_str(obj)
        else:
            return json.JSONEncoder.default(self, obj)


def generate_doc():
    doc = {
        "doc_c_time": int(time.time() * 1000),
        "doc_i_time": int(time.time() * 1000),
        "gc_id": str(uuid.uuid4()),
        "is_file": True,
        "is_folder": False,
        "path": random.choice(["", "/", "/dir", "/dir" + "{}".format(random.randint(1, 100))]),
        "size": random.randint(1, 1000000),
        "uid": random.randint(0, 10),
        "gid": random.randint(0, 10),
        "ctime": int(time.time() * 1000),
        "mtime": int(time.time() * 1000),
        "atime": int(time.time() * 1000),
        "last_used_time": int(time.time() * 1000),
        "app_id": str(uuid.uuid4()),
        "app_name": generate_random_string(10),
        "file_id": str(random.randint(11111111111111111111111111111111, 99999911111111111111111111111111))
    }

    return doc


def generate_docs(docs_num):
    for _ in range(docs_num):
        yield generate_doc()


def get_file_md5(file_path_name):
    if WINDOWS:
        md5_cmd = 'certutil -hashfile {file} md5'.format(file=file_path_name)
    else:
        md5_cmd = 'md5sum {file}'.format(file=file_path_name)

    rtn_dict = run_cmd(md5_cmd)
    if rtn_dict['rc'] == 0:
        if WINDOWS:
            md5_value = rtn_dict['stdout'].strip().split('\r\n')[1]
        else:
            md5_value = rtn_dict['stdout'].split(' ')[0].split('\\')[-1]

        md5_info = {}
        file_name = os.path.basename(file_path_name)
        md5_info[file_name] = md5_value
        return md5_info
    else:
        logger.error(rtn_dict)
        raise Exception('Get {name} exception occured!'.format(name=file_path_name))


def sanitize_for_serialization(obj):
    if obj is None:
        return None

    elif isinstance(obj, PRIMITIVE_TYPES):
        return obj

    elif isinstance(obj, decimal.Decimal):
        return obj

    elif isinstance(obj, list):
        return [sanitize_for_serialization(sub_obj) for sub_obj in obj]

    elif isinstance(obj, tuple):
        return tuple(sanitize_for_serialization(sub_obj) for sub_obj in obj)

    elif isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()

    elif isinstance(obj, dict):
        obj_dict = obj

    else:
        obj_dict = {obj.attribute_map[attr]: getattr(obj, attr) for attr, _ in six.iteritems(obj.openapi_types)
                    if getattr(obj, attr) is not None}

    return {key: sanitize_for_serialization(val) for key, val in six.iteritems(obj_dict)}


if __name__ == '__main__':
    print(time_str())
