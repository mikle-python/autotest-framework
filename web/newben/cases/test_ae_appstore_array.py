import pytest
from libs.log_obj import LogObj
from selenium.webdriver.common.by import By
from utils.times import sleep
from utils.util import generate_string
from web import arguments
from selenium.webdriver.support.select import Select
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
def test_appstore_array_create_application_array(browser_obj):
    '''创建应用矩阵'''
    browser_obj.implicitly_wait(30)
    wd=WebDriverWait(browser_obj.driver,30)
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="userName"]')))
    browser_obj.find_element((By.XPATH, '//*[@id="userName"]')).send_keys('admin')
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]')))
    browser_obj.find_element((By.XPATH, '//*[@id="password"]')).send_keys('password')
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[4]/div/div/div/button')))
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[4]/div/div/div/button')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="应用管理"]')))
    browser_obj.find_element((By.XPATH, '//li[2]/div/span/span/span[2][text()="应用管理"]')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[2]/ul/li[2]/span/a')))
    browser_obj.find_element((By.XPATH, '/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[2]/ul/li[2]/span/a')).click()
    # 点击创建应用规阵
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="创建应用矩阵"]')))
    browser_obj.find_element((By.XPATH, '//span[text()="创建应用矩阵"]')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="appMatrixName"]')))
    browser_obj.find_element((By.XPATH,'//*[@id="appMatrixName"]')).send_keys('matrixx-test')
    sleep(2)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"确 定")]')).click()
    sleep(0.5)

    assert browser_obj.find_element((By.XPATH,'/html/body/div[2]/div/div/div/div/div/span[2]')).text == "创建成功"


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_appstore_array_view_details(browser_obj,nginx):
    '''搜索-查看详情-创建应用'''
    wd=WebDriverWait(browser_obj.driver,30)

    wd.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="ant-input"]')))
    browser_obj.find_element((By.XPATH,'//input[@class="ant-input"]')).send_keys('rixx-te')
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//button[@class="ant-btn ant-btn-primary ant-btn-icon-only"]')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="ant-table-content"]/table/tbody/tr/td[4]/div/a')))
    browser_obj.find_element((By.XPATH, '//div[@class="ant-table-content"]/table/tbody/tr/td[4]/div/a')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[contains(text(),"查看详情")]')))
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"查看详情")]')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="创建应用"]')))
    browser_obj.find_element((By.XPATH, '//span[text()="创建应用"]')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="base_applicationName"]')))
    browser_obj.find_element((By.XPATH,'//*[@id="base_applicationName"]')).send_keys('nginxx01-test')
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_type"]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_type"]')).send_keys(Keys.ENTER)
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_image"]')).click()
    sleep(1)
    browser_obj.find_element((By.XPATH, '//*[@id="base_image"]')).send_keys(nginx)
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_image"]')).send_keys(Keys.ENTER)
    sleep(0.5)
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
def test_appstore_array_matrix_details(browser_obj):
    '''应用矩阵-矩阵详情'''
    wd=WebDriverWait(browser_obj.driver,30)

    wd.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="ant-input"]')))
    browser_obj.find_element((By.XPATH,'//input[@class="ant-input"]')).send_keys('xx01-te')
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//button[@class="ant-btn ant-btn-primary ant-btn-icon-only"]')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="查看处理详情"]')))
    browser_obj.find_element((By.XPATH, '//span[text()="查看处理详情"]')).click()
    sleep(1)
    browser_obj.driver.refresh()
    sleep(0.5)
    browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/table/tbody/tr/td[6]/div/a')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//span[text()="查看详情"]')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="返 回"]')))
    browser_obj.find_element((By.XPATH, '//span[text()="返 回"]')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/table/tbody/tr/td[6]/div/a')))
    browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/table/tbody/tr/td[6]/div/a')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="查看处理详情"]')))
    browser_obj.find_element((By.XPATH, '//span[text()="查看处理详情"]')).click()
    sleep(1)
    browser_obj.driver.refresh()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/table/tbody/tr/td[6]/div/a')))
    browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/table/tbody/tr/td[6]/div/a')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="修改应用"]')))
    browser_obj.find_element((By.XPATH, '//span[text()="修改应用"]')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//div[text()="副本设置(必填)"]')))
    browser_obj.find_element((By.XPATH, '//div[text()="副本设置(必填)"]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="copy_replicas"]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="copy_replicas"]')).send_keys(Keys.BACK_SPACE)
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="copy_replicas"]')).send_keys('2')
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//span[text()="提 交"]')).click()
    sleep(0.5)
    wd.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/table/tbody/tr/td[6]/div/a')))
    browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/table/tbody/tr/td[6]/div/a')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//span[text()="删除"]')).click()
    sleep(3)
    browser_obj.find_element((By.XPATH, '//span[text()="是"]')).click()
    sleep(0.5)
    assert browser_obj.find_element((By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')).text == "操作成功"
    sleep(1)
    browser_obj.find_element((By.XPATH, '/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[2]/ul/li[2]/span/a')).click()


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_appstore_array_view_details_redeplo(browser_obj):
    '''查看处理详情'''
    sleep(0.5)
    browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[1]/td[4]/div/a')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//span[text()="查看处理详情"]')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//button[@class="ant-drawer-close"]')).click()
    sleep(0.1)


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_appstore_array_amend_application(browser_obj,nginx):
    '''修改应用矩阵'''
    browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[1]/td[4]/div/a')).click()
    sleep(0.1)
    browser_obj.find_element((By.XPATH, '//span[text()="修改应用矩阵"]')).click()
    sleep(0.1)
    browser_obj.find_element((By.XPATH,'//*[@id="matrix-sortable"]/div[1]/button')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH,'//*[@id="base_applicationName"]')).send_keys('nginx01-test')
    sleep(0.5)
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
    sleep(1)
    browser_obj.find_element((By.XPATH, '//*[@id="base_image"]')).send_keys(Keys.TAB)
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_imageTag"]')).send_keys(Keys.ENTER)
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_imageTag"]')).send_keys(Keys.ENTER)
    sleep(0.5)

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
    browser_obj.find_element((By.XPATH, '//*[@id="matrix-sortable"]/div[2]/div[2]/div/div[2]/div[2]/div/footer/button[2]')).click()
    sleep(1)
    # 点击确定
    browser_obj.find_element((By.XPATH, '//span[text()="确 定"]')).click()

@pytest.mark.flaky(retun=3,runs_delay=2)
def test_appstore_array_delete_application(browser_obj):
    '''删除应用矩阵'''
    wd=WebDriverWait(browser_obj.driver,30)
    sleep(0.5)
    browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[1]/td[4]/div/a')).click()
    sleep(0.1)
    browser_obj.find_element((By.XPATH, '//span[text()="删除"]')).click()
    sleep(3)
    browser_obj.find_element((By.XPATH, '//span[text()="是"]')).click()
    sleep(1)
    assert browser_obj.find_element((By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')).text == "操作成功"

    sleep(0.3)
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="ant-layout-header"]/div/div[2]/section[3]/section/span')))
    akik=browser_obj.find_element((By.XPATH, '//*[@class="ant-layout-header"]/div/div[2]/section[3]/section/span'))
    ActionChains(browser_obj.driver).move_to_element(akik).perform()
    sleep(1)
    browser_obj.find_element((By.XPATH, '//span[text()="退出登录"]')).click()
    sleep(1)




