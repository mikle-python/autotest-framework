import pytest
import time
from _pytest import terminal
from py._xmlgen import html
from libs.log_obj import LogObj


logger = LogObj().get_logger()


@pytest.mark.optionalhook
def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([html.p("Tester: Luo Chao")])


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(2, html.th('Description'))
    cells.pop()


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(report.description))
    cells.pop()


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)


def pytest_html_results_table_html(report, data):
    if report.failed:
        del data[:]
        data.append(html.div(report.longrepr, class_='empty log'))


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    total = len([i for i in terminalreporter.stats.get('', []) if i.when == 'call'])
    passed = len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])
    failed = len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])
    errored = len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])
    skipped = len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
    successful = len(terminalreporter.stats.get('passed', [])) / total
    duration = time.time() - terminalreporter._sessionstarttime

    with open('{0}/result.txt'.format(LogObj._instance.log_dir), "w") as fp:
        fp.write("TOTAL={0}\n".format(total))
        fp.write("PASSED={0}\n".format(passed))
        fp.write("FAILED={0}\n".format(failed))
        fp.write("ERROR={0}\n".format(errored))
        fp.write("SKIPPED={0}\n".format(skipped))
        fp.write("SUCCESSFUL={0:.2%}\n".format(successful))
        fp.write("TOTAL_TIMES={0:.2f}s\n".format(duration))
