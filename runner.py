import pytest
import os
import traceback
from settings.global_settings import PROJECT_PATH
from utils.times import time_str
from libs.log_obj import LogObj


def run(project, args):
    new_time_str = time_str()
    if args.log_dir:
        log_file_dir = os.path.join(PROJECT_PATH, 'log/{0}'.format(args.log_dir))
    else:
        if 'ip' in args and args.ip:
            log_file_dir = os.path.join(PROJECT_PATH, 'log/{0}/{1}/{2}/{3}'.format(project, args.action,
                                                                                   args.ip.replace('.', '_'),
                                                                                   new_time_str))
        else:
            log_file_dir = os.path.join(PROJECT_PATH, 'log/{0}/{1}/{2}'.format(project, args.action, new_time_str))
    log_file = 'test.log'
    logger = LogObj(log_file_dir, log_file).get_logger()
    log_file_path = os.path.join(log_file_dir, log_file)

    send_files = []
    send_files.append(log_file_path)
    if args.log_dir:
        report_file_dir = os.path.join(PROJECT_PATH, 'report/{0}/'.format('/'.join(args.log_dir.split('/')[:-1])))
        html_name = 'Report-{0}.html'.format(args.log_dir.split('/')[-1])
    else:
        report_file_dir = os.path.join(PROJECT_PATH, 'report/{0}/{1}/'.format(project, args.action))
        html_name = 'Report-{0}.html'.format(new_time_str)
    if not os.path.exists(report_file_dir):
        os.makedirs(report_file_dir)
    html_path = os.path.join(report_file_dir, html_name)
    send_files.append(html_path)

    from common.common import load_yaml
    run_list = []
    if project == 'stress' or (project == 'interface' and args.action == 'tool'):
        run_list.extend(args.cases)
    else:
        run_cases = load_yaml(args.suite_file)

        for module, cases in run_cases.items():
            if cases:
                run_list.extend(cases)
    run_tests = ' or '.join(run_list)
    feature_script = os.path.join(PROJECT_PATH, '{0}/{1}/cases/'.format(project, args.action))
    if args.show_case:
        cmd = ['--collect-only', feature_script]
    else:
        if project == 'web':
            cmd = ['-sv', '-k {tests}'.format(tests=run_tests)]
        elif project == 'interface':
            cmd = ['-sv']
        else:
            cmd = ['-xsv', '-k {tests}'.format(tests=run_tests)]
        cmd.extend(
            ['--capture=no', '--show-capture=no', '--disable-warnings', '--tb=short',
             '--count={iteration}'.format(iteration=args.iteration), '--repeat-scope=session', '--instafail',
             '--html={path}'.format(path=html_path), '--self-contained-html', feature_script]
        )

    logger.info('Run test command: {0}'.format(cmd))
    result = pytest.main(cmd)

    config_data = load_yaml(os.path.join(PROJECT_PATH, 'config/config.yaml'))
    email_config_data = config_data['email']
    if not args.show_case and email_config_data['send']:
        if result == pytest.ExitCode.OK:
            title = 'PASSED: {0} {1} {2}'.format(project.upper(), args.action.upper(), '-'.join(args.cases))
        elif result == pytest.ExitCode.INTERRUPTED:
            title = 'PASSED by Canceled: {0} {1} {2}'.format(project.upper(), args.action.upper(), '-'.join(args.cases))
        else:
            title = 'FAILED: {0} {1} {2}'.format(project.upper(), args.action.upper(), '-'.join(args.cases))
        sender = email_config_data['sender']
        receivers = email_config_data['receivers'].split(',')
        smtp_server = email_config_data['smtp_server']
        username = email_config_data['username']
        password = email_config_data['password']
        smtp_port = email_config_data['smtp_port']

        from libs.email_obj import EmailObj
        email_obj = EmailObj(smtp_server, smtp_port, username, password)
        try:
            email_obj.send(sender, receivers, title, send_files)
        except Exception:
            logger.error('Test result send fail, error is {0}!'.format(traceback.format_exc()))
        else:
            logger.info('Test result send to {0} success!'.format(receivers))
    return result