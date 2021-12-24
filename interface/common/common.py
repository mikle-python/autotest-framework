import re
import os
import yaml
from libs.excel_obj import ExcelObj
from libs.log_obj import LogObj
from settings.global_settings import PROJECT_PATH


logger = LogObj().get_logger()


def read_cases_data(data_file, sheet):
    cases_data = []
    excel_obj = ExcelObj(data_file)
    key_list = excel_obj.get_rows_values(0, sheet)
    for nrow in range(1, excel_obj.get_sheet_nrows(sheet)):
        cases_data.append(dict(zip(key_list, excel_obj.get_rows_values(nrow, sheet))))
    return cases_data


def get_run_cases(suite_file):
    with open(suite_file, mode='r') as file_obj:
        run_cases = yaml.load(file_obj, Loader=yaml.FullLoader)
    return run_cases


def get_cli_cases_info(data_file, suite_file):
    run_cases = get_run_cases(suite_file)
    clis_info = []
    pattern = '_'
    for module_name, case_names in run_cases.items():
        if not case_names:
            continue
        cases_data = read_cases_data(data_file, module_name)
        for case_data in cases_data:
            if case_data['case_name'] in case_names:
                case_data['module_name'] = module_name
                tmp_cmd = []
                for key_name, data in case_data.items():
                    if key_name is None:
                        continue
                    if data is None:
                        data = ''
                    if key_name == 'bin':
                        tmp_cmd.append(data)
                    m = re.match(pattern, key_name)
                    if m:
                        tmp_cmd.append(data)
                cmd = ' '.join(map(str, tmp_cmd))
                case_data['cmd'] = cmd
                clis_info.append(case_data)
    return clis_info


def get_api_cases_info(data_file, suite_file):
    run_cases = get_run_cases(suite_file)
    apis_info = []
    for module_name, case_names in run_cases.items():
        if not case_names:
            continue
        cases_data = read_cases_data(data_file, module_name)
        for case_data in cases_data:
            if case_data['case_name'] in case_names:
                case_data['module_name'] = module_name
                apis_info.append(case_data)
    return apis_info


if __name__ == '__main__':
    print(get_cli_cases_info('C:/test/newben_cli_arm64.xlsx', 'C:/test/newben_cli_arm64_suites.yaml'))