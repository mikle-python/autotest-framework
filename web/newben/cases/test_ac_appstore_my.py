import time
import pytest
from libs.log_obj import LogObj
from selenium.webdriver.common.by import By
from utils.times import sleep
from time import sleep
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
def test_appstore_my_create_application(browser_obj, nginx):
    '''我的应用'''
    browser_obj.implicitly_wait(20)
    wd=WebDriverWait(browser_obj.driver,30)

    wd.until(EC.presence_of_element_located((By.XPATH, '//*[@id="userName"]')))
    browser_obj.find_element((By.XPATH, '//*[@id="userName"]')).send_keys('admin')
    wd.until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
    browser_obj.find_element((By.XPATH, '//*[@id="password"]')).send_keys('password')
    wd.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[4]/div/div/div/button')))
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[4]/div/div/div/button')).click()
    # 创建定时任务
    wd.until(EC.presence_of_element_located((By.XPATH, '//span[text()="应用管理"]')))
    browser_obj.find_element((By.XPATH,'//span[text()="应用管理"]')).click()
    wd.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[2]/ul/li[4]/span/a')))
    browser_obj.find_element((By.XPATH, '/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[2]/ul/li[4]/span/a')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="创建定时任务"]')))
    browser_obj.find_element((By.XPATH, '//span[text()="创建定时任务"]')).click()
    wd.until(EC.presence_of_element_located((By.XPATH, '//*[@id="base_cronMissionName"]')))
    browser_obj.find_element((By.XPATH, '//*[@id="base_cronMissionName"]')).send_keys('anginxx01-test')
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
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_image"]')).send_keys(Keys.TAB)
    sleep(1)
    browser_obj.find_element((By.XPATH, '//*[@id="base_imageTag"]')).send_keys(Keys.ENTER)
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_imageTag"]')).send_keys(Keys.ENTER)
    sleep(0.5)

    browser_obj.find_element((By.XPATH, '//*[@id="base_imagePullPolicy"]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_imagePullPolicy"]')).send_keys(Keys.DOWN)
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_imagePullPolicy"]')).send_keys(Keys.ENTER)
    sleep(0.1)
    browser_obj.find_element((By.XPATH, '//*[@id="base_cpuResource"]')).send_keys('100')
    sleep(0.1)
    browser_obj.find_element((By.XPATH, '//*[@id="base_memoryResource"]')).send_keys('100')
    sleep(0.1)
    browser_obj.find_element((By.XPATH, '//*[@id="base_cronExpression"]')).send_keys('*/1 * * * *')
    sleep(0.1)
    browser_obj.find_element((By.XPATH, '//*[@id="base_concurrencyPolicy"]')).click()
    sleep(0.1)
    browser_obj.find_element((By.XPATH, '//*[@id="base_concurrencyPolicy"]')).send_keys(Keys.ENTER)
    sleep(0.1)
    browser_obj.find_element((By.XPATH, '//*[@id="base_gpuResource"]')).send_keys('0')
    sleep(0.1)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"提 交")]')).click()

    wd.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')))
    assert browser_obj.find_element((By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')).text == "创建成功"

    wd.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[2]/ul/li[1]/span/a')))
    browser_obj.find_element((By.XPATH,'/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[2]/ul/li[1]/span/a')).click()
    # 点击创建应用
    wd.until(EC.presence_of_element_located((By.XPATH, '//span[text()="创建应用"]')))
    browser_obj.find_element((By.XPATH, '//span[text()="创建应用"]')).click()
    # 输入详细数据
    wd.until(EC.presence_of_element_located((By.XPATH, '//*[@id="base_applicationName"]')))
    browser_obj.find_element((By.XPATH, '//*[@id="base_applicationName"]')).send_keys("nginx-test001")
    # 镜像类型
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_type"]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_type"]')).send_keys(Keys.ENTER)
    # 镜像名称
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
    # 镜像拉取策略
    browser_obj.find_element((By.XPATH, '//*[@id="base_imagePullPolicy"]')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//*[@id="base_imagePullPolicy"]')).send_keys(Keys.DOWN)
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//*[@id="base_imagePullPolicy"]')).send_keys(Keys.ENTER)
    sleep(0.3)
    # CPU核数(毫核)
    browser_obj.find_element((By.XPATH, '//*[@id="base_cpuResource"]')).send_keys("100")
    sleep(0.3)
    # 内存容量(M)
    browser_obj.find_element((By.XPATH, '//*[@id="base_memoryResource"]')).send_keys("100")
    sleep(0.5)
    # 点击提交
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[2]/div/div[2]/div/div/div[2]/div/div/div/footer/button[2]/span')).click()
    wd.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')))

    assert browser_obj.find_element((By.XPATH,'/html/body/div[2]/div/div/div/div/div/span[2]')).text == "创建成功"


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_appstore_my_view_details(browser_obj):
    '''搜索——查看详情'''
    wd=WebDriverWait(browser_obj.driver,30)
    sleep(0.5)
    wd.until(EC.presence_of_element_located((By.XPATH, '//input[@class="ant-input"]')))
    browser_obj.find_element((By.XPATH,'//input[@class="ant-input"]')).send_keys("nx-tes")
    wd.until(EC.presence_of_element_located((By.XPATH, '//button[@class="ant-btn ant-btn-primary ant-btn-icon-only"]')))
    browser_obj.find_element((By.XPATH,'//button[@class="ant-btn ant-btn-primary ant-btn-icon-only"]')).click()
    wd.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[1]/td[6]/div/a')))
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[1]/td[6]/div/a')).click()
    wd.until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(),"查看详情")]')))
    browser_obj.find_element((By.XPATH,'//span[contains(text(),"查看详情")]')).click()
    wd.until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(),"暴露应用")]')))
    browser_obj.find_element((By.XPATH,'//span[contains(text(),"暴露应用")]')).click()
    wd.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/section/section/div/main/div/div/div/section/section/div/main/div/div[4]/div/div[2]/div/div/div[2]/form/div[3]/div[2]/div/div/div/div/div[2]/div/div/div[1]/div[1]/div/div[2]/div/div/div[1]/div/div/div[2]/input')))
    browser_obj.find_element((By.XPATH, '/html/body/div/div/section/section/div/main/div/div/div/section/section/div/main/div/div[4]/div/div[2]/div/div/div[2]/form/div[3]/div[2]/div/div/div/div/div[2]/div/div/div[1]/div[1]/div/div[2]/div/div/div[1]/div/div/div[2]/input')).send_keys("80")
    wd.until(EC.presence_of_element_located((By.XPATH, '//span[text()="确 定"]')))
    browser_obj.find_element((By.XPATH,'//span[text()="确 定"]')).click()
    time.sleep(8)
    browser_obj.driver.refresh()
    time.sleep(3)
    while browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div[1]/div[1]/div[1]/div[3]/span')).text!="running":
        sleep(3)
        browser_obj.driver.refresh()
    sleep(3)
    browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div/div/div/div/div/div[1]/div[2]/div/span[2]/span/a')).click()
    sleep(3)
    nu=browser_obj.driver.window_handles
    browser_obj.driver.switch_to.window(nu[1])
    sleep(3)
    browser_obj.driver.refresh()
    sleep(3)
    assert browser_obj.find_element((By.XPATH,'/html/body/h1')).text=='Welcome to nginx!'
    sleep(1)
    browser_obj.driver.switch_to.window(nu[0])


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_appstore_my_view_details_redeplo(browser_obj):
    '''重新部署'''
    wd = WebDriverWait(browser_obj.driver, 30)
    sleep(1)
    wd.until(EC.presence_of_element_located((By.XPATH, '//span[text()="重新部署"]')))
    browser_obj.find_element((By.XPATH,'//span[text()="重新部署"]')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')))
    assert browser_obj.find_element((By.XPATH,'/html/body/div[2]/div/div/div/div/div/span[2]')).text == "重新部署应用成功,请勿重复操作"
   # 点击返回
    wd.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/section/section/div/main/div/div/div/section/section/div/main/div/div/div/div/div/div/div[1]/div[2]/div/span[3]')))
    browser_obj.find_element((By.XPATH, '/html/body/div[1]/div/section/section/div/main/div/div/div/section/section/div/main/div/div/div/div/div/div/div[1]/div[2]/div/span[3]')).click()
    sleep(4)
    browser_obj.find_element((By.XPATH,'//span[text()="是"]')).click()
    sleep(1)
    wd.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')))
    assert browser_obj.find_element((By.XPATH,'/html/body/div[2]/div/div/div/div/div/span[2]')).text == "删除暴露应用成功"
    # 点击返回
    wd.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[2]/ul/li[1]/span/a')))
    browser_obj.find_element((By.XPATH,'/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[2]/ul/li[1]/span/a')).click()


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_appstore_my_dispose_details(browser_obj):
    '''查看处理详情'''
    wd = WebDriverWait(browser_obj.driver, 30)

    wd.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[1]/td[6]/div/a')))
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[1]/td[6]/div/a')).click()
    sleep(0.5)
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="查看处理详情"]')))
    browser_obj.find_element((By.XPATH,'//span[text()="查看处理详情"]')).click()
    # 点击关闭
    sleep(0.5)
    browser_obj.driver.refresh()


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_appstore_my_amend_application(browser_obj):
    '''修改应用'''
    wd = WebDriverWait(browser_obj.driver, 30)

    wd.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[1]/td[6]/div/a')))
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[1]/td[6]/div/a')).click()
    sleep(1)
    browser_obj.find_element((By.XPATH, '//span[text()="修改应用"]')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//div[text()="副本设置(必填)"]')))
    browser_obj.find_element((By.XPATH, '//div[text()="副本设置(必填)"]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="copy_replicas"]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="copy_replicas"]')).send_keys(Keys.BACK_SPACE)
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="copy_replicas"]')).send_keys('2')
    # 点击关闭
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"提 交")]')).click()
    wd.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')))

    assert browser_obj.find_element((By.XPATH,'/html/body/div[2]/div/div/div/div/div/span[2]')).text == "修改成功"


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_appstore_my_delete_application(browser_obj):
    '''删除应用'''
    wd = WebDriverWait(browser_obj.driver, 30)

    wd.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[1]/td[6]/div/a')))
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[1]/td[6]/div/a')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH,'//span[contains(text(),"删除")]')).click()
    sleep(3)
    browser_obj.find_element((By.XPATH,'//span[contains(text(),"是")]')).click()
    sleep(0.5)
    wd.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')))
    assert browser_obj.find_element((By.XPATH,'/html/body/div[2]/div/div/div/div/div/span[2]')).text == "操作成功"

    sleep(2)
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="ant-layout-header"]/div/div[2]/section[3]/section/span')))
    akik=browser_obj.find_element((By.XPATH, '//*[@class="ant-layout-header"]/div/div[2]/section[3]/section/span'))
    ActionChains(browser_obj.driver).move_to_element(akik).perform()
    sleep(1)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"退出登录")]')).click()
    sleep(1)