import pytest
from libs.log_obj import LogObj
from selenium.webdriver.common.by import By
from utils.times import sleep
from utils.util import generate_string
from web import arguments


args = arguments.parse_arg()
logger = LogObj().get_logger()


@pytest.fixture(scope='function', autouse=True)
def open_login_url(browser_obj, login_url):
    browser_obj.open_url(login_url)


def test_login_page_check(browser_obj):
    assert browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/div/div[1]/p[1]')).text == "Ghostcloud"
    assert browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/div/div[1]/p[2]')).text == "专属军工领域的DevOps体系"
    assert browser_obj.find_element((
        By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[1]/div/span')).text == "DevMilOps"
    assert browser_obj.find_element((
        By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[2]/div[1]/div[1]/label')).text == "内置"
    assert browser_obj.find_element((
        By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[2]/div[1]/div[2]/label')).text == "LDAP"
    assert browser_obj.find_element((
        By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[2]/form/div[1]/div/div[1]/div/span/span[1]/label'
    )).text == "账户"
    assert browser_obj.find_element((
        By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[2]/form/div[2]/div/div[1]/div/span/span[1]/label'
    )).text == "密码"
    assert browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[2]/div[2]/label[1]'
                                     )).text == "注册用户"
    assert browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[2]/div[2]/label[2]'
                                     )).text == "忘记密码"
    assert browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[2]/button/span')).text == "登 录"


def test_login_wrong_password(browser_obj):
    browser_obj.find_element((By.XPATH, '//*/input[@id="username"]')).send_keys('admin')
    browser_obj.find_element((By.XPATH, '//*/input[@id="password"]')).send_keys('adminP@ssw1rd')
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[2]/button')).click()
    sleep(0.5)
    assert browser_obj.find_element((By.XPATH, "/html/body/div[2]/div/div/div/div/div/span[2]")).text == "密码错误"


def test_login_not_exist_user(browser_obj):
    browser_obj.find_element((By.XPATH, '//*/input[@id="username"]')).send_keys('admin1')
    browser_obj.find_element((By.XPATH, '//*/input[@id="password"]')).send_keys('adminP@ssw0rd')
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[2]/button')).click()
    sleep(0.5)
    assert browser_obj.find_element((By.XPATH, "/html/body/div[2]/div/div/div/div/div/span[2]")).text == "指定用户不存在"


@pytest.mark.run(order=2)
def test_login_password_null(browser_obj):
    browser_obj.find_element((By.XPATH, '//*/input[@id="username"]')).send_keys('admin')
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[2]/button')).click()
    sleep(0.5)
    assert browser_obj.find_element((
        By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[2]/form/div[2]/div/div[2]/div[@role="alert"]'
    )).text == "请输入密码"


@pytest.mark.run(order=1)
def test_login_user_limit(browser_obj):
    test_user = generate_string(33)
    browser_obj.find_element((By.XPATH, '//*/input[@id="username"]')).send_keys(test_user)
    sleep(0.5)
    assert browser_obj.find_element((
        By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[2]/form/div[1]/div/div[2]/div')).text == "最多32个字符"
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[2]/div[2]/label[1]')).click()
    browser_obj.find_element((By.XPATH, '//*/input[@id="username"]')).send_keys(test_user)
    logger.debug(browser_obj.find_element((
        By.XPATH, '//*[@id="root"]/div/div/div[2]/div/form/div[1]/div/div[2]/div')).text)
    sleep(0.5)
    assert browser_obj.find_element((
        By.XPATH, '//*[@id="root"]/div/div/div[2]/div/form/div[1]/div/div[2]/div'
    )).text == "用户名只能包含字母、数字、_、@，长度1-32"


def test_login_right(browser_obj, devops_config):
    browser_obj.find_element((By.XPATH, '//*/input[@id="username"]')).send_keys(devops_config['username'])
    browser_obj.find_element((By.XPATH, '//*/input[@id="password"]')).send_keys(devops_config['password'])
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[2]/button')).click()
    sleep(0.5)
    assert browser_obj.find_element((
        By.XPATH, '//*[@id="root"]/section/main/div[1]/div[1]/div[2]/div/div/div[1]/div/div[1]/label'
    )).text == "项目列表"


def test_login_ldap_right(browser_obj):
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[2]/div[1]/div[2]/label')).click()
    browser_obj.find_element((By.XPATH, '//*/input[@id="username"]')).send_keys('luochao')
    browser_obj.find_element((By.XPATH, '//*/input[@id="password"]')).send_keys('JLY123456')
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[2]/button')).click()
    sleep(0.5)
    assert browser_obj.find_element((
        By.XPATH, '//*[@id="root"]/section/main/div[1]/div[1]/div[2]/div/div/div[1]/div/div[1]/label'
    )).text == "项目列表"
