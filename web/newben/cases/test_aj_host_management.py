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
def test_host_management_status_checkout(browser_obj):
    '''主机管理-主机状态检查'''
    browser_obj.implicitly_wait(10)
    wd=WebDriverWait(browser_obj.driver,10)

    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="userName"]')))
    browser_obj.find_element((By.XPATH, '//*[@id="userName"]')).send_keys('admin')
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]')))
    browser_obj.find_element((By.XPATH, '//*[@id="password"]')).send_keys('password')
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[4]/div/div/div/button')))
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[4]/div/div/div/button')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="主机管理"]')))
    browser_obj.find_element((By.XPATH, '//span[text()="主机管理"]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[4]/ul/li/span/a')).click()
    sleep(0.1)
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[1]/td[1]/span')).click()
    sleep(0.5)
    assert browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[2]/td/div/div/div/div/ul/li/section[1]/span')).text=='正常'

    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[2]/td/div/div/div/div/ul/li/section[9]/span[2]/button[2]/span')).click()
    sleep(1)
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[2]/td/div/div/div/div/ul/li/section[9]/span[2]/button[2]/span')).click()
    sleep(0.5)


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_host_management_Modify_node(browser_obj):
    '''修改节点配置'''
    wd=WebDriverWait(browser_obj.driver,10)

    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[1]/td[3]/div/a')))
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[1]/td[3]/div/a')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="修改节点配置"]')))
    browser_obj.find_element((By.XPATH, '//span[text()="修改节点配置"]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH,'//input[@class="ant-input-number-input"]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH,'//input[@class="ant-input-number-input"]')).send_keys(Keys.BACK_SPACE)
    sleep(0.5)
    browser_obj.find_element((By.XPATH,'//input[@class="ant-input-number-input"]')).send_keys('2')
    sleep(0.5)
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="确 定"]')))
    browser_obj.find_element((By.XPATH, '//span[text()="确 定"]')).click()
    sleep(3)
    assert browser_obj.find_element((By.XPATH,'/html/body/div[2]/div/div/div/div/div/span[2]')).text == "修改成功"


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_host_management_deal_details(browser_obj):
    '''查看处理详情'''
    wd=WebDriverWait(browser_obj.driver,10)

    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[1]/td[3]/div/a')))
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[1]/td[3]/div/a')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="查看处理详情"]')))
    browser_obj.find_element((By.XPATH, '//span[text()="查看处理详情"]')).click()
    sleep(1)
    browser_obj.driver.refresh()
    sleep(3)


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_host_management_save_cost(browser_obj):
    '''节点维护'''
    wd = WebDriverWait(browser_obj.driver, 10)

    wd.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[1]/td[3]/div/a')))
    browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[1]/td[3]/div/a')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="维护"]')))
    browser_obj.find_element((By.XPATH, '//span[text()="维护"]')).click()
    sleep(2)
    assert browser_obj.find_element((By.XPATH,'/html/body/div[2]/div/div/div/div/div/span[2]')).text == "维护成功"
    sleep(2)
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[1]/td[3]/div/a')).click()
    sleep(2)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"取消维护")]')).click()
    sleep(0.5)
    assert browser_obj.find_element((By.XPATH,'/html/body/div[2]/div/div/div/div/div/span[2]')).text == "取消维护成功"
    sleep(0.5)


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_host_management_label_set(browser_obj):
    '''标签设置'''
    browser_obj.driver.refresh()
    wd=WebDriverWait(browser_obj.driver,10)

    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[1]/td[1]/span')))
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[1]/td[1]/span')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="标签设置"]')))
    browser_obj.find_element((By.XPATH, '//span[text()="标签设置"]')).click()
    sleep(1)
    browser_obj.find_element((By.XPATH, '/html/body/div/div/section/section/div/main/div/div/div/section/section/div/main/div/div[4]/div/div[2]/div/div/div[3]/div/button[2]/span')).click()
    sleep(0.5)
    assert browser_obj.find_element((By.XPATH,'/html/body/div[2]/div/div/div/div/div/span[2]')).text == "标签设置成功"


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_host_management_view_details(browser_obj):
    '''查看详情'''
    wd=WebDriverWait(browser_obj.driver,10)

    wd.until(EC.presence_of_element_located((By.XPATH, '//table/tbody/tr[2]/td/div/div/div/div/ul/li/section[9]/span[2]/a[text()="查看详情"]')))
    browser_obj.find_element((By.XPATH, '//table/tbody/tr[2]/td/div/div/div/div/ul/li/section[9]/span[2]/a[text()="查看详情"]')).click()
    sleep(2)
    a=browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div/div/div/div/div/div[2]/div[3]/div/div[1]/footer/span[2]/b')).text
    aa=a.split(' ')[0]
    assert aa > '0'
    sleep(0.3)
    b=browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div/div/div/div/div/div[2]/div[3]/div/div[2]/footer/span[2]/b')).text
    bb=b.split(' ')[0]
    assert bb > '0'
    sleep(0.3)
    c=browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div/div/div/div/div/div[2]/div[3]/div/div[3]/footer/span[2]/b')).text
    cc=c.split(' ')[0]
    assert cc > '0'
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//div[contains(text(),"节点监控")]')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//div[contains(text(),"节点事件")]')).click()
    sleep(0.3)
    assert browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div/div/div/div/div/div[2]/div/div/div/div/div/div/table/tbody/tr[1]/td[1]')).text != ""
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//div[contains(text(),"节点Box列表")]')).click()
    sleep(1)

    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="ant-layout-header"]/div/div[2]/section[3]/section/span')))
    akik=browser_obj.find_element((By.XPATH, '//*[@class="ant-layout-header"]/div/div[2]/section[3]/section/span'))
    ActionChains(browser_obj.driver).move_to_element(akik).perform()
    sleep(1)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"退出登录")]')).click()
    sleep(1)

