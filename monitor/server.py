# -*- coding: utf-8 -*-1

import sys
import os
work_dir = os.path.join(os.getcwd().split('ghostcloudtest')[0], 'ghostcloudtest')
sys.path.append(work_dir)
from flask import Flask, render_template, request
from utils.util import get_localhost_ip
from flask.json import jsonify
from libs.log_obj import LogObj
from libs.mysql_obj import MysqlObj
from settings.global_settings import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD


logger = LogObj().get_logger()
app = Flask(__name__)

# global var define
c_time_list = []
ping_time_list = []
query_time_list = []
performance_infos = []
performance_items = []
mysql_obj = MysqlObj(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD)


def get_envs(project_name):
    sql_cmd = 'show databases'
    rows = mysql_obj.run_sql_cmd(sql_cmd)
    if project_name == 'socket':
        project_name = 'newben'
    return [row['Database'] for row in rows if project_name in row['Database']]


def get_performance_info_names(db):
    sql_cmd = 'use {0}'.format(db)
    mysql_obj.run_sql_cmd(sql_cmd)
    sql_cmd = 'show tables'
    rows = mysql_obj.run_sql_cmd(sql_cmd)
    return [row['Tables_in_{0}'.format(db)] for row in rows]


def get_performance_items(db, table_name):
    sql_cmd = 'use {0}'.format(db)
    mysql_obj.run_sql_cmd(sql_cmd)
    sql_cmd = 'desc {0}'.format(table_name)
    rows = mysql_obj.run_sql_cmd(sql_cmd)
    return [row['Field'] for row in rows]


def get_performance_infos(db, table_name):
    sql_cmd = 'select * from {0}.{1}'.format(db, table_name)
    rows = mysql_obj.run_sql_cmd(sql_cmd)
    return rows


def get_cmd_results(db):
    sql_cmd = 'use {0}'.format(db)
    mysql_obj.run_sql_cmd(sql_cmd)
    sql_cmd = 'show tables'
    rows = mysql_obj.run_sql_cmd(sql_cmd)
    return [row['Tables_in_{0}'.format(db)] for row in rows if 'cmd_result' in row['Tables_in_{0}'.format(db)]]


def get_ping_times_info(db, table_name):
    c_time_list = []
    ping_time_list = []
    query_time_list = []

    get_socket_server_cmd = 'select * from {0}.{1}'.format(db, table_name)
    rows = mysql_obj.run_sql_cmd(get_socket_server_cmd)
    for row in rows:
        if row['rc'] == 0:
            try:
                tmp_list = row['stdout'].split('\n')
                for tmp_str in tmp_list:
                    if 'Query time' in tmp_str:
                        query_time = tmp_str.split()[3].strip()
                        query_time_list.append(float(query_time))
                        break
                ping_time = tmp_list[-1].split('=')[-1].split('/')[1]
                ping_time_list.append(float(ping_time))
                c_time_list.append(row['c_time'])
            except Exception:
                logger.error(row)
    return ping_time_list, query_time_list, c_time_list


@app.route("/", methods=["GET"])
def main():
    return render_template("main.html")


@app.route("/<project_name>", methods=["GET"])
def project(project_name):
    envs = get_envs(project_name)
    return render_template("envs.html", project_name=project_name, envs=envs)


@app.route("/<project_name>/<env_name>", methods=["GET"])
def performance_infos(project_name, env_name):
    performance_info_names = get_performance_info_names(env_name)
    return render_template("performance_infos.html", project_name=project_name, env_name=env_name,
                           performance_info_names=performance_info_names)


@app.route("/<project_name>/<env_name>/<performance_info_name>/performance", methods=["GET"])
def performance(project_name, env_name, performance_info_name):
    global c_time_list

    if project_name == 'socket':
        global ping_time_list
        global query_time_list

        ping_time_list, query_time_list, c_time_list = get_ping_times_info(env_name, performance_info_name)
        return render_template("network_time.html", project_name=project_name, env_name=env_name,
                               performance_info_name=performance_info_name)
    else:
        global performance_infos
        global performance_items

        performance_infos = get_performance_infos(env_name, performance_info_name)
        performance_items = get_performance_items(env_name, performance_info_name)
        performance_items.remove('c_time')
        for performance_info in performance_infos:
            c_time_list.append(performance_info['c_time'])
        return render_template("performance.html", project_name=project_name, env_name=env_name,
                               performance_info_name=performance_info_name, performance_items=performance_items,
                               performance_infos=performance_infos, c_time_list=c_time_list)


@app.route("/<project_name>/<env_name>/<performance_info_name>/performance/update", methods=["GET", "POST"])
def performance_update(project_name, env_name, performance_info_name):
    global c_time_list

    data = dict()
    data['c_time_list'] = c_time_list
    if project_name == 'socket':
        global ping_time_list
        global query_time_list
        data['ping_time_list'] = ping_time_list
        data['query_time_list'] = query_time_list
    else:
        global performance_infos
        global performance_items
        data['performance_infos'] = performance_infos
        data['performance_items'] = performance_items
    return jsonify(data)


if __name__ == '__main__':
    app.run(host=get_localhost_ip(), port=5000)