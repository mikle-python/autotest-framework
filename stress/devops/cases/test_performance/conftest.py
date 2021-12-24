from concurrent.futures import ThreadPoolExecutor, as_completed
import pytest
from prettytable import PrettyTable

from libs.log_obj import LogObj
from stress.devops.common.common import all_pipeline_names, create_api, all_member_name_id, all_project_user, update_api
from utils.util import time_str

logger = LogObj().get_logger()


@pytest.fixture(scope='session')
def application_create_table():
    return 'application_create'


@pytest.fixture(scope='session')
def pipeline_data_lists(devops_test_data, header_after_login):
    pipeline_data_lists = []

    create_pipeline_url = devops_test_data['common']['api_server'] + \
                          devops_test_data['performance']['pipeline']['path']['create_pipeline']

    for i in range(devops_test_data['performance']['pipeline']['pipeline_quantity']):
        pipeline_data = devops_test_data['performance']['pipeline']['data_create_pipeline'].copy()
        pipeline_data['name'] = "{}-{}".format(devops_test_data['performance']['pipeline']['pipeline_name'], i)
        pipeline_data_lists.append({'pipeline_data': pipeline_data, 'pipeline_header': header_after_login,
                                    'create_pipeline_url': create_pipeline_url})
    return pipeline_data_lists


@pytest.fixture(scope='function')
def pipeline_names_from_mysql(mysql_obj):
    return all_pipeline_names(mysql_obj)


@pytest.fixture(scope='session')
def pipeline_create(request_obj, mysql_obj, pipeline_data_lists):
    pipeline_names = all_pipeline_names(mysql_obj)
    pool_create = ThreadPoolExecutor(max_workers=50)
    futures_create = []
    for pipeline_data_list in pipeline_data_lists:
        if pipeline_data_list['pipeline_data']['name'] not in pipeline_names:
            futures_create.append(pool_create.submit(create_api, request_obj,
                                                     pipeline_data_list['pipeline_data'],
                                                     pipeline_data_list['pipeline_header'],
                                                     pipeline_data_list['create_pipeline_url']))
        else:
            logger.info("Pipeline <{}> already exist, not create it again".
                        format(pipeline_data_list['pipeline_data']['name']))
    pool_create.shutdown()
    for future in as_completed(futures_create):
        future.result()


@pytest.fixture(scope='session')
def check_table():
    return PrettyTable(['API', 'ResponseTime(s)'])


@pytest.fixture(scope='session')
def plan_name():
    return "autotest"


@pytest.fixture(scope='session')
def pipeline_with_platform_data_lists(devops_test_data, header_after_login):
    pipeline_with_platform_data_lists = []
    create_pipeline_url = devops_test_data['common']['api_server'] + \
                          devops_test_data['performance']['pipeline']['path']['create_pipeline']

    for i in range(devops_test_data['performance']['work_platform']['build_note']['build_quantity']):
        pipeline_data = devops_test_data['performance']['pipeline']['data_create_pipeline_demo'].copy()
        pipeline_data['name'] = "{}-{}-{}".format(devops_test_data['performance']['pipeline']['pipeline_name'],
                                                  'build-note', i)
        pipeline_with_platform_data_lists.append({'pipeline_data': pipeline_data, 'pipeline_header': header_after_login,
                                                  'create_pipeline_url': create_pipeline_url})
    return pipeline_with_platform_data_lists


@pytest.fixture(scope='function')
def member_of_project(devops_test_data):
    member_of_project = []
    for i in range(devops_test_data['performance']['work_platform']['project']['project_user']['user_quantity']):
        request_data = {
            "username": "autotest-{}-{}".format(time_str(), i),
            "realName": "autotest-{}-{}".format(time_str(), i),
            "password": devops_test_data['performance']['work_platform']['project']['project_user']['password'],
            "confirm": devops_test_data['performance']['work_platform']['project']['project_user']['password']
        }
        member_of_project.append(request_data)
    return member_of_project


@pytest.fixture(scope='session')
def register_user(devops_test_data, request_obj, mysql_obj, auth_token):
    pool_create = ThreadPoolExecutor(max_workers=20)
    future_create = []
    all_users = all_member_name_id(mysql_obj)
    user_info = devops_test_data['performance']['multiple_users']
    devops_test_data['common']['header_after_login']['Authorization'] = auth_token

    for i in range(user_info['user_quantity']):
        request_data = {
            "username": "autotest-{}".format(i),
            "realName": "autotest-{}".format(i),
            "password": user_info['password'],
            "confirm": user_info['password']
        }
        header_register = devops_test_data['common']['header_without_login'].copy()
        header_register['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
                                        "(KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
        if request_data['username'] not in all_users.keys():
            future_create.append(pool_create.submit(create_api, request_obj, request_data,
                                                    header_register,
                                                    devops_test_data['common']['api_server'] +
                                                    user_info['path']['user_register'],
                                                    "Register user "))
        else:
            logger.info("User <{}> has exist, not register again .".format(request_data['username']))
    pool_create.shutdown()
    for future in as_completed(future_create):
        future.result()

    user_with_ids = []
    all_users = all_member_name_id(mysql_obj)
    all_project_users = all_project_user(mysql_obj)
    pool_add = ThreadPoolExecutor(max_workers=10)
    future_add = []
    for i in range(user_info['user_quantity']):
        user_with_ids.append({"autotest-{}".format(i): all_users["autotest-{}".format(i)]})
        if all_users["autotest-{}".format(i)] not in all_project_users[devops_test_data['common']['projectId']]:
            data = {
                "projectId": devops_test_data['common']['projectId'],
                "userId": all_users["autotest-{}".format(i)],
                "roleIds": user_info['project']['member_role']
            }
            add_member_to_project_url = devops_test_data['common']['api_server'] + user_info['path']['add_project_user']
            update_header = devops_test_data['common']['header_after_login'].copy()
            update_header['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
                                          "(KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
            future_add.append(pool_add.submit(update_api, request_obj, data,
                                              update_header,
                                              add_member_to_project_url))
        else:
            logger.info("The user <{}> is member of project_id <{}>, not add it again"
                        .format("autotest-{}".format(i), devops_test_data['common']['projectId']))
    pool_add.shutdown()
    for future in as_completed(future_add):
        future.result()

    return user_with_ids


@pytest.fixture(scope='session')
def multiple_user_table():
    return PrettyTable(['ApiType', 'ResponseTime(ms)'])


@pytest.fixture(scope='session')
def db(devops_test_data):
    server_ip = devops_test_data['common']['api_server_ip']
    return '{}_devops'.format(server_ip.replace('.', '_'))


@pytest.fixture(scope='session', autouse=True)
def create_db(mysql_show_obj, db):
    create_db = 'create database if not exists {0}'.format(db)
    mysql_show_obj.run_sql_cmd(create_db)


@pytest.fixture(scope='session')
def create_api_table():
    return 'create_api'


@pytest.fixture(scope='session')
def list_api_table():
    return 'list_api'


@pytest.fixture(scope='session')
def pipeline_table():
    return 'pipeline'


@pytest.fixture(scope='session')
def assist_job_dashboard_wait_plan_table():
    return 'assist_job_dashboard_wait_plan'


@pytest.fixture(scope='session')
def assist_current_iteration_swim_line_table():
    return 'assist_current_iteration_swim_line'


@pytest.fixture(scope='session')
def case_library_case_table():
    return 'case_library_case'


@pytest.fixture(scope='session')
def test_plan_with_case_table():
    return 'test_plan_with_case'


@pytest.fixture(scope='session')
def test_plan_without_case_table():
    return 'test_plan_without_case'


@pytest.fixture(scope='session')
def test_team_setting_table():
    return 'test_team_setting'


@pytest.fixture(scope='session')
def role_setting_table():
    return 'role_setting'


@pytest.fixture(scope='session')
def work_platform_build_note_table():
    return 'work_platform_build_note'


@pytest.fixture(scope='session')
def work_platform_remain_issue_table():
    return 'work_platform_remain_issue'


@pytest.fixture(scope='session')
def work_platform_project_table():
    return 'work_platform_project'


@pytest.fixture(scope='session')
def work_platform_member_project_table():
    return 'work_platform_member_project'


@pytest.fixture(scope='session')
def assist_multiple_user_table():
    return 'assist_multiple_user'


@pytest.fixture(scope='session')
def cases_multiple_user_table():
    return 'cases_multiple_user'


@pytest.fixture(scope='session')
def create_create_api_table(mysql_show_obj, db, create_api_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, create_api_table)
    mysql_show_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_list_api_table(mysql_show_obj, db, list_api_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, list_api_table)
    mysql_show_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_pipeline_table(mysql_show_obj, db, pipeline_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, pipeline_table)
    mysql_show_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_assist_job_dashboard_wait_plan_table(mysql_show_obj, db, assist_job_dashboard_wait_plan_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, assist_job_dashboard_wait_plan_table)
    mysql_show_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_assist_current_iteration_swim_line_table(mysql_show_obj, db, assist_current_iteration_swim_line_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, assist_current_iteration_swim_line_table)
    mysql_show_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_case_library_case_table(mysql_show_obj, db, case_library_case_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, case_library_case_table)
    mysql_show_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_test_plan_with_case_table(mysql_show_obj, db, test_plan_with_case_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, test_plan_with_case_table)
    mysql_show_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_test_plan_without_case_table(mysql_show_obj, db, test_plan_without_case_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, test_plan_without_case_table)
    mysql_show_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_test_team_setting_table(mysql_show_obj, db, test_team_setting_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, test_team_setting_table)
    mysql_show_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_role_setting_table(mysql_show_obj, db, role_setting_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, role_setting_table)
    mysql_show_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_work_platform_build_note_table(mysql_show_obj, db, work_platform_build_note_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, work_platform_build_note_table)
    mysql_show_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_work_platform_remain_issue_table(mysql_show_obj, db, work_platform_remain_issue_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, work_platform_remain_issue_table)
    mysql_show_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_work_platform_project_table(mysql_show_obj, db, work_platform_project_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, work_platform_project_table)
    mysql_show_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_work_platform_member_project_table(mysql_show_obj, db, work_platform_member_project_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, work_platform_member_project_table)
    mysql_show_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_assist_multiple_user_table(mysql_show_obj, db, assist_multiple_user_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, assist_multiple_user_table)
    mysql_show_obj.run_sql_cmd(create_table)


@pytest.fixture(scope='session')
def create_cases_multiple_user_table(mysql_show_obj, db, cases_multiple_user_table):
    create_table = """create table if not exists {0}.{1} (
                api VARCHAR(255), 
                take_time double,
                c_time DATETIME)""".format(db, cases_multiple_user_table)
    mysql_show_obj.run_sql_cmd(create_table)
