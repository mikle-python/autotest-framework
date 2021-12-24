import pytest
import json
import re
from libs.request_obj import RequstObj
from libs.log_obj import LogObj
from libs.excel_obj import ExcelObj
from interface import arguments
from interface.common.common import get_api_cases_info, read_cases_data
from jsonpath import jsonpath
from utils.times import sleep


logger = LogObj().get_logger()
args = arguments.parse_arg()


@pytest.fixture(scope='session')
def request_obj():
    return RequstObj()


@pytest.fixture(scope='session')
def excel_obj():
    return ExcelObj(args.data_file)


@pytest.fixture(scope='session')
def token(request_obj, api_config):
    case_data = read_cases_data(args.data_file, 'get_token')[0]
    if case_data['method']:
        results = re.findall("\\$\w+", case_data['method'])
        for result in results:
            case_data['method'] = case_data['method'].replace(result, api_config['variable'][result.split('$')[-1]])

    if case_data['url']:
        results = re.findall("\\$\w+", case_data['url'])
        for result in results:
            case_data['url'] = case_data['url'].replace(result, api_config['variable'][result.split('$')[-1]])

    if case_data['headers']:
        results = re.findall("\\$\w+", case_data['headers'])
        for result in results:
            case_data['headers'] = case_data['headers'].replace(result, api_config['variable'][result.split('$')[-1]])

    if case_data['data']:
        results = re.findall("\\$\w+", case_data['data'])
        for result in results:
            case_data['data'] = case_data['data'].replace(result, api_config['variable'][result.split('$')[-1]])

    if args.sys_port != 22:
        login_url = 'http://{0}:{1}/{2}'.format(args.ip, args.sys_port, case_data['url'])
    else:
        login_url = 'http://{0}/{1}'.format(args.ip, case_data['url'])
    if case_data['headers']:
        headers = json.loads(case_data['headers'])
    else:
        headers = None
    response = request_obj.call(case_data['method'], login_url, data=case_data['data'], headers=headers)
    response_text = json.loads(response.text)
    logger.debug(response_text)
    try:
        token = response_text['data']
    except Exception:
        token = response_text['venus']
    return token


@pytest.mark.parametrize("api_info", get_api_cases_info(args.data_file, args.suite_file))
def test_api(request_obj, excel_obj, api_info, token, global_config, api_config):
    test_api.__doc__ = api_info['case_name']
    logger.debug(test_api.__doc__)

    if api_info['method']:
        results = re.findall("\\$\w+", api_info['method'])
        for result in results:
            api_info['method'] = api_info['method'].replace(result, api_config['variable'][result.split('$')[-1]])

    if api_info['url']:
        results = re.findall("\\$\w+", api_info['url'])
        for result in results:
            api_info['url'] = api_info['url'].replace(result, api_config['variable'][result.split('$')[-1]])

    if api_info['headers']:
        results = re.findall("\\$\w+", api_info['headers'])
        for result in results:
            api_info['headers'] = api_info['headers'].replace(result, api_config['variable'][result.split('$')[-1]])

    if api_info['data']:
        results = re.findall("\\$\w+", api_info['data'])
        for result in results:
            api_info['data'] = api_info['data'].replace(result, api_config['variable'][result.split('$')[-1]])

    if 'login' not in api_info['case_name']:
        if api_info['headers']:
            headers = json.loads(api_info['headers'])
            headers['Authorization'] = token
        else:
            api_info['headers'] = {'Authorization': token}
    else:
        if api_info['headers']:
            headers = json.loads(api_info['headers'])
        else:
            headers = None

    if args.sys_port != 22:
        url = 'http://{0}:{1}/{2}'.format(args.ip, args.sys_port, api_info['url'])
    else:
        url = 'http://{0}/{1}'.format(args.ip, api_info['url'])
    response = request_obj.call(api_info['method'], url, data=api_info['data'], headers=headers)
    logger.debug(response.text)
    response_text = json.loads(response.text)
    status_code = response.status_code
    if global_config['save_result']:
        row = excel_obj.get_cell_row(api_info['case_name'], api_info['module_name'])
        actual_rc_col = excel_obj.get_cell_col('actual_rc', api_info['module_name'])
        actual_result_col = excel_obj.get_cell_col('actual_result', api_info['module_name'])
        excel_obj.write_cell(row, actual_rc_col, status_code, api_info['module_name'])
        excel_obj.write_cell(row, actual_result_col, response.text, api_info['module_name'])
    if api_info['expect_pattern']:
        expect_pattern = json.loads(api_info['expect_pattern'])
        expect_key_pattern = expect_pattern['key_name']
        expect_value_pattern = expect_pattern['value']
        assert (status_code == api_info['expect_rc'] and
                expect_value_pattern in jsonpath(response_text, '$..{0}'.format(expect_key_pattern)))
    else:
        assert status_code == api_info['expect_rc']
    if 'interval_time' in api_info and api_info['interval_time']:
        sleep(api_info['interval_time'])