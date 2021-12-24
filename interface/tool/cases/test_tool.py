import pytest
import os
from common.common import dump_yaml_data
from libs.log_obj import LogObj
from libs.excel_obj import ExcelObj
from interface import arguments
from interface.common.common import read_cases_data


logger = LogObj().get_logger()
args = arguments.parse_arg()


@pytest.fixture(scope='session')
def excel_obj():
    return ExcelObj(args.data_file)


@pytest.fixture(scope='session')
def suite_file():
    return '{0}.yaml'.format(os.path.splitext(args.data_file)[0])


def test_generate_suites(excel_obj, suite_file):
    yaml_data = dict()
    for sheet_name in excel_obj.sheet_names:
        yaml_data[sheet_name] = []
        for case_data in read_cases_data(args.data_file, sheet_name):
            if 'case_name' in case_data and case_data['case_name']:
                yaml_data[sheet_name].append(case_data['case_name'])
    dump_yaml_data(yaml_data, suite_file)