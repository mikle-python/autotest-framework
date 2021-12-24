import pytest
from libs.log_obj import LogObj
from selenium.webdriver.common.by import By
from utils.times import sleep
from utils.util import generate_string
from web import arguments
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

args = arguments.parse_arg()
logger = LogObj().get_logger()


@pytest.fixture(scope='module', autouse=True)
def open_login_url(browser_obj, login_url):
    browser_obj.open_url(login_url)


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_log_incident(browser_obj):
    '''日志管理-日志检查'''
    browser_obj.implicitly_wait(20)
    wd=WebDriverWait(browser_obj.driver,10)

    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="userName"]')))
    browser_obj.find_element((By.XPATH, '//*[@id="userName"]')).send_keys('admin')
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]')))
    browser_obj.find_element((By.XPATH, '//*[@id="password"]')).send_keys('password')
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[4]/div/div/div/button')))
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[4]/div/div/div/button')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="日志管理"]')))
    browser_obj.find_element((By.XPATH, '//span[text()="日志管理"]')).click()
    sleep(0.1)
    browser_obj.find_element((By.XPATH, '/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[3]/ul/li[1]/span/a')).click()


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_log_incident_inspect(browser_obj):
    '''查询管理'''
    wd=WebDriverWait(browser_obj.driver,10)
    wd.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[3]/ul/li[1]/span/a')))
    browser_obj.find_element((By.XPATH, '/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[3]/ul/li[1]/span/a')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="componentName"]')))
    browser_obj.find_element((By.XPATH, '//*[@id="componentName"]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="componentName"]')).send_keys('newben')
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//*[@id="componentName"]')).send_keys(Keys.ENTER)
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"查 询")]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"重 置")]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="workerName"]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="workerName"]')).send_keys(Keys.ENTER)
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"查 询")]')).click()
    sleep(1)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"重 置")]')).click()
    sleep(0.3)

    browser_obj.find_element((By.XPATH, '//*[@id="level"]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="level"]')).send_keys(Keys.DOWN)
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//*[@id="level"]')).send_keys(Keys.DOWN)
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//*[@id="level"]')).send_keys(Keys.DOWN)
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//*[@id="level"]')).send_keys(Keys.ENTER)
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"查 询")]')).click()
    sleep(1)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"重 置")]')).click()
    sleep(0.5)
    assert browser_obj.find_element((By.XPATH, '//*[@id="workerName"]')).text == ""

    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="date"]')).send_keys('2021-11-03 16:56:24')
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div[1]/div/div[4]/div/div[2]/div/div/div/div[3]/input')).send_keys('2021-12-23 19:56:40')
    sleep(1)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"查 询")]')).click()
    sleep(1)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"重 置")]')).click()
    sleep(0.5)


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_log_incident_auditing(browser_obj):
    '''审计日志检查'''
    sleep(0.5)
    browser_obj.find_element((By.XPATH,'/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[3]/ul/li[2]/span/a')).click()
    sleep(0.5)
    assert browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/article/div/div/div/div/div/div/table/tbody/tr[1]/td[2]')).text != ''


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_log_incident_operation(browser_obj):
    '''操作行为搜索'''
    wd=WebDriverWait(browser_obj.driver,10)

    wd.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[3]/ul/li[2]/span/a')))
    browser_obj.find_element((By.XPATH,'/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[3]/ul/li[2]/span/a')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH,'//*[@id="action"]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH,'//*[@id="action"]')).send_keys(Keys.ENTER)
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"查 询")]')).click()
    sleep(0.5)
    a=browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/article/header/form/div/div[2]/div/div[2]/div/div/div/div/span[2]')).text
    sleep(0.5)
    b=browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/article/div/div/div/div/div/div/table/tbody/tr[1]/td[3]/div/div')).text
    sleep(0.5)
    assert a==b
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"重 置")]')).click()


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_log_incident_account_search(browser_obj):
    '''查询操作账号'''
    sleep(0.5)
    browser_obj.find_element((By.XPATH,'/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[3]/ul/li[2]/span/a')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH,'//*[@id="user_name"]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH,'//*[@id="user_name"]')).send_keys(Keys.ENTER)
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"查 询")]')).click()
    sleep(1)
    assert browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/article/div/div/div/div/div/div/table/tbody/tr[1]/td[2]')).text != ''
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"重 置")]')).click()


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_log_incident_data_search(browser_obj):
    '''查询日期搜索'''
    wd=WebDriverWait(browser_obj.driver,10)
    sleep(0.5)
    browser_obj.find_element((By.XPATH,'/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[3]/ul/li[2]/span/a')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="searchTime"]')).send_keys('2021-11-03 16:56:24')
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div/div/article/header/form/div/div[3]/div/div[2]/div/div/div/div[3]/input')).send_keys('2021-12-23 19:56:40')
    sleep(1)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"查 询")]')).click()
    sleep(1)
    assert browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/article/div/div/div/div/div/div/table/tbody/tr[1]/td[1]/div/div[1]')).text != ''
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"重 置")]')).click()

    sleep(1)
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="ant-layout-header"]/div/div[2]/section[3]/section/span')))
    akik=browser_obj.find_element((By.XPATH, '//*[@class="ant-layout-header"]/div/div[2]/section[3]/section/span'))
    ActionChains(browser_obj.driver).move_to_element(akik).perform()
    sleep(1)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"退出登录")]')).click()
    sleep(1)


