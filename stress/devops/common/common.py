import json
import time
from libs.log_obj import LogObj
from utils.decorator import retry
logger = LogObj().get_logger()


def run_time(func):
    def wrapper_func(*args, **kwargs):
        logger.debug('Enter {name}.'.format(name=func.__name__))
        start_time = int(time.time()*1000)
        func(*args, **kwargs)
        end_time = int(time.time()*1000)
        take_time = end_time-start_time
        logger.debug('Exit from {0}, take time: {1} ms'.format(func.__name__, take_time))
        return take_time
    return wrapper_func


def build_pipeline(request_obj, pipeline_data, pipeline_header, build_pipeline_url):
    build_pipeline_response = request_obj.call('post', build_pipeline_url, data=json.dumps(pipeline_data),
                                               headers=pipeline_header).json()

    if build_pipeline_response['code'] == "200" and build_pipeline_response['message'] == "success":
        logger.info("Build pipeline by api <{}> done !".format(build_pipeline_url))
    else:
        raise Exception("Build pipeline by <{}> failed, the error messages are [{}]".format(build_pipeline_url,
                                                                                            build_pipeline_response))


@retry(30, 10)
def is_pipeline_build_success(mysql_obj, pipeline_id, build_pipeline_time):
    sql_cmd = "select result,startTime from devops.pipeline_build_record where pipeline_id={} and startTime>{}"\
        .format(pipeline_id, build_pipeline_time)
    results = mysql_obj.run_sql_cmd(sql_cmd)
    if results:
        for result in results:
            if result['result'] != "SUCCESS":
                raise Exception("Build pipeline failed, the pipeline_id is <{}> .".format(pipeline_id))
        else:
            logger.info("Build pipeline successfully that id is <{}>".format(pipeline_id))
    else:
        raise Exception("No build pipeline record found in current time .")


def create_api(request_obj, data, header, url, description=None):
    if description is None:
        pass
    else:
        logger.info("The data description is  <{}> !".format(description))
    response = request_obj.call('post', url, data=json.dumps(data), headers=header)
    try:
        response_json = response.json()
    except Exception as e:
        if "Expecting value: line 1 column 1 (char 0)" in str(e):
            logger.warning("The response: {}".format(response.content.decode()))
            logger.warning("The data happened error: {}".format(data))
            raise e

    if response_json['code'] == "200" and response_json['message'] == "success":
        logger.info("Use the <{}> done !".format(url))
        return response.elapsed.total_seconds()
    else:
        raise Exception("Use the <{}> failed, the error messages are [{}]".format(url, response_json))


def list_api(request_obj, header, url, description=None):
    if description is None:
        pass
    else:
        logger.info("List api description is  <{}> !".format(description))

    response = request_obj.call('get', url, headers=header)
    try:
        response_json = response.json()
    except Exception as e:
        if "Expecting value: line 1 column 1 (char 0)" in str(e):
            logger.warning("The response: {}".format(response.content.decode()))
            raise e

    if response_json['code'] == "200" and response_json['message'] == "success":
        logger.info("List by <{}> done !".format(url))
        return response.elapsed.total_seconds()
    else:
        raise Exception("List by <{}> failed, the error messages are [{}]".format(url, response_json))


def update_api(request_obj, data, header, url, description=None):
    if description is None:
        pass
    else:
        logger.info("The data description is  <{}> !".format(description))

    response = request_obj.call('put', url, data=json.dumps(data), headers=header)

    try:
        response_json = response.json()
    except Exception as e:
        if "Expecting value: line 1 column 1 (char 0)" in str(e):
            logger.warning(response.content.decode())
            raise e

    if response_json['code'] == "200" and response_json['message'] == "success":
        logger.info("Use the <{}> done !".format(url))
        return response.elapsed.total_seconds()
    else:
        raise Exception("Use the <{}> failed, the error messages are [{}]".format(url, response_json))


def delete_api(request_obj, header, url, data=None, description=None):
    if description is None:
        pass
    else:
        logger.info("The data description is  <{}> !".format(description))
    if data:
        response = request_obj.call('delete', url, headers=header, data=json.dumps(data))
    else:
        response = request_obj.call('delete', url, headers=header)
    try:
        response_json = response.json()
    except Exception as e:
        if "Expecting value: line 1 column 1 (char 0)" in str(e):
            logger.warning("The response: {}".format(response.content.decode()))
            logger.warning("The url happened error: {}".format(url))
            raise e

    if response_json['code'] == "200" and response_json['message'] == "success":
        logger.info("Use the <{}> done !".format(url))
        return response.elapsed.total_seconds()
    else:
        raise Exception("Use the <{}> failed, the error messages are [{}]".format(url, response_json))


def login_token(request_obj, username, password, login_url):
    login_data = {
        "username": username,
        "password": password,
        "provider": "DEVOPS"
    }
    login_headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                      "Chrome/96.0.4664.45 Safari/537.36"
    }
    login_response = request_obj.call('post', login_url, data=json.dumps(login_data), headers=login_headers).json()
    if login_response['code'] == "200" and login_response['message'] == "success":
        logger.info("Login api server {} successfully !".format(login_url))
        return login_response['data']['token']
    else:
        raise Exception("Login api server {} failed, the error messages are [{}]".
                        format(login_url, login_response))


def all_member_name_id(mysql_obj):
    all_members_name_id = {}
    for member in mysql_obj.run_sql_cmd("select username,id from devops.user"):
        all_members_name_id[member['username']] = member['id']
    return all_members_name_id


def all_pipeline_name_id(mysql_obj):
    all_pipelines_name_id = {}
    for pipeline in mysql_obj.run_sql_cmd("select name,id from devops.pipeline"):
        all_pipelines_name_id[pipeline['name']] = pipeline['id']
    return all_pipelines_name_id


def all_pipeline_names(mysql_obj):
    all_pipelines_names = []
    for pipeline in mysql_obj.run_sql_cmd("select name from devops.pipeline"):
        all_pipelines_names.append(pipeline['name'])
    return all_pipelines_names


def all_pipeline_build_record(mysql_obj):
    all_pipelines_build_record = []
    for pipeline in mysql_obj.run_sql_cmd("select name,startTime from devops.pipeline"):
        all_pipelines_build_record.append(pipeline['name'])
    return all_pipelines_build_record


def all_project_user(mysql_obj):
    all_project_users = {}
    for result in mysql_obj.run_sql_cmd("select project_id, user_id from devops.project_user"):
        if result['project_id'] not in all_project_users.keys():
            all_project_users[result['project_id']] = [result['user_id']]
        else:
            all_project_users[result['project_id']].append(result['user_id'])

    return all_project_users


def all_issue_name_id(mysql_obj):
    all_issues = {}
    for issue in mysql_obj.run_sql_cmd("select id,title from devops.issue"):
        all_issues[issue['title']] = issue['id']
    return all_issues


def all_case_name_id(mysql_obj):
    all_cases = {}
    for case in mysql_obj.run_sql_cmd("select id,title,creator_id from devops.test_case"):
        all_cases[case['title']] = {'id': case['id'], 'creator_id': case['creator_id']}
    return all_cases


def all_user_id_real_name(mysql_obj):
    all_users = {}
    for user in mysql_obj.run_sql_cmd("select id,name from devops.user"):
        all_users[user['id']] = user['name']
    return all_users
