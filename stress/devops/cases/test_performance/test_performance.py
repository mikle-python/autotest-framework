import random
import pytest
import time
from datetime import datetime
from libs.log_obj import LogObj
from utils.util import time_str
from concurrent.futures import ThreadPoolExecutor, as_completed
from stress.devops.common.common import is_pipeline_build_success, build_pipeline, create_api, \
    list_api, update_api, all_member_name_id, all_pipeline_name_id, all_pipeline_names, login_token, \
    all_issue_name_id, delete_api, all_case_name_id, all_user_id_real_name

logger = LogObj().get_logger()


@pytest.mark.usefixtures("create_pipeline_table")
def test_pipeline(request_obj, mysql_obj, devops_test_data, pipeline_data_lists, header_after_login, db,
                  pipeline_table, mysql_show_obj):
    test_pipeline.__doc__ = 'Test start, devops_pipeline test !'
    logger.info(test_pipeline.__doc__)
    for pipeline_data_list in pipeline_data_lists:
        pipeline_data_list['build_time'] = int(time.time() * 1000)
    time.sleep(1)
    all_pipelines_name_id = all_pipeline_name_id(mysql_obj)
    pool_build = ThreadPoolExecutor(max_workers=50)
    futures_build = []
    for pipeline_data_list in pipeline_data_lists:
        pipeline_id = all_pipelines_name_id[pipeline_data_list['pipeline_data']['name']]
        pipeline_data = {
            "id": pipeline_id
        }
        build_pipeline_url = devops_test_data['common']['api_server'] + \
                             devops_test_data['performance']['pipeline']['path_build_pipeline'].replace("pipeline_id",
                                                                                                        str(pipeline_id))
        futures_build.append(pool_build.submit(build_pipeline, request_obj, pipeline_data,
                                               pipeline_data_list['pipeline_header'],
                                               build_pipeline_url))
    pool_build.shutdown()
    for future in as_completed(futures_build):
        future.result()

    # check devops list
    api_path1 = devops_test_data['performance']['pipeline']['pipeline_list'].replace("project_id", str(
        devops_test_data['common']['projectId']))
    pipeline_list_url = devops_test_data['common']['api_server'] + api_path1

    take_time1 = list_api(request_obj, header_after_login, pipeline_list_url)
    # check_table.add_row([pipeline_list_url, take_time1])
    insert1 = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
              "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=pipeline_table, api=api_path1, take_time=take_time1, c_time=datetime.now())
    mysql_show_obj.run_sql_cmd(insert1)

    api_path2 = devops_test_data['performance']['pipeline']['pipeline_build_list']
    pipeline_build_list_url = devops_test_data['common']['api_server'] + api_path2

    random_pipeline_id = str(list(random.choice(all_pipelines_name_id).values())[-1])
    data_pipeline_build_list = {
        "id": random_pipeline_id,
        "currentPage": 1,
        "pageSize": 10
    }
    take_time2 = create_api(request_obj, data_pipeline_build_list, header_after_login, pipeline_build_list_url)
    # check_table.add_row([pipeline_build_list_url, take_time2])
    insert2 = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
              "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=pipeline_table, api=api_path2, take_time=take_time2, c_time=datetime.now())
    mysql_show_obj.run_sql_cmd(insert2)

    api_path3 = devops_test_data['performance']['pipeline']['pipeline_build_detail'].replace("pipeline_id",
                                                                                             random_pipeline_id)
    pipeline_build_detail_url = devops_test_data['common']['api_server'] + api_path3

    take_time3 = list_api(request_obj, header_after_login, pipeline_build_detail_url)
    # check_table.add_row([pipeline_build_detail_url, take_time3])
    insert3 = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
              "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=pipeline_table, api=api_path3, take_time=take_time3, c_time=datetime.now())
    mysql_show_obj.run_sql_cmd(insert3)

    pool_check = ThreadPoolExecutor(max_workers=20)
    futures_check = []
    for pipeline_data_list in pipeline_data_lists:
        pipeline_id = all_pipelines_name_id[pipeline_data_list['pipeline_data']['name']]
        futures_check.append(pool_check.submit(is_pipeline_build_success, mysql_obj, pipeline_id,
                                               pipeline_data_list['build_time']))
    pool_check.shutdown()
    for future in as_completed(futures_check):
        future.result()


@pytest.mark.usefixtures("create_assist_job_dashboard_wait_plan_table")
def test_assist_job_dashboard_wait_plan(request_obj, devops_test_data, header_after_login, db,
                                        assist_job_dashboard_wait_plan_table, mysql_show_obj):
    test_assist_job_dashboard_wait_plan.__doc__ = 'Test start, assist_job_dashboard_wait_plan test !'
    logger.info(test_assist_job_dashboard_wait_plan.__doc__)
    wait_plan_data = devops_test_data['performance']['assist']['job_dashboard']['wait_plan']
    backlog_create_url = devops_test_data['common']['api_server'] + wait_plan_data['path']['create_backlog']

    pool_create_backlog = ThreadPoolExecutor(max_workers=1)
    future_create_backlog = []

    for i in range(wait_plan_data['backlog_quantity']):
        backlog_data = {
            "projectId": devops_test_data['common']['projectId'],
            "issueType": "{}".format(random.randint(1, 3)),
            "issueTitle": "autotest-{}-{}".format(time_str(), i)
        }
        future_create_backlog.append(pool_create_backlog.submit(create_api, request_obj, backlog_data,
                                                                header_after_login,
                                                                backlog_create_url, "Create wait plan -> backlogs"))
    pool_create_backlog.shutdown()
    for future in as_completed(future_create_backlog):
        future.result()

    api_path = wait_plan_data['path']['list_wait_plan']
    list_wait_plan_url = devops_test_data['common']['api_server'] + api_path
    list_plan_data = {
        "projectId": devops_test_data['common']['projectId']
    }
    take_time = create_api(request_obj, list_plan_data, header_after_login, list_wait_plan_url)
    # check_table.add_row([wait_plan_data['path']['list_wait_plan'], take_time])
    # logger.info("The {} response time table :\n{}".format(wait_plan_data['path']['list_wait_plan'], check_table))
    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=assist_job_dashboard_wait_plan_table, api=api_path, take_time=take_time,
                c_time=datetime.now())
    mysql_show_obj.run_sql_cmd(insert)


@pytest.mark.usefixtures("create_assist_current_iteration_swim_line_table")
def test_assist_current_iteration_swim_line(request_obj, devops_test_data, header_after_login, db,
                                            assist_current_iteration_swim_line_table, mysql_show_obj):
    test_assist_current_iteration_swim_line.__doc__ = 'Test start, assist_current_iteration_swim_line test !'
    logger.info(test_assist_current_iteration_swim_line.__doc__)
    swim_line_data = devops_test_data['performance']['assist']['current_iteration']['swim_line']
    issue_create_url = devops_test_data['common']['api_server'] + swim_line_data['path']['create_issue']

    pool_create_issue = ThreadPoolExecutor(max_workers=1)
    future_create_issue = []

    for i in range(swim_line_data['issue_quantity']):
        issue_data = {
            "issueTitle": "autotest-{}-{}".format(time_str(), i),
            "issueType": "{}".format(random.randint(1, 3)),
            "description": "<p>test</p>",
            "fileNames": [],
            "sprintId": devops_test_data['performance']['assist']['current_iteration']['sprintId'],
            "priority": random.randint(1, 3),
            "threats": [],
            "projectId": devops_test_data['common']['projectId']
        }
        if issue_data['issueType'] == "3":
            issue_data['level'] = "{}".format(random.randint(0, 3))
        future_create_issue.append(pool_create_issue.submit(create_api, request_obj, issue_data,
                                                            header_after_login,
                                                            issue_create_url,
                                                            "Create current_iteration -> issue"))
    pool_create_issue.shutdown()
    for future in as_completed(future_create_issue):
        future.result()

    api_path = swim_line_data['path']['list_swim_line']
    list_swim_line_url = devops_test_data['common']['api_server'] + api_path
    list_swim_line_data = {
        "projectId": devops_test_data['common']['projectId'],
        "sprintId": devops_test_data['performance']['assist']['current_iteration']['sprintId']
    }
    take_time = create_api(request_obj, list_swim_line_data, header_after_login, list_swim_line_url)
    # check_table.add_row([swim_line_data['path']['list_swim_line'], take_time])
    # logger.info("The {} response time table :\n{}".format(swim_line_data['path']['list_swim_line'], check_table))
    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=assist_current_iteration_swim_line_table, api=api_path, take_time=take_time,
                c_time=datetime.now())
    mysql_show_obj.run_sql_cmd(insert)


@pytest.mark.usefixtures("create_create_api_table")
@pytest.mark.usefixtures("create_list_api_table")
def test_assist_job_dashboard_all_issue(request_obj, mysql_show_obj, db, create_api_table, list_api_table,
                                        devops_test_data, header_after_login):
    test_assist_job_dashboard_all_issue.__doc__ = 'Test start, test_assist_job_dashboard_all_issue test !'
    logger.info(test_assist_job_dashboard_all_issue.__doc__)
    test_create_data = devops_test_data['performance']['assist']['job_dashboard']['all_issue']
    test_create_url = devops_test_data['common']['api_server'] + test_create_data['path']['create_issue']

    pool_create = ThreadPoolExecutor(max_workers=20)
    future_create = []

    for i in range(test_create_data['issue_quantity']):
        issue_data = {
            "issueTitle": "autotest-{}-{}".format(time_str(), i),
            "issueType": "{}".format(random.randint(1, 3)),
            "description": "<p>test</p>",
            "fileNames": [],
            "sprintId": devops_test_data['performance']['assist']['current_iteration']['sprintId'],
            "priority": random.randint(1, 3),
            "threats": [],
            "projectId": devops_test_data['common']['projectId']
        }
        if issue_data['issueType'] == "3":
            issue_data['level'] = "{}".format(random.randint(0, 3))

        future_create.append(pool_create.submit(create_api, request_obj, issue_data,
                                                header_after_login,
                                                test_create_url,
                                                "Create job_dashboard -> issue"))
    pool_create.shutdown()
    for future in as_completed(future_create):
        insert_create_api = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                            "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=create_api_table, api=test_create_data['path']['create_issue'],
                    take_time=future.result(), c_time=datetime.now())
        mysql_show_obj.run_sql_cmd(insert_create_api)

    test_list_url = devops_test_data['common']['api_server'] + test_create_data['path']['list_all_issue']
    test_list_data = {
        "projectId": devops_test_data['common']['projectId'],
        "currentPage": 1,
        "pageSize": 10,
        "typeCodeList": [],
        "statusCodeList": [],
        "startDate": "",
        "endDate": ""
    }
    take_time = create_api(request_obj, test_list_data, header_after_login, test_list_url)
    insert_list_api = "INSERT INTO {db}.{table} (api, take_time, c_time) VALUES ('{api}', '{take_time}', '{c_time}')". \
        format(db=db, table=list_api_table, api=test_create_data['path']['list_all_issue'], take_time=take_time,
               c_time=datetime.now())
    mysql_show_obj.run_sql_cmd(insert_list_api)


@pytest.mark.usefixtures("create_case_library_case_table")
def test_case_library_case(request_obj, devops_test_data, header_after_login, db, case_library_case_table,
                           mysql_show_obj):
    test_case_library_case.__doc__ = 'Test start, test_case_library_case test !'
    logger.info(test_case_library_case.__doc__)
    test_create_data = devops_test_data['performance']['test']['case_library']
    test_create_url = devops_test_data['common']['api_server'] + test_create_data['path']['create_case']

    pool_create = ThreadPoolExecutor(max_workers=20)
    future_create = []

    for i in range(test_create_data['case_quantity']):
        request_data = {
            "title": "autotest-{}-{}".format(time_str(), i),
            "parentId": test_create_data['case_group_id'],
            "level": random.randint(0, 4),
            "type": "{}".format(random.randint(0, 6)),
            "precondition": "test",
            "descriptionType": "1",
            "description": "test",
            "expectResult": "test",
            "fileNames": [],
            "descriptions": [],
            "projectId": devops_test_data['common']['projectId']
        }
        future_create.append(pool_create.submit(create_api, request_obj, request_data,
                                                header_after_login,
                                                test_create_url,
                                                "Create case_library -> case"))
    pool_create.shutdown()
    for future in as_completed(future_create):
        future.result()

    api_path = test_create_data['path']['list_cases']
    test_list_url = devops_test_data['common']['api_server'] + api_path
    test_list_data = {
        "projectId": devops_test_data['common']['projectId'],
        "currentPage": 1,
        "pageSize": 20
    }
    take_time = create_api(request_obj, test_list_data, header_after_login, test_list_url)
    # check_table.add_row([test_create_data['path']['list_cases'], take_time])
    # if take_time > 1000:
    #     raise Exception("The response's time of <{}>, check below table:\n{}".
    #                     format(test_create_data['path']['list_cases'], check_table))
    # else:
    #     logger.info("The {} response time table :\n{}".format(test_create_data['path']['list_cases'], check_table))
    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=case_library_case_table, api=api_path, take_time=take_time, c_time=datetime.now())
    mysql_show_obj.run_sql_cmd(insert)


@pytest.mark.usefixtures("create_create_api_table")
@pytest.mark.usefixtures("create_list_api_table")
def test_assist_og_issue(request_obj, devops_test_data, header_after_login, db, create_api_table, list_api_table,
                         mysql_show_obj):
    test_assist_og_issue.__doc__ = 'Test start, test_assist_og_issue test !'
    logger.info(test_assist_og_issue.__doc__)
    test_create_data = devops_test_data['performance']['assist']['originalIssue']
    test_create_url = devops_test_data['common']['api_server'] + test_create_data['path']['create_og_issue']

    pool_create = ThreadPoolExecutor(max_workers=20)
    future_create = []

    for i in range(test_create_data['og_issue_quantity']):
        request_data = devops_test_data['api_data']['project']['assist']['og_issue']['create_og_issue'].copy()
        request_data['summarize'] = "autotest-{}-{}".format(time_str(), i)
        request_data['source'] = "{}".format(random.choice(["客户", "老板", "客服", "收集"]))
        request_data['priority'] = random.randint(1, 3)
        request_data['projectId'] = devops_test_data['common']['projectId']
        future_create.append(pool_create.submit(create_api, request_obj, request_data,
                                                header_after_login,
                                                test_create_url,
                                                "Create assist -> original issue"))
    pool_create.shutdown()
    for future in as_completed(future_create):
        insert_create_api = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                            "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=create_api_table, api=test_create_data['path']['create_og_issue'],
                    take_time=future.result(), c_time=datetime.now())
        mysql_show_obj.run_sql_cmd(insert_create_api)

    list_url = devops_test_data['common']['api_server'] + test_create_data['path']['list_og_issue']
    list_data = devops_test_data['api_data']['project']['assist']['og_issue']['list_og_issue'].copy()
    list_data['projectId'] = devops_test_data['common']['projectId']
    list_data['pageSize'] = devops_test_data['common']['list_page_size']

    take_time = create_api(request_obj, list_data, header_after_login, list_url)
    insert_list_api = "INSERT INTO {db}.{table} (api, take_time, c_time) VALUES ('{api}', '{take_time}', '{c_time}')". \
        format(db=db, table=list_api_table, api=test_create_data['path']['list_og_issue'], take_time=take_time,
               c_time=datetime.now())
    mysql_show_obj.run_sql_cmd(insert_list_api)


@pytest.mark.usefixtures("create_test_plan_with_case_table")
def test_test_plan_with_case(request_obj, plan_name, devops_test_data, header_after_login, db,
                             test_plan_with_case_table, mysql_show_obj):
    test_test_plan_with_case.__doc__ = 'Test start, test_test_plan_with_case test !'
    logger.info(test_test_plan_with_case.__doc__)
    test_create_data = devops_test_data['performance']['test']['test_plan']

    test_create_url_case = devops_test_data['common']['api_server'] + test_create_data['path']['create_case']
    test_list_url_plan = devops_test_data['common']['api_server'] + test_create_data['path']['list_plan'] \
        .replace("pID", str(devops_test_data['common']['projectId']))
    test_create_url_plan = devops_test_data['common']['api_server'] + test_create_data['path']['create_test_plan']. \
        replace("pID", str(devops_test_data['common']['projectId']))

    results = request_obj.call('get', test_list_url_plan,
                               headers=header_after_login).json()
    is_not_exist_plan = False
    if results['data']:
        for result in results['data']:
            if result['title'] == plan_name:
                logger.info("Already exist test plan -> {}, not create it again !".format(plan_name))
                plan_id = result['id']
                break
            elif result == results['data'][-1]:
                is_not_exist_plan = True
    else:
        logger.info("Not exist any test plan!")
        is_not_exist_plan = True

    if is_not_exist_plan:
        logger.info("Create test plan -> {}!".format(plan_name))
        create_test_plan_data = {
            "title": plan_name,
            "phase": "{}".format(random.randint(1, 6)),
            "isAll": test_create_data['plan_is_all'],
            "projectId": devops_test_data['common']['projectId'],
            "enableSync": test_create_data['plan_sync']
        }
        create_api(request_obj, create_test_plan_data, header_after_login, test_create_url_plan)

        for res in request_obj.call('get', test_list_url_plan, headers=header_after_login).json()['data']:
            if res['title'] == plan_name:
                plan_id = res['id']
                break

    pool_create = ThreadPoolExecutor(max_workers=20)
    future_create = []

    for i in range(test_create_data['case_quantity']):
        request_data = {
            "title": "autotest-{}-{}".format(time_str(), i),
            "parentId": test_create_data['case_group_id'],
            "level": random.randint(0, 4),
            "type": "{}".format(random.randint(0, 6)),
            "precondition": "test",
            "descriptionType": "1",
            "description": "test",
            "expectResult": "test",
            "fileNames": [],
            "descriptions": [],
            "projectId": devops_test_data['common']['projectId']
        }
        future_create.append(pool_create.submit(create_api, request_obj, request_data,
                                                header_after_login,
                                                test_create_url_case,
                                                "Create test case -> case"))
    pool_create.shutdown()
    for future in as_completed(future_create):
        future.result()

    api_path = test_create_data['path']['list_case_from_plan']
    test_list_url = devops_test_data['common']['api_server'] + api_path
    test_list_data = {
        "testPlanId": plan_id
    }
    take_time = create_api(request_obj, test_list_data, header_after_login, test_list_url)
    # check_table.add_row([test_create_data['path']['list_case_from_plan'], take_time])
    # if take_time > 1000:
    #     raise Exception("The response's time of <{}>, check below table:\n{}".
    #                     format(test_create_data['path']['list_case_from_plan'], check_table))
    # else:
    #     logger.info("The {} response time table :\n{}".format(test_create_data['path']['list_case_from_plan'],
    #                                                           check_table))
    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=test_plan_with_case_table, api=api_path, take_time=take_time,
                c_time=datetime.now())
    mysql_show_obj.run_sql_cmd(insert)


@pytest.mark.usefixtures("create_test_plan_without_case_table")
def test_test_plan_without_case(request_obj, devops_test_data, header_after_login, db, test_plan_without_case_table,
                                mysql_show_obj):
    test_test_plan_with_case.__doc__ = 'Test start, test_test_plan_with_case test !'
    logger.info(test_test_plan_with_case.__doc__)
    test_create_data = devops_test_data['performance']['test']['test_plan']

    test_create_url = devops_test_data['common']['api_server'] + test_create_data['path']['create_test_plan']. \
        replace("pID", str(devops_test_data['common']['projectId']))

    pool_create = ThreadPoolExecutor(max_workers=10)
    future_create = []

    for i in range(test_create_data['plan_quantity']):
        request_data = {
            "title": "autotest-{}-{}".format(time_str(), i),
            "phase": "{}".format(random.randint(1, 6)),
            "isAll": test_create_data['plan_is_all'],
            "projectId": devops_test_data['common']['projectId'],
            "enableSync": test_create_data['plan_sync']
        }
        future_create.append(pool_create.submit(create_api, request_obj, request_data,
                                                header_after_login,
                                                test_create_url,
                                                "Create test -> test plan"))
    pool_create.shutdown()
    for future in as_completed(future_create):
        future.result()

    api_path = test_create_data['path']['list_plan'].replace("pID", str(devops_test_data['common']['projectId']))
    test_list_url = devops_test_data['common']['api_server'] + api_path

    take_time = list_api(request_obj, header_after_login, test_list_url)
    # check_table.add_row([test_create_data['path']['list_plan'].
    #                     replace("pID", str(devops_test_data['common']['projectId'])), take_time])
    # if take_time > 1000:
    #     raise Exception("The response's time of <{}>, check below table:\n{}".
    #                     format(test_create_data['path']['list_case_from_plan'], check_table))
    # else:
    #     logger.info("The {} response time table :\n{}".format(test_create_data['path']['list_case_from_plan'],
    #                                                           check_table))
    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=test_plan_without_case_table, api=api_path, take_time=take_time,
                c_time=datetime.now())
    mysql_show_obj.run_sql_cmd(insert)


@pytest.mark.usefixtures("create_test_team_setting_table")
def test_team_setting(request_obj, devops_test_data, header_after_login, db, test_team_setting_table, mysql_show_obj):
    test_team_setting.__doc__ = 'Test start, test_team_setting test !'
    logger.info(test_team_setting.__doc__)
    test_create_data = devops_test_data['performance']['setting']['team']

    test_create_url = devops_test_data['common']['api_server'] + test_create_data['path']['user_register']

    pool_create = ThreadPoolExecutor(max_workers=20)
    future_create = []
    date_tag = int(time.time() * 1000)
    for i in range(test_create_data['user_quantity']):
        request_data = {
            "username": "autotest_{}_{}".format(date_tag, i),
            "realName": "autotest_{}_{}".format(date_tag, i),
            "password": test_create_data['password'],
            "confirm": test_create_data['password']
        }
        header_register = devops_test_data['common']['header_without_login'].copy()
        header_register['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
                                        "(KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
        future_create.append(pool_create.submit(create_api, request_obj, request_data,
                                                header_register,
                                                test_create_url,
                                                "Create team -> Register user"))
    pool_create.shutdown()
    for future in as_completed(future_create):
        future.result()

    api_path = test_create_data['path']['list_team_user']
    test_list_url = devops_test_data['common']['api_server'] + api_path
    test_list_data = {
        "groupId": -1,
        "currentPage": 1,
        "pageSize": 10
    }
    take_time = create_api(request_obj, test_list_data, header_after_login, test_list_url)
    # check_table.add_row([test_create_data['path']['list_team_user'], take_time])
    # if take_time > 1000:
    #     raise Exception("The response's time of <{}>, check below table:\n{}".
    #                     format(test_create_data['path']['list_team_user'], check_table))
    # else:
    #     logger.info("The {} response time table :\n{}".format(test_create_data['path']['list_team_user'],
    #                                                           check_table))
    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=test_team_setting_table, api=api_path, take_time=take_time,
                c_time=datetime.now())
    mysql_show_obj.run_sql_cmd(insert)


@pytest.mark.usefixtures("create_role_setting_table")
def test_role_setting(request_obj, devops_test_data, header_after_login, db, role_setting_table, mysql_show_obj):
    test_role_setting.__doc__ = 'Test start, test_role_setting test !'
    logger.info(test_role_setting.__doc__)
    test_create_data = devops_test_data['performance']['setting']['role']

    test_create_url = devops_test_data['common']['api_server'] + test_create_data['path']['user_register']

    pool_create = ThreadPoolExecutor(max_workers=20)
    future_create = []
    date_tag = int(time.time() * 1000)
    for i in range(test_create_data['user_quantity']):
        request_data = {
            "username": "autotest_{}_{}".format(date_tag, i),
            "realName": "autotest_{}_{}".format(date_tag, i),
            "password": test_create_data['password'],
            "confirm": test_create_data['password']
        }
        header_register = devops_test_data['common']['header_without_login'].copy()
        header_register['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
                                        "(KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
        future_create.append(pool_create.submit(create_api, request_obj, request_data,
                                                header_register,
                                                test_create_url,
                                                "Create team -> register user"))
    pool_create.shutdown()
    for future in as_completed(future_create):
        future.result()

    api_path = test_create_data['path']['list_role_user']
    test_list_url = devops_test_data['common']['api_server'] + api_path

    take_time = list_api(request_obj, header_after_login, test_list_url)
    # check_table.add_row([test_create_data['path']['list_role_user'], take_time])
    # if take_time > 1000:
    #     raise Exception("The response's time of <{}>, check below table:\n{}".
    #                     format(test_create_data['path']['list_role_user'], check_table))
    # else:
    #     logger.info("The {} response time table :\n{}".format(test_create_data['path']['list_role_user'],
    #                                                           check_table))
    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=role_setting_table, api=api_path, take_time=take_time,
                c_time=datetime.now())
    mysql_show_obj.run_sql_cmd(insert)


@pytest.mark.usefixtures("create_work_platform_build_note_table")
def test_work_platform_build_note(request_obj, devops_test_data, mysql_obj, header_after_login,
                                  pipeline_with_platform_data_lists, db, work_platform_build_note_table,
                                  mysql_show_obj):
    test_work_platform_build_note.__doc__ = 'Test start, test_work_platform_build_note test !'
    logger.info(test_work_platform_build_note.__doc__)
    pipeline_names = all_pipeline_names(mysql_obj)
    build_time = int(time.time() * 1000)
    test_data = devops_test_data['performance']['work_platform']['build_note']

    pool_create = ThreadPoolExecutor(max_workers=1)
    futures_create = []

    for pipeline_data_list in pipeline_with_platform_data_lists:
        if pipeline_data_list['pipeline_data']['name'] not in pipeline_names:
            futures_create.append(pool_create.submit(create_api, request_obj,
                                                     pipeline_data_list['pipeline_data'],
                                                     pipeline_data_list['pipeline_header'],
                                                     pipeline_data_list['create_pipeline_url']))
        else:
            logger.info("{} already exist not create it again .".format(pipeline_data_list['pipeline_data']['name']))
    pool_create.shutdown()
    for future in as_completed(futures_create):
        future.result()

    all_pipeline_name_ids = all_pipeline_name_id(mysql_obj)
    time.sleep(2)
    pool_build = ThreadPoolExecutor(max_workers=2)
    futures_build = []

    for pipeline_data_list in pipeline_with_platform_data_lists:
        pipeline_id = all_pipeline_name_ids[pipeline_data_list['pipeline_data']['name']]
        pipeline_data = {
            "id": 1
        }
        build_pipeline_url = devops_test_data['common']['api_server'] + test_data['path']['build_pipeline']. \
            replace("pipeline_id", str(1))
        pipeline_data_list['build_time'] = build_time
        futures_build.append(pool_build.submit(create_api, request_obj,
                                               pipeline_data,
                                               pipeline_data_list['pipeline_header'],
                                               build_pipeline_url))
    pool_build.shutdown()
    for future in as_completed(futures_build):
        future.result()

    pool_check = ThreadPoolExecutor(max_workers=20)
    futures_check = []
    for pipeline_data_list in pipeline_with_platform_data_lists:
        pipeline_id = all_pipeline_name_ids[pipeline_data_list['pipeline_data']['name']]
        futures_check.append(pool_check.submit(is_pipeline_build_success, mysql_obj, 1,
                                               pipeline_data_list['build_time']))
    pool_create.shutdown()
    for future in as_completed(futures_check):
        future.result()

    api_path = test_data['path']['build_note']
    test_list_url = devops_test_data['common']['api_server'] + api_path
    list_data = {
        "currentPage": 1,
        "pageSize": 5
    }
    take_time = create_api(request_obj, list_data, header_after_login, test_list_url)
    # check_table.add_row([test_data['path']['build_note'], take_time])
    # if take_time > 1000:
    #     raise Exception("The response's time of <{}>, check below table:\n{}".
    #                     format(test_data['path']['build_note'], check_table))
    # else:
    #     logger.info("The {} response time table :\n{}".format(test_data['path']['build_note'], check_table))
    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=work_platform_build_note_table, api=api_path, take_time=take_time,
                c_time=datetime.now())
    mysql_show_obj.run_sql_cmd(insert)


@pytest.mark.usefixtures("create_work_platform_remain_issue_table")
def test_work_platform_remain_issue(request_obj, devops_test_data, header_after_login, db,
                                    work_platform_remain_issue_table, mysql_show_obj):
    test_work_platform_remain_issue.__doc__ = 'Test start, test_work_platform_remain_issue test !'
    logger.info(test_work_platform_remain_issue.__doc__)
    test_data = devops_test_data['performance']['work_platform']['remain_issue']
    test_create_url = devops_test_data['common']['api_server'] + test_data['path']['create_remain']

    pool_create = ThreadPoolExecutor(max_workers=1)
    future_create = []

    for i in range(test_data['remain_issue_quantity']):
        issue_data = {
            "issueTitle": "autotest-{}-{}".format(time_str(), i),
            "issueType": "{}".format(random.randint(1, 3)),
            "description": "<p>test</p>",
            "fileNames": [],
            "sprintId": test_data['sprintId'],
            "priority": random.randint(1, 3),
            "threats": [],
            "projectId": devops_test_data['common']['projectId'],
            "assigneeId": devops_test_data['common']['user_manager_id']
        }
        if issue_data['issueType'] == "3":
            issue_data['level'] = "{}".format(random.randint(0, 3))

        future_create.append(pool_create.submit(create_api, request_obj, issue_data,
                                                header_after_login,
                                                test_create_url,
                                                "Create remain -> issue"))
    pool_create.shutdown()
    for future in as_completed(future_create):
        future.result()

    api_path = test_data['path']['list_remain']
    test_list_url = devops_test_data['common']['api_server'] + api_path
    list_data = {
        "total": 1,
        "currentPage": 1,
        "pageSize": 5
    }
    take_time = create_api(request_obj, list_data, header_after_login, test_list_url)
    # check_table.add_row([test_data['path']['list_remain'], take_time])
    # if take_time > 1000:
    #     raise Exception("The response's time of <{}>, check below table:\n{}".
    #                     format(test_data['path']['list_remain'], check_table))
    # else:
    #     logger.info("The {} response time table :\n{}".format(test_data['path']['list_remain'],
    #                                                           check_table))
    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=work_platform_remain_issue_table, api=api_path, take_time=take_time,
                c_time=datetime.now())
    mysql_show_obj.run_sql_cmd(insert)


@pytest.mark.usefixtures("create_work_platform_project_table")
def test_work_platform_project(request_obj, devops_test_data, header_after_login, db, work_platform_project_table,
                               mysql_show_obj):
    test_work_platform_project.__doc__ = 'Test start, test_work_platform_project test !'
    logger.info(test_work_platform_project.__doc__)
    test_data = devops_test_data['performance']['work_platform']['project']

    test_create_url = devops_test_data['common']['api_server'] + test_data['path']['create_project']

    pool_create = ThreadPoolExecutor(max_workers=20)
    future_create = []

    for i in range(test_data['project_quantity']):
        issue_data = {
            "projectProd": {
                "principalId": "1",
                "name": "autotest-{}-{}".format(time_str(), i),
                "description": "test",
                "projectCycle": "",
                "projectImage": ""
            },
            "user": [
                {
                    "id": test_data['admin_user_id']
                }
            ]
        }
        future_create.append(pool_create.submit(create_api, request_obj, issue_data,
                                                header_after_login,
                                                test_create_url,
                                                "Create project -> project"))
    pool_create.shutdown()
    for future in as_completed(future_create):
        future.result()

    api_path = test_data['path']['list_project']
    test_list_url = devops_test_data['common']['api_server'] + api_path
    take_time = list_api(request_obj, header_after_login, test_list_url)
    # check_table.add_row([test_data['path']['list_project'], take_time])
    # if take_time > 1000:
    #     raise Exception("The response's time of <{}>, check below table:\n{}".
    #                     format(test_data['path']['list_project'], check_table))
    # else:
    #     logger.info("The {} response time table :\n{}".format(test_data['path']['list_project'],
    #                                                           check_table))
    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=work_platform_project_table, api=api_path, take_time=take_time,
                c_time=datetime.now())
    mysql_show_obj.run_sql_cmd(insert)


@pytest.mark.usefixtures("create_work_platform_member_project_table")
def test_work_platform_member_project(request_obj, mysql_obj, devops_test_data, header_after_login, member_of_project,
                                      db, work_platform_member_project_table, mysql_show_obj):
    test_work_platform_member_project.__doc__ = 'Test start, test_work_platform_member_project test !'
    logger.info(test_work_platform_member_project.__doc__)
    test_data = devops_test_data['performance']['work_platform']['project']['project_user']
    test_register_user_url = devops_test_data['common']['api_server'] + test_data['path']['user_register']
    test_add_member_to_project_url = devops_test_data['common']['api_server'] + test_data['path']['add_project_user']

    pool_register = ThreadPoolExecutor(max_workers=20)
    future_register = []

    for member_data in member_of_project:
        future_register.append(pool_register.submit(create_api, request_obj, member_data,
                                                    devops_test_data['common']['header_without_login'],
                                                    test_register_user_url,
                                                    "Create team -> register user"))
    pool_register.shutdown()
    for future in as_completed(future_register):
        future.result()

    all_member_name_ids = all_member_name_id(mysql_obj)
    pool_add = ThreadPoolExecutor(max_workers=10)
    future_add = []

    for member_data in member_of_project:
        data = {
            "projectId": test_data['projectId'],
            "userId": all_member_name_ids[member_data['username']],
            "roleIds": random.sample(test_data['roleIDs'], random.randint(1, len(test_data['roleIDs'])))
        }
        future_add.append(pool_add.submit(update_api, request_obj, data,
                                          header_after_login,
                                          test_add_member_to_project_url,
                                          "Add project -> member of project"))
    pool_add.shutdown()
    for future in as_completed(future_add):
        future.result()

    api_path = test_data['path']['list_project_user']
    test_list_url = devops_test_data['common']['api_server'] + api_path
    take_time = list_api(request_obj, header_after_login, test_list_url)
    # check_table.add_row([test_data['path']['list_project_user'], take_time])
    # if take_time > 1000:
    #     raise Exception("The response's time of <{}>, check below table:\n{}".
    #                     format(test_data['path']['list_project_user'], check_table))
    # else:
    #     logger.info("The {} response time table :\n{}".format(test_data['path']['list_project_user'],
    #                                                           check_table))
    insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
             "VALUES ('{api}', '{take_time}', '{c_time}')" \
        .format(db=db, table=work_platform_member_project_table, api=api_path, take_time=take_time,
                c_time=datetime.now())
    mysql_show_obj.run_sql_cmd(insert)


@pytest.mark.usefixtures("create_assist_multiple_user_table")
def test_assist_multiple_user(request_obj, mysql_obj, register_user, devops_test_data, db, assist_multiple_user_table,
                              mysql_show_obj):
    test_assist_multiple_user.__doc__ = 'Test start, test_assist_multiple_user test !'
    logger.info(test_assist_multiple_user.__doc__)
    user_info = devops_test_data['performance']['multiple_users']

    issue_create_path = user_info['path']['issue_create']
    issue_update_path = user_info['path']['issue_update']
    issue_create_url = devops_test_data['common']['api_server'] + issue_create_path
    issue_update_url = devops_test_data['common']['api_server'] + issue_update_path
    user_tokens = []

    pool_login = ThreadPoolExecutor(max_workers=20)
    future_login = []
    for user in register_user:
        for username, _ in user.items():
            login_url = devops_test_data['common']['api_server'] + devops_test_data['login_info']['login_path']
            future_login.append(pool_login.submit(login_token, request_obj, username, user_info['password'], login_url))
    pool_login.shutdown()
    for future in as_completed(future_login):
        user_tokens.append(future.result())

    token_with_issue_names = {}  # Bind token to issue
    pool_create = ThreadPoolExecutor(max_workers=user_info['user_quantity'])
    future_create = []
    token_num = 0
    for token in user_tokens:
        issue_name = "autotest-{}-{}".format(time_str(), token_num)
        issue_data = {
            "issueTitle": issue_name,
            "issueType": "{}".format(random.randint(1, 3)),
            "description": "<p>test</p>",
            "fileNames": [],
            "sprintId": user_info['sprintId'],
            "priority": random.randint(1, 3),
            "threats": [],
            "projectId": devops_test_data['common']['projectId']
        }
        if issue_data['issueType'] == "3":
            issue_data['level'] = "{}".format(random.randint(0, 3))

        issue_header = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": token
        }
        future_create.append(pool_create.submit(create_api, request_obj, issue_data, issue_header, issue_create_url))
        token_num += 1
        token_with_issue_names[issue_name] = token
    pool_create.shutdown()
    for future in as_completed(future_create):
        # multiple_user_table.add_row(["Create issue", future.result()])
        insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                 "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=assist_multiple_user_table, api=issue_create_path, take_time=future.result(),
                    c_time=datetime.now())
        mysql_show_obj.run_sql_cmd(insert)

    all_issues = all_issue_name_id(mysql_obj)  # Get all issue_id from mysql
    pool_update = ThreadPoolExecutor(max_workers=user_info['user_quantity'])
    future_update = []
    for issue_name, token in token_with_issue_names.items():
        issue_data = {
            "issueId": all_issues[issue_name],
            "description": "<p>test auto update</p>"
        }
        header = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": token
        }
        future_update.append(pool_update.submit(create_api, request_obj, issue_data, header, issue_update_url))
    pool_update.shutdown()
    for future in as_completed(future_update):
        # multiple_user_table.add_row(["Update issue", future.result()])
        insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                 "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=assist_multiple_user_table, api=issue_update_path, take_time=future.result(),
                    c_time=datetime.now())
        mysql_show_obj.run_sql_cmd(insert)
    pool_get = ThreadPoolExecutor(max_workers=user_info['user_quantity'])
    future_get = []
    for issue_name, token in token_with_issue_names.items():
        header = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": token
        }
        issue_get_path = user_info['path']['issue_detail'].replace("issue_id", str(all_issues[issue_name])).replace(
            "project_id", str(devops_test_data['common']['projectId']))
        issue_get_url = devops_test_data['common']['api_server'] + issue_get_path

        future_get.append(pool_get.submit(list_api, request_obj, header, issue_get_url))
    pool_get.shutdown()
    for future in as_completed(future_get):
        # multiple_user_table.add_row(["Get issue detail", future.result()])
        insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                 "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=assist_multiple_user_table, api=issue_get_path, take_time=future.result(),
                    c_time=datetime.now())
        mysql_show_obj.run_sql_cmd(insert)

    pool_delete = ThreadPoolExecutor(max_workers=user_info['user_quantity'])
    future_delete = []
    for issue_name, token in token_with_issue_names.items():
        header = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": token
        }
        issue_delete_path = user_info['path']['issue_delete'].replace("issue_id", str(all_issues[issue_name]))
        issue_delete_url = devops_test_data['common']['api_server'] + issue_delete_path

        future_delete.append(pool_delete.submit(delete_api, request_obj, header, issue_delete_url))
    pool_delete.shutdown()
    for future in as_completed(future_delete):
        # multiple_user_table.add_row(["Delete issue", future.result()])
        insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                 "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=assist_multiple_user_table, api=issue_delete_path, take_time=future.result(),
                    c_time=datetime.now())
        mysql_show_obj.run_sql_cmd(insert)
    # logger.info("The response detail check below table\n{}".format(multiple_user_table))


@pytest.mark.usefixtures("create_cases_multiple_user_table")
def test_cases_multiple_user(request_obj, mysql_obj, register_user, devops_test_data, db, cases_multiple_user_table,
                             mysql_show_obj):
    test_cases_multiple_user.__doc__ = 'Test start, test_cases_multiple_user test !'
    logger.info(test_cases_multiple_user.__doc__)
    user_info = devops_test_data['performance']['multiple_users']
    case_create_path = user_info['path']['case_create']
    case_update_path = user_info['path']['case_update']
    case_create_url = devops_test_data['common']['api_server'] + case_create_path
    case_update_url = devops_test_data['common']['api_server'] + case_update_path
    user_tokens = []

    pool_login = ThreadPoolExecutor(max_workers=20)
    future_login = []
    for user in register_user:
        for username, _ in user.items():
            login_url = devops_test_data['common']['api_server'] + devops_test_data['login_info']['login_path']
            future_login.append(pool_login.submit(login_token, request_obj, username, user_info['password'], login_url))
    pool_login.shutdown()
    for future in as_completed(future_login):
        user_tokens.append(future.result())

    token_with_case_names = {}  # Bind token to case
    pool_create = ThreadPoolExecutor(max_workers=user_info['user_quantity'])
    future_create = []
    token_num = 0
    for token in user_tokens:
        case_name = "autotest-{}-{}".format(time_str(), token_num)
        case_data = {
            "title": case_name,
            "parentId": user_info['case']['case_group_id'],
            "level": random.randint(0, 4),
            "type": "{}".format(random.randint(0, 6)),
            "precondition": "test",
            "descriptionType": "{}".format(random.randint(1, 2)),
            "description": "test",
            "expectResult": "test",
            "fileNames": [],
            "descriptions": [],
            "projectId": devops_test_data['common']['projectId']
        }
        if case_data['descriptionType'] == "2":
            case_data['descriptions'] = [{"description": "test-{}".format(i), "expectResult": "test-{}".format(i)}
                                         for i in range(random.randint(1, 10))]
            case_data.pop('description')
            case_data.pop('expectResult')
        case_header = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": token
        }
        future_create.append(pool_create.submit(create_api, request_obj, case_data, case_header, case_create_url))
        token_num += 1
        token_with_case_names[case_name] = token
    pool_create.shutdown()
    for future in as_completed(future_create):
        # multiple_user_table.add_row(["Create case", future.result()])
        insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                 "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=cases_multiple_user_table, api=case_create_path, take_time=future.result(),
                    c_time=datetime.now())
        mysql_show_obj.run_sql_cmd(insert)

    users_id_real_name = all_user_id_real_name(mysql_obj)
    all_cases = all_case_name_id(mysql_obj)  # Get all issue_id from mysql
    pool_update = ThreadPoolExecutor(max_workers=user_info['user_quantity'])
    future_update = []
    for case_name, token in token_with_case_names.items():
        case_data = user_info['case']['edit_data'].copy()
        case_data['id'] = all_cases[case_name]['id']
        case_data['title'] = case_name
        case_data['parentId'] = user_info['case']['case_group_id']
        case_data['projectId'] = devops_test_data['common']['projectId']
        case_data['level'] = random.randint(0, 4)
        case_data['type'] = "{}".format(random.randint(0, 6))
        case_data['precondition'] = "test"
        case_data['descriptionType'] = "{}".format(random.randint(1, 2))
        case_data['path'] = user_info['case']['group_path']
        case_data['directoryPath'] = "0,1"
        case_data['description'] = "test"
        case_data['expectResult'] = "test"
        case_data['descriptions'] = []
        case_data['creatorName'] = users_id_real_name[all_cases[case_name]['creator_id']]
        case_data['creatorId'] = all_cases[case_name]['creator_id']

        if case_data['descriptionType'] == "2":
            case_data['descriptions'] = [{"description": "test-{}".format(i), "expectResult": "test-{}".format(i)}
                                         for i in range(random.randint(1, 10))]
            case_data.pop('description')
            case_data.pop('expectResult')
        header = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": token
        }
        future_update.append(pool_update.submit(create_api, request_obj, case_data, header, case_update_url))
    pool_update.shutdown()
    for future in as_completed(future_update):
        # multiple_user_table.add_row(["Update case", future.result()])
        insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                 "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=cases_multiple_user_table, api=case_update_path, take_time=future.result(),
                    c_time=datetime.now())
        mysql_show_obj.run_sql_cmd(insert)

    pool_get = ThreadPoolExecutor(max_workers=user_info['user_quantity'])
    future_get = []
    for case_name, token in token_with_case_names.items():
        header = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": token
        }
        case_get_path = user_info['path']['case_detail'].replace("case_id", str(all_cases[case_name]['id']))
        case_get_url = devops_test_data['common']['api_server'] + case_get_path

        future_get.append(pool_get.submit(list_api, request_obj, header, case_get_url))
    pool_get.shutdown()
    for future in as_completed(future_get):
        # multiple_user_table.add_row(["Get case detail", future.result()])
        insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                 "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=cases_multiple_user_table, api=case_get_path, take_time=future.result(),
                    c_time=datetime.now())
        mysql_show_obj.run_sql_cmd(insert)
    pool_delete = ThreadPoolExecutor(max_workers=user_info['user_quantity'])
    future_delete = []
    for case_name, token in token_with_case_names.items():
        header = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": token
        }
        delete_data = [
            all_cases[case_name]['id']
        ]
        case_delete_path = user_info['path']['case_delete']
        case_delete_url = devops_test_data['common']['api_server'] + case_delete_path
        future_delete.append(pool_delete.submit(delete_api, request_obj, header, case_delete_url, delete_data))
    pool_delete.shutdown()
    for future in as_completed(future_delete):
        # multiple_user_table.add_row(["Delete case", future.result()])
        insert = "INSERT INTO {db}.{table} (api, take_time, c_time) " \
                 "VALUES ('{api}', '{take_time}', '{c_time}')" \
            .format(db=db, table=cases_multiple_user_table, api=case_delete_path, take_time=future.result(),
                    c_time=datetime.now())
        mysql_show_obj.run_sql_cmd(insert)

    # logger.info("The response detail check below table\n{}".format(multiple_user_table))


def test_tmptest(pipeline_create):
    logger.info("Done")
