import pytest
from libs.log_obj import LogObj
from selenium.webdriver.common.by import By
from utils.times import sleep
from utils.util import generate_string
from web import arguments
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

args = arguments.parse_arg()
logger = LogObj().get_logger()


@pytest.fixture(scope='module', autouse=True)
def open_login_url(browser_obj, login_url):
    browser_obj.open_url(login_url)


def test_pandect_catalog(browser_obj):
    '''总览'''
    browser_obj.find_element((By.XPATH, '//*[@id="userName"]')).send_keys('admin')
    browser_obj.find_element((By.XPATH, '//*[@id="password"]')).send_keys('password')
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[4]/div/div/div/button')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//ul[@class="ant-menu ant-menu-root ant-menu-inline ant-menu-dark ant-pro-sider-menu"]/li[1]/span/a')).click()
    sleep(0.3)
    assert (browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div[1]')).text)[0] >"0"
    sleep(0.3)
    assert (browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div/div/div/div/div[1]/div[2]/div/div/div/div/div[1]/div[1]/div/div/div[1]')).text)[0] >"0"
    sleep(0.3)
    assert (browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div/div/div/div/div[1]/div[3]/div/div/div/div/div[1]/div[1]/div/div/div[1]')).text)[0] >"0"
    sleep(0.3)


def test_pandect_anomaly(browser_obj):
    '''异常应用'''
    wd=WebDriverWait(browser_obj.driver,10)
    if browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div/div[1]/h1/span[2]')).text == "0":
        pass
    else:
        sleep(1)
        browser_obj.find_element((By.XPATH,'//a[text()="查看详情"]')).click()
        sleep(0.3)
        browser_obj.find_element((By.XPATH,'//span[text()="返 回"]')).click()
        sleep(0.3)

    sleep(0.3)
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="ant-layout-header"]/div/div[2]/section[3]/section/span')))
    a=browser_obj.find_element((By.XPATH, '//*[@class="ant-layout-header"]/div/div[2]/section[3]/section/span'))
    ActionChains(browser_obj.driver).move_to_element(a).perform()
    sleep(1)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"退出登录")]')).click()
    sleep(1)



