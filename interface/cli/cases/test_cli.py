import pytest
import re
from libs.ssh_obj import SSHObj
from libs.log_obj import LogObj
from libs.excel_obj import ExcelObj
from interface import arguments
from interface.common.common import get_cli_cases_info
from utils.times import sleep


logger = LogObj().get_logger()
args = arguments.parse_arg()


@pytest.fixture(scope='session')
def ssh_obj():
    return SSHObj(args.ip, args.sys_user, args.sys_pwd)


@pytest.fixture(scope='session')
def excel_obj():
    return ExcelObj(args.data_file)


@pytest.mark.parametrize("cli_info", get_cli_cases_info(args.data_file, args.suite_file))
def test_cli(ssh_obj, cli_info, global_config, cli_config):
    test_cli.__doc__ = cli_info['case_name']
    cmd = []
    for item in cli_info['cmd'].split():
        results = re.findall("\\$\w+", item)
        for result in results:
            item = item.replace(result, cli_config['variable'][result.split('$')[-1]])
        cmd.append(item)

    new_cmd = ' '.join(map(str, cmd))
    rtn_dict = ssh_obj.run_cmd(new_cmd)
    logger.debug(rtn_dict)
    actual_result = '{0} {1}'.format(rtn_dict['stdout'], rtn_dict['stderr'])
    if global_config['save_result']:
        row = excel_obj.get_cell_row(cli_info['case_name'], cli_info['module_name'])
        actual_rc_col = excel_obj.get_cell_col('actual_rc', cli_info['module_name'])
        actual_result_col = excel_obj.get_cell_col('actual_result', cli_info['module_name'])
        excel_obj.write_cell(row, actual_rc_col, rtn_dict['rc'], cli_info['module_name'])
        excel_obj.write_cell(row, actual_result_col, actual_result, cli_info['module_name'])
    assert rtn_dict['rc'] == cli_info['expect_rc']
    if cli_info['expect_pattern']:
        assert re.findall(cli_info['expect_pattern'], actual_result)
    if 'interval_time' in cli_info and cli_info['interval_time']:
        sleep(cli_info['interval_time'])
