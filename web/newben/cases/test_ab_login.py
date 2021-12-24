import pytest
from libs.log_obj import LogObj
from selenium.webdriver.common.by import By
from utils.times import sleep
from utils.util import generate_string
from web import arguments
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

args = arguments.parse_arg()
logger = LogObj().get_logger()


@pytest.fixture(scope='function', autouse=True)
def open_login_url(browser_obj, login_url):
    browser_obj.open_url(login_url)


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_login_wrong_password(browser_obj):
    browser_obj.implicitly_wait(10)
    browser_obj.find_element((By.XPATH, '//*[@id="userName"]')).send_keys('admin')
    browser_obj.find_element((By.XPATH, '//*[@id="password"]')).send_keys('adminP@ssw1rd')
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[4]/div/div/div/button')).click()

    assert browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[1]/div/div[1]')).text == "密码错误"


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_login_not_exist_user(browser_obj):
    browser_obj.find_element((By.XPATH, '//*[@id="userName"]')).send_keys('admin1')
    browser_obj.find_element((By.XPATH, '//*[@id="password"]')).send_keys('adminP@ssw0rd')
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[4]/div/div/div/button')).click()
    sleep(0.1)
    assert browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[1]/div/div[1]')).text == "用户不存在"


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_login_password_null(browser_obj):
    wd=WebDriverWait(browser_obj.driver,30)
    browser_obj.find_element((By.XPATH, '//*[@id="userName"]')).send_keys('admin')
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[4]/div/div/div/button')).click()
    sleep(0.1)
    wd.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[3]/div/div[2]/div')))
    assert browser_obj.find_element((
        By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[3]/div/div[2]/div'
    )).text == "请输入密码"


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_login_right(browser_obj):
    wd=WebDriverWait(browser_obj.driver,30)
    browser_obj.find_element((By.XPATH, '//*[@id="userName"]')).send_keys('admin')
    browser_obj.find_element((By.XPATH, '//*[@id="password"]')).send_keys('password')
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[4]/div/div/div/button')).click()
    sleep(0.1)
    wd.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div/section/h1/span')))
    assert browser_obj.find_element((
        By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div/section/h1/span'
    )).text == "总览"


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_login_right_ldap(browser_obj):
    browser_obj.implicitly_wait(10)
    wd=WebDriverWait(browser_obj.driver,30)

    wd.until(EC.presence_of_element_located((By.XPATH, '//span[text()="用户管理"]')))
    browser_obj.find_element((By.XPATH,'//span[text()="用户管理"]')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[7]/ul/li/span/a')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//span[text()="创建用户"]')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="username"]')).send_keys('testbu')
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="password"]')).send_keys('123456')
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="confPassword"]')).send_keys('123456')
    sleep(2)
    browser_obj.find_element((By.XPATH,'//span[text()="提 交"]')).click()
    sleep(0.3)
    assert browser_obj.find_element((By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')).text == "创建用户成功"

    sleep(1)
    a=browser_obj.find_element((By.XPATH, '//*[@class="ant-layout-header"]/div/div[2]/section[3]/section/span'))
    ActionChains(browser_obj.driver).move_to_element(a).perform()
    sleep(1)
    browser_obj.find_element((By.XPATH, '//span[text()="退出登录"]')).click()
    sleep(1)

    wd.until(EC.presence_of_element_located((By.XPATH, '//*[@id="userName"]')))
    browser_obj.find_element((By.XPATH, '//*[@id="userName"]')).send_keys('testbu')
    browser_obj.find_element((By.XPATH, '//*[@id="password"]')).send_keys('123456')
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[4]/div/div/div/button')).click()

    sleep(1)
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="ant-layout-header"]/div/div[2]/section[3]/section/span')))
    akik=browser_obj.find_element((By.XPATH, '//*[@class="ant-layout-header"]/div/div[2]/section[3]/section/span'))
    ActionChains(browser_obj.driver).move_to_element(akik).perform()
    sleep(1)
    browser_obj.find_element((By.XPATH, '//span[text()="退出登录"]')).click()
    sleep(1)

    wd.until(EC.presence_of_element_located((By.XPATH, '//*[@id="userName"]')))
    browser_obj.find_element((By.XPATH, '//*[@id="userName"]')).send_keys('admin')
    browser_obj.find_element((By.XPATH, '//*[@id="password"]')).send_keys('password')
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[4]/div/div/div/button')).click()

    wd.until(EC.presence_of_element_located((By.XPATH, '//span[text()="用户管理"]')))
    browser_obj.find_element((By.XPATH,'//span[text()="用户管理"]')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[7]/ul/li/span/a')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//a[text()="删除"]')).click()
    sleep(3)
    browser_obj.find_element((By.XPATH,'//span[text()="确 定"]')).click()
    sleep(0.3)
    wd.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')))
    assert browser_obj.find_element((By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')).text == "操作成功"

    sleep(1)
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="ant-layout-header"]/div/div[2]/section[3]/section/span')))
    akik=browser_obj.find_element((By.XPATH, '//*[@class="ant-layout-header"]/div/div[2]/section[3]/section/span'))
    ActionChains(browser_obj.driver).move_to_element(akik).perform()
    sleep(1)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"退出登录")]')).click()
    sleep(1)


