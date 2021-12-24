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
def test_timed_task_create_timed_task(browser_obj):
    '''创建定时任务'''
    browser_obj.implicitly_wait(30)
    wd=WebDriverWait(browser_obj.driver,30)

    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="userName"]')))
    browser_obj.find_element((By.XPATH, '//*[@id="userName"]')).send_keys('admin')
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]')))
    browser_obj.find_element((By.XPATH, '//*[@id="password"]')).send_keys('password')
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[4]/div/div/div/button')))
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[4]/div/div/div/button')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="应用管理"]')))
    browser_obj.find_element((By.XPATH,'//span[text()="应用管理"]')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[2]/ul/li[4]/span/a')))
    browser_obj.find_element((By.XPATH, '/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[2]/ul/li[4]/span/a')).click()
    sleep(0.5)


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_timed_task_view_details(browser_obj):
    '''搜索-查看详情'''
    wd=WebDriverWait(browser_obj.driver,30)

    wd.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="ant-input"]')))
    browser_obj.find_element((By.XPATH,'//input[@class="ant-input"]')).send_keys('xx01-te')
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//button[@class="ant-btn ant-btn-primary ant-btn-icon-only"]')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr/td[5]/div/a')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH,'//span[text()="查看详情"]')).click()
    sleep(1)
    browser_obj.find_element((By.XPATH,'//span[text()="查看处理详情"]')).click()
    sleep(0.5)
    browser_obj.driver.refresh()

    while browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/div/div/div/table/tbody/tr[1]/td[3]')).text!='running':
        browser_obj.driver.refresh()
        sleep(2)

    browser_obj.find_element((By.XPATH,'//span[text()="查看详情"]')).click()
    sleep(1)
    browser_obj.driver.refresh()
    sleep(1)
    assert browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div[1]/div[1]/div[1]/div[3]/span')).text == 'running'
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//span[text()="查看处理详情"]')).click()
    sleep(0.3)
    browser_obj.driver.refresh()
    sleep(0.5)
    browser_obj.find_element((By.XPATH,'//span[text()="日志"]')).click()
    sleep(3)
    nu=browser_obj.driver.window_handles
    browser_obj.driver.switch_to.window(nu[1])
    sleep(2)
    browser_obj.driver.switch_to.window(nu[0])
    sleep(2)
    browser_obj.find_element((By.XPATH,'//span[text()="控制台"]')).click()
    sleep(3)
    browser_obj.driver.switch_to.window(nu[0])
    sleep(1)
    browser_obj.find_element((By.XPATH,'//div[contains(text(),"应用事件")]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH,'//div[contains(text(),"资源定义")]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH,'//div[contains(text(),"基本信息")]')).click()
    sleep(0.5)
    browser_obj.driver.refresh()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//span[text()="删除任务"]')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//span[text()="是"]')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="删除"]')))
    browser_obj.find_element((By.XPATH,'//span[text()="删除"]')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//span[text()="是"]')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//div[text()="应用事件"]')))
    browser_obj.find_element((By.XPATH,'//div[text()="应用事件"]')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//div[text()="资源定义"]')))
    browser_obj.find_element((By.XPATH,'//div[text()="资源定义"]')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="返 回"]')))
    browser_obj.find_element((By.XPATH,'//span[text()="返 回"]')).click()
    sleep(0.5)


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_timed_task_view_details_redeplo(browser_obj):
    '''查看处理详情'''
    wd=WebDriverWait(browser_obj.driver,30)

    wd.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr/td[5]/div/a')))
    browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr/td[5]/div/a')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH,'//span[contains(text(),"查看处理详情")]')).click()
    sleep(0.5)
    browser_obj.driver.refresh()
    sleep(0.5)


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_timed_task_suspended_task(browser_obj):
    '''暂停任务'''
    wd=WebDriverWait(browser_obj.driver,30)

    wd.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr/td[5]/div/a')))
    browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr/td[5]/div/a')).click()
    wd.until(EC.presence_of_element_located((By.XPATH, '//span[text()="暂停任务"]')))
    browser_obj.find_element((By.XPATH,'//span[text()="暂停任务"]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH,'//span[contains(text(),"是")]')).click()
    sleep(0.5)


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_timed_task_amend_task(browser_obj):
    '''修改'''
    wd=WebDriverWait(browser_obj.driver,30)

    wd.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr/td[5]/div/a')))
    browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr/td[5]/div/a')).click()
    wd.until(EC.presence_of_element_located((By.XPATH, '//span[text()="修改"]')))
    browser_obj.find_element((By.XPATH,'//span[text()="修改"]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_memoryResource"]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_memoryResource"]')).send_keys(Keys.BACK_SPACE)
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_memoryResource"]')).send_keys(Keys.BACK_SPACE)
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_memoryResource"]')).send_keys(Keys.BACK_SPACE)
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_memoryResource"]')).send_keys('100')
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//span[text()="提 交"]')).click()
    sleep(0.5)


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_timed_task_delete(browser_obj):
    '''删除'''
    wd=WebDriverWait(browser_obj.driver,30)

    wd.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr/td[5]/div/a')))
    browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr/td[5]/div/a')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="删除"]')))
    browser_obj.find_element((By.XPATH,'//span[text()="删除"]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//span[text()="是"]')).click()

    sleep(1)
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="ant-layout-header"]/div/div[2]/section[3]/section/span')))
    akik=browser_obj.find_element((By.XPATH, '//*[@class="ant-layout-header"]/div/div[2]/section[3]/section/span'))
    ActionChains(browser_obj.driver).move_to_element(akik).perform()
    sleep(1)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"退出登录")]')).click()
    sleep(1)