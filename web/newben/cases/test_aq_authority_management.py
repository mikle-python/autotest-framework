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


def test_test_authority_management_create_user(browser_obj):
    '''创建角色'''
    browser_obj.implicitly_wait(10)
    wd=WebDriverWait(browser_obj.driver,10)

    wd.until(EC.presence_of_element_located((By.XPATH, '//*[@id="userName"]')))
    browser_obj.find_element((By.XPATH, '//*[@id="userName"]')).send_keys('admin')
    wd.until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
    browser_obj.find_element((By.XPATH, '//*[@id="password"]')).send_keys('password')
    wd.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[4]/div/div/div/button')))
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[4]/div/div/div/button')).click()
    wd.until(EC.presence_of_element_located((By.XPATH, '//span[text()="权限管理"]')))
    browser_obj.find_element((By.XPATH,'//span[text()="权限管理"]')).click()
    wd.until(EC.presence_of_element_located((By.XPATH, '//ul[@class="ant-menu ant-menu-root ant-menu-inline ant-menu-dark ant-pro-sider-menu"]/li[8]/ul/li[2]/span/a')))
    browser_obj.find_element((By.XPATH,'//ul[@class="ant-menu ant-menu-root ant-menu-inline ant-menu-dark ant-pro-sider-menu"]/li[8]/ul/li[2]/span/a')).click()
    wd.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="创建角色"]')))
    browser_obj.find_element((By.XPATH,'//span[text()="创建角色"]')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="name"]')).send_keys('network-test')
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[2]/div/div[2]/div/div/div[2]/div/div/div/form/div[4]/div/div/div/div[3]/div/div/div/div[1]/span[3]/span')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[2]/div/div[2]/div/div/div[2]/div/div/div/form/div[4]/div/div/div/div[3]/div/div/div/div[2]/span[3]/span')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[2]/div/div[2]/div/div/div[2]/div/div/div/form/div[4]/div/div/div/div[3]/div/div/div/div[3]/span[3]/span')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[2]/div/div[2]/div/div/div[2]/div/div/div/form/div[4]/div/div/div/div[3]/div/div/div/div[4]/span[3]/span')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[2]/div/div[2]/div/div/div[2]/div/div/div/form/div[4]/div/div/div/div[3]/div/div/div/div[5]/span[3]/span')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[2]/div/div[2]/div/div/div[2]/div/div/div/form/div[4]/div/div/div/div[3]/div/div/div/div[6]/span[3]/span')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[2]/div/div[2]/div/div/div[2]/div/div/div/form/div[4]/div/div/div/div[3]/div/div/div/div[7]/span[3]/span')).click()
    sleep(3)
    browser_obj.find_element((By.XPATH,'//span[text()="确 定"]')).click()
    sleep(0.3)
    assert browser_obj.find_element((By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')).text == "创建成功"


def test_authority_management_search_networks(browser_obj):
    '''搜索角色'''
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//input[@class="ant-input"]')).send_keys('work-te')
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//button[@class="ant-btn ant-btn-primary ant-btn-icon-only"]')).click()
    sleep(0.5)


def test_authority_management_revamp_networks(browser_obj):
    '''修改角色'''
    sleep(0.5)
    browser_obj.find_element((By.XPATH,'//span[text()="修改"]')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="comment"]')).send_keys('test')
    sleep(2)
    browser_obj.find_element((By.XPATH,'//span[text()="确 定"]')).click()
    sleep(0.3)
    assert browser_obj.find_element((By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')).text == "修改成功"
    sleep(0.5)


def test_authority_management_delect_networks(browser_obj):
    '''删除角色'''
    browser_obj.find_element((By.XPATH, '//input[@class="ant-input"]')).send_keys('work-te')
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//button[@class="ant-btn ant-btn-primary ant-btn-icon-only"]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH,'//span[text()="删除"]')).click()
    sleep(3)
    browser_obj.find_element((By.XPATH,'//span[text()="是"]')).click()
    sleep(0.3)
    assert browser_obj.find_element((By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')).text == "操作成功"


def test_authority_management_cearte_authorization(browser_obj):
    '''创建授权'''
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//ul[@class="ant-menu ant-menu-root ant-menu-inline ant-menu-dark ant-pro-sider-menu"]/li[8]/ul/li[1]/span/a')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//span[text()="创建授权"]')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="name"]')).send_keys('rolebinding-test')
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="type"]/label[1]/span[1]/input')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="objects_user"]')).send_keys('tester')
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="roles_superRole"]')).send_keys('global')
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//span[text()="确 定"]')).click()
    sleep(0.3)
    assert browser_obj.find_element((By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')).text == "创建成功"
    sleep(0.5)


def test_authority_management_search_authorization(browser_obj):
    '''搜索授权'''
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//input[@class="ant-input"]')).send_keys('ding-te')
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//button[@class="ant-btn ant-btn-primary ant-btn-icon-only"]')).click()
    sleep(0.5)


def test_authority_management_revamp_authorization(browser_obj):
    '''修改授权'''
    browser_obj.find_element((By.XPATH,'//span[text()="修改"]')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="comment"]')).send_keys('test')
    sleep(2)
    browser_obj.find_element((By.XPATH,'//span[text()="确 定"]')).click()
    sleep(0.3)
    assert browser_obj.find_element((By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')).text == "修改成功"
    sleep(0.5)


def test_authority_management_delect_authorization(browser_obj):
    '''删除授权'''
    wd=WebDriverWait(browser_obj.driver,10)
    browser_obj.find_element((By.XPATH, '//input[@class="ant-input"]')).send_keys('ding-te')
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//button[@class="ant-btn ant-btn-primary ant-btn-icon-only"]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH,'//span[text()="删除"]')).click()
    sleep(3)
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





