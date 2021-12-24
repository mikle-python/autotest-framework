import pytest
import os
from web import arguments
from libs.browser_obj import BrowserObj
from utils.times import time_str
from libs.log_obj import LogObj
from common.common import load_yaml
from settings.global_settings import PROJECT_PATH


args = arguments.parse_arg()
browser_obj = None


def pytest_configure(config):
    if 'ip' in args and args.ip:
        config._metadata['Testbed'] = args.ip


@pytest.fixture(scope='session')
def config():
    return load_yaml(os.path.join(PROJECT_PATH, 'web/config/config.yaml'))


@pytest.fixture(scope='session', autouse=True)
def browser_obj(config):
    global browser_obj
    browser_obj = BrowserObj(config['browser'])
    return browser_obj


@pytest.fixture(scope='session', autouse=True)
def quit(browser_obj):
    yield
    browser_obj.quit()


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            pic_path = os.path.join(LogObj._instance.log_dir, "{0}-test.png".format(time_str()))
            browser_obj.save_screenshot(pic_path)
            if pic_path:
                html = '<div><img src="%s" alt="screenshot" style="width:1200px;height:600px;" ' \
                       'οnclick="window.open(this.src)" align="right"/></div>' % pic_path
                extra.append(pytest_html.extras.html(html))
        report.extra = extra