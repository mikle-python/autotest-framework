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


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_offline_tasks_create_offline_tasks(browser_obj,nginx):
    '''创建离线任务'''
    browser_obj.implicitly_wait(30)
    wd=WebDriverWait(browser_obj.driver,30)
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="userName"]')))
    browser_obj.find_element((By.XPATH, '//*[@id="userName"]')).send_keys('admin')
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]')))
    browser_obj.find_element((By.XPATH, '//*[@id="password"]')).send_keys('password')
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[4]/div/div/div/button')))
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[4]/div/div/div/button')).click()
    # 点击应用管理
    wd.until(EC.visibility_of_element_located((By.XPATH, '//li[2]/div/span/span/span[2][text()="应用管理"]')))
    browser_obj.find_element((By.XPATH, '//li[2]/div/span/span/span[2][text()="应用管理"]')).click()
    # 点击离线任务
    wd.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[2]/ul/li[3]/span/a')))
    browser_obj.find_element((By.XPATH,'/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[2]/ul/li[3]/span/a')).click()
    # 点击创建离线任务
    wd.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div/div/div/header/div/div[1]/button[1]')))
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div/div/div/header/div/div[1]/button[1]')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="base_name"]')))
    browser_obj.find_element((By.XPATH,'//*[@id="base_name"]')).send_keys('nginxx01-test')
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_type"]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_type"]')).send_keys(Keys.ENTER)
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_image"]')).click()
    sleep(1)
    browser_obj.find_element((By.XPATH, '//*[@id="base_image"]')).send_keys(nginx)
    sleep(1)
    browser_obj.find_element((By.XPATH, '//*[@id="base_image"]')).send_keys(Keys.ENTER)

    sleep(3)
    browser_obj.find_element((By.XPATH, '//*[@id="base_image"]')).send_keys(Keys.TAB)
    sleep(1)
    browser_obj.find_element((By.XPATH, '//*[@id="base_imageTag"]')).send_keys(Keys.ENTER)
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_imageTag"]')).send_keys(Keys.ENTER)
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_image"]')).send_keys(Keys.TAB)
    sleep(1)
    browser_obj.find_element((By.XPATH, '//*[@id="base_imageTag"]')).send_keys(Keys.ENTER)
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_imageTag"]')).send_keys(Keys.ENTER)
    sleep(0.5)

    browser_obj.find_element((By.XPATH, '//*[@id="base_imagePullPolicy"]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_imagePullPolicy"]')).send_keys(Keys.ENTER)
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_cpuResource"]')).send_keys('100')
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_memoryResource"]')).send_keys('100')
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_gpuResource"]')).send_keys('0')
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"提 交")]')).click()
    sleep(0.5)
    assert browser_obj.find_element((By.XPATH,'/html/body/div[2]/div/div/div/div/div/span[2]')).text == "创建成功"
    sleep(0.1)


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_offline_tasks_view_details(browser_obj):
    '''搜索-查看详情'''
    wd=WebDriverWait(browser_obj.driver,30)

    wd.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="ant-input"]')))
    browser_obj.find_element((By.XPATH,'//input[@class="ant-input"]')).send_keys('xx01-tes')
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//button[@class="ant-btn ant-btn-primary ant-btn-icon-only"]')).click()
    wd.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="查看详情"]')))
    browser_obj.find_element((By.XPATH,'//span[text()="查看详情"]')).click()
    sleep(1)
    # 离线任务详情-查看处理详情
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"查看处理详情")]')).click()
    sleep(0.5)
    browser_obj.driver.refresh()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//div[contains(text(),"监控指标")]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//div[contains(text(),"应用事件")]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//div[contains(text(),"资源定义")]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//div[contains(text(),"基本信息")]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//div/button[1]/span[contains(text(),"删除任务")]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//div/div[2]/button[2]/span[text()="是"]')).click()
    sleep(0.5)
    assert browser_obj.find_element((By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')).text == "操作成功"
    sleep(0.5)


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_offline_tasks_view_details_redeplo(browser_obj,nginx):
    '''查看处理详情'''
    # 点击离线任务
    wd=WebDriverWait(browser_obj.driver,30)

    wd.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[2]/ul/li[3]/span/a')))
    browser_obj.find_element((By.XPATH,'/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[2]/ul/li[3]/span/a')).click()
    # 点击创建离线任务
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div/div/div/header/div/div[1]/button[1]')))
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div/div/div/header/div/div[1]/button[1]')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="base_name"]')))
    browser_obj.find_element((By.XPATH,'//*[@id="base_name"]')).send_keys('nginxg01-test')
    sleep(0.1)
    browser_obj.find_element((By.XPATH, '//*[@id="base_type"]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_type"]')).send_keys(Keys.ENTER)
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_image"]')).click()
    sleep(1)
    browser_obj.find_element((By.XPATH, '//*[@id="base_image"]')).send_keys(nginx)
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_image"]')).send_keys(Keys.ENTER)

    sleep(3)
    browser_obj.find_element((By.XPATH, '//*[@id="base_image"]')).send_keys(Keys.TAB)
    sleep(1)
    browser_obj.find_element((By.XPATH, '//*[@id="base_imageTag"]')).send_keys(Keys.ENTER)
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_imageTag"]')).send_keys(Keys.ENTER)
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_image"]')).send_keys(Keys.TAB)
    sleep(1)
    browser_obj.find_element((By.XPATH, '//*[@id="base_imageTag"]')).send_keys(Keys.ENTER)
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_imageTag"]')).send_keys(Keys.ENTER)
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_imagePullPolicy"]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_imagePullPolicy"]')).send_keys(Keys.ENTER)
    sleep(0.1)
    browser_obj.find_element((By.XPATH, '//*[@id="base_cpuResource"]')).send_keys('100')
    sleep(0.1)
    browser_obj.find_element((By.XPATH, '//*[@id="base_memoryResource"]')).send_keys('100')
    sleep(0.1)
    browser_obj.find_element((By.XPATH, '//*[@id="base_gpuResource"]')).send_keys('0')
    sleep(0.1)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"提 交")]')).click()
    sleep(0.5)
    assert browser_obj.find_element((By.XPATH,'/html/body/div[2]/div/div/div/div/div/span[2]')).text == "创建成功"
    sleep(0.1)
    browser_obj.find_element((By.XPATH,'//span[text()="查看处理详情"]')).click()
    sleep(0.3)
    browser_obj.driver.refresh()
    sleep(0.5)


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_offline_tasks_delete(browser_obj):
    '''删除'''
    wd=WebDriverWait(browser_obj.driver,30)

    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="删除"]')))
    browser_obj.find_element((By.XPATH,'//span[text()="删除"]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//span[text()="是"]')).click()
    sleep(0.5)
    assert browser_obj.find_element((By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')).text == "操作成功"

    sleep(0.5)
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="ant-layout-header"]/div/div[2]/section[3]/section/span')))
    akik=browser_obj.find_element((By.XPATH, '//*[@class="ant-layout-header"]/div/div[2]/section[3]/section/span'))
    ActionChains(browser_obj.driver).move_to_element(akik).perform()
    sleep(1)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"退出登录")]')).click()
    sleep(1)

