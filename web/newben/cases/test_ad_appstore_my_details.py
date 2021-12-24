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
def test_appstore_my_details_application_details(browser_obj,nginx):
    '''应用详情-修改应用'''
    browser_obj.implicitly_wait(30)
    wd=WebDriverWait(browser_obj.driver,30)

    wd.until(EC.presence_of_element_located((By.XPATH, '//*[@id="userName"]')))
    browser_obj.find_element((By.XPATH, '//*[@id="userName"]')).send_keys('admin')
    wd.until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
    browser_obj.find_element((By.XPATH, '//*[@id="password"]')).send_keys('password')
    wd.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[4]/div/div/div/button')))
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[4]/div/div/div/button')).click()
    # 点击应用管理
    wd.until(EC.presence_of_element_located((By.XPATH, '//span[text()="应用管理"]')))
    browser_obj.find_element((By.XPATH,'//span[text()="应用管理"]')).click()
    # 点击我的应用
    wd.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[2]/ul/li[1]/span/a')))
    browser_obj.find_element((By.XPATH,'/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[2]/ul/li[1]/span/a')).click()
    # 点击创建应用
    wd.until(EC.presence_of_element_located((By.XPATH, '//span[text()="创建应用"]')))
    browser_obj.find_element((By.XPATH, '//span[text()="创建应用"]')).click()
    # 输入详细数据
    # 应用名
    wd.until(EC.presence_of_element_located((By.XPATH, '//*[@id="base_applicationName"]')))
    browser_obj.find_element((By.XPATH, '//*[@id="base_applicationName"]')).send_keys("nginx-test01")
    # 镜像类型
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_type"]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_type"]')).send_keys(Keys.ENTER)
    # 镜像名称
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
    sleep(0.5)
    assert browser_obj.find_element((By.XPATH,'/html/body/div[2]/div/div/div/div/div/span[2]')).text == "创建成功"
    sleep(0.5)
    browser_obj.find_element((By.XPATH,'//div[text()="nginx-test01"]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"修改应用")]')).click()
    sleep(2)
    browser_obj.find_element((By.XPATH, '//div[contains(text(),"副本设置(必填)")]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="copy_replicas"]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="copy_replicas"]')).send_keys(Keys.BACK_SPACE)
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="copy_replicas"]')).send_keys('2')
    # 点击关闭
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"提 交")]')).click()
    sleep(0.5)
    assert browser_obj.find_element((By.XPATH,'/html/body/div[2]/div/div/div/div/div/span[2]')).text == "修改成功"
    # 应用详情-查看处理详情
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="查看处理详情"]')))
    browser_obj.find_element((By.XPATH, '//span[text()="查看处理详情"]')).click()
    sleep(5)
    browser_obj.driver.refresh()
    sleep(1)
    #应用详情-查看日志
    wd.until(EC.visibility_of_element_located((By.XPATH, "//span[text()='日志']")))
    browser_obj.find_element((By.XPATH, "//span[text()='日志']")).click()
    sleep(2)
    nu=browser_obj.driver.window_handles
    browser_obj.driver.switch_to.window(nu[-1])
    sleep(3)
    browser_obj.driver.switch_to.window(nu[0])
    sleep(0.5)
    # 应用详情-控制台
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="控制台"]')))
    browser_obj.find_element((By.XPATH, '//span[text()="控制台"]')).click()
    sleep(2)
    nu=browser_obj.driver.window_handles
    browser_obj.driver.switch_to.window(nu[-1])
    sleep(3)
    browser_obj.driver.switch_to.window(nu[0])
    sleep(0.5)


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_appstore_my_details_strategy(browser_obj):
    '''应用详情-伸缩策略'''
    wd=WebDriverWait(browser_obj.driver,30)

    wd.until(EC.presence_of_element_located((By.XPATH, '//div[text()="伸缩策略"]')))
    browser_obj.find_element((By.XPATH, "//div[text()='伸缩策略']")).click()
    wd.until(EC.presence_of_element_located((By.XPATH, '//span[text()="立即设置"]')))
    browser_obj.find_element((By.XPATH, "//span[text()='立即设置']")).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//*[@id="triggers_init_field"]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="triggers_init_field"]')).send_keys(Keys.ENTER)
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//*[@id="triggers_init_value_value"]')).send_keys('10')
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//*[@id="triggers_init_last"]')).send_keys('60')
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//*[@id="replicasLimitDown"]')).send_keys('1')
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//*[@id="replicasLimitUp"]')).send_keys('5')
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//*[@id="cooldownDown"]')).send_keys('120')
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//*[@id="cooldownUp"]')).send_keys('60')
    sleep(1)
    browser_obj.find_element((By.XPATH, "//span[text()='设 置']")).click()
    sleep(0.3)
    assert browser_obj.find_element((By.XPATH,'/html/body/div[2]/div/div/div/div/div/span[2]')).text == "设置伸缩策略成功"
    sleep(1)
    browser_obj.find_element((By.XPATH, "//button[1]/span[text()='删 除']")).click()
    sleep(3)
    browser_obj.find_element((By.XPATH, "//span[text()='是']")).click()
    sleep(0.3)
    assert browser_obj.find_element((By.XPATH,'/html/body/div[2]/div/div/div/div/div/span[2]')).text == "删除伸缩策略成功！"


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_appstore_my_details_history(browser_obj):
    '''应用详情-历史版本'''
    wd=WebDriverWait(browser_obj.driver,30)

    wd.until(EC.presence_of_element_located((By.XPATH, '//div[text()="历史版本"]')))
    browser_obj.find_element((By.XPATH, "//div[text()='历史版本']")).click()
    wd.until(EC.presence_of_element_located((By.XPATH, '//span[text()="查看详情"]')))
    browser_obj.find_element((By.XPATH, "//span[text()='查看详情']")).click()
    sleep(2)
    assert browser_obj.find_element((By.XPATH,'//div[@class="ant-modal-body"]/div/div[1]/span[2]')).text =="历史版本YAML"
    sleep(0.5)
    wd.until(EC.presence_of_element_located((By.XPATH, "//span[text()='知道了']")))
    browser_obj.find_element((By.XPATH, "//span[text()='知道了']")).click()

    wd.until(EC.presence_of_element_located((By.XPATH, "//div[text()='资源定义']")))
    browser_obj.find_element((By.XPATH, "//div[text()='资源定义']")).click()
    sleep(0.5)
    # 应用详情-删除应用
    wd=WebDriverWait(browser_obj.driver,10)

    wd.until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(),"删 除")]')))
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"删 除")]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"是")]')).click()
    sleep(0.5)
    assert browser_obj.find_element((By.XPATH,'/html/body/div[2]/div/div/div/div/div/span[2]')).text == "操作成功"
    sleep(0.5)

    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="ant-layout-header"]/div/div[2]/section[3]/section/span')))
    akik=browser_obj.find_element((By.XPATH, '//*[@class="ant-layout-header"]/div/div[2]/section[3]/section/span'))
    ActionChains(browser_obj.driver).move_to_element(akik).perform()
    sleep(1)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"退出登录")]')).click()
    sleep(1)


