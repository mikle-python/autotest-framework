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
def test_space_management_create_space(browser_obj):
    '''创建工作空间'''
    browser_obj.implicitly_wait(10)
    wd=WebDriverWait(browser_obj.driver,10)

    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="userName"]')))
    browser_obj.find_element((By.XPATH, '//*[@id="userName"]')).send_keys('admin')
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]')))
    browser_obj.find_element((By.XPATH, '//*[@id="password"]')).send_keys('password')
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[4]/div/div/div/button')))
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[4]/div/div/div/button')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="空间管理"]')))
    browser_obj.find_element((By.XPATH,'//span[text()="空间管理"]')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[9]/ul/li/span/a')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="创建空间"]')))
    browser_obj.find_element((By.XPATH,'//span[text()="创建空间"]')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="name"]')))
    browser_obj.find_element((By.XPATH,'//*[@id="name"]')).send_keys('space-test')
    sleep(2)
    browser_obj.find_element((By.XPATH,'//span[text()="确 定"]')).click()
    sleep(0.3)
    assert browser_obj.find_element((By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')).text == "创建成功"


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_space_management_search_space(browser_obj):
    '''搜索工作空间'''
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//input[@class="ant-input"]')).send_keys('ace-te')
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//button[@class="ant-btn ant-btn-primary ant-btn-icon-only"]')).click()
    sleep(0.5)


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_space_management_revamp_space(browser_obj):
    '''修改工作空间'''
    browser_obj.find_element((By.XPATH,'//span[text()="修改"]')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//*[@id="description"]')).send_keys('test')
    sleep(2)
    browser_obj.find_element((By.XPATH,'//span[text()="确 定"]')).click()
    sleep(0.3)
    assert browser_obj.find_element((By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')).text == "修改成功"
    sleep(0.5)


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_space_management_delect_space(browser_obj):
    '''删除工作空间'''
    wd=WebDriverWait(browser_obj.driver,10)
    browser_obj.find_element((By.XPATH, '//input[@class="ant-input"]')).send_keys('ace-te')
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//button[@class="ant-btn ant-btn-primary ant-btn-icon-only"]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH,'//span[text()="删除"]')).click()
    sleep(2)
    browser_obj.find_element((By.XPATH,'//span[text()="是"]')).click()
    sleep(0.3)
    assert browser_obj.find_element((By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')).text == "操作成功"

    sleep(1)
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="ant-layout-header"]/div/div[2]/section[3]/section/span')))
    akik=browser_obj.find_element((By.XPATH, '//*[@class="ant-layout-header"]/div/div[2]/section[3]/section/span'))
    ActionChains(browser_obj.driver).move_to_element(akik).perform()
    sleep(1)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"退出登录")]')).click()
    sleep(1)





