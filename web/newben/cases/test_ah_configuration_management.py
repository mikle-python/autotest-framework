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
def test_configuration_management_Increase_configuration(browser_obj):
    '''配置管理'''
    wd=WebDriverWait(browser_obj.driver,30)

    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="userName"]')))
    browser_obj.find_element((By.XPATH, '//*[@id="userName"]')).send_keys('admin')
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]')))
    browser_obj.find_element((By.XPATH, '//*[@id="password"]')).send_keys('password')
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[4]/div/div/div/button')))
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[4]/div/div/div/button')).click()
    # 点击应用管理
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="应用管理"]')))
    browser_obj.find_element((By.XPATH, '//span[text()="应用管理"]')).click()
    # 点击配置管理
    wd.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/section/section/div/main/div/div/div/section/aside/div/ul/li[2]/ul/li[5]/span/a')))
    browser_obj.find_element((By.XPATH, '/html/body/div/div/section/section/div/main/div/div/div/section/aside/div/ul/li[2]/ul/li[5]/span/a')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="增加配置"]')))
    browser_obj.find_element((By.XPATH, '//span[text()="增加配置"]')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//span[@class="anticon anticon-close-circle ant-input-clear-icon"]')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//*[@id="name"]')).send_keys('config-test')
    sleep(2)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"确 定")]')).click()
    sleep(0.3)
    assert browser_obj.find_element((By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')).text == "创建成功"


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_configuration_management_Modify_configuration(browser_obj):
    '''修改配置'''
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"修改配置")]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//span[contains(text()," 添加配置")]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '/html/body/div[1]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[2]/div/div[2]/div/div/div[2]/form/div[1]/div/div/div[2]/div[2]/div/div/div/div[1]/div[1]/div/div[1]/span/div/div/div[1]/div/span/input')).send_keys('MYSQL_ROOT_PASSWORD')
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '/html/body/div[1]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[2]/div/div[2]/div/div/div[2]/form/div[1]/div/div/div[2]/div[2]/div/div/div/div[1]/div[1]/div/div[2]/div/div/div[1]/div/span/textarea')).send_keys('123456')
    sleep(2)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"确 定")]')).click()
    sleep(0.1)
    assert browser_obj.find_element((By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')).text == "修改成功"


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_configuration_management_search_configuration(browser_obj):
    '''搜索配置'''
    wd=WebDriverWait(browser_obj.driver,30)
    sleep(0.3)
    wd.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="ant-input"]')))
    browser_obj.find_element((By.XPATH, '//input[@class="ant-input"]')).send_keys('config-test')
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//button[@class="ant-btn ant-btn-primary ant-btn-icon-only"]')).click()
    sleep(0.5)
    assert browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr/td[1]/div/div[1]')).text == "config-test"


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_configuration_management_delete(browser_obj):
    '''删除配置'''
    wd=WebDriverWait(browser_obj.driver,30)
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"删除")]')).click()
    sleep(3)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"是")]')).click()
    sleep(0.5)
    assert browser_obj.find_element((By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')).text == "操作成功"

    sleep(1)
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="ant-layout-header"]/div/div[2]/section[3]/section/span')))
    akik=browser_obj.find_element((By.XPATH, '//*[@class="ant-layout-header"]/div/div[2]/section[3]/section/span'))
    ActionChains(browser_obj.driver).move_to_element(akik).perform()
    sleep(1)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"退出登录")]')).click()
    sleep(1)