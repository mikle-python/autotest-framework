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
def test_torage_administration_create_localstorage(browser_obj):
    '''存储管理-存储资源池'''
    browser_obj.implicitly_wait(10)
    wd=WebDriverWait(browser_obj.driver,10)
    sleep(1)
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="userName"]')))
    browser_obj.find_element((By.XPATH, '//*[@id="userName"]')).send_keys('admin')
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//*[@id="password"]')).send_keys('password')
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[4]/div/div/div/button')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//span[text()="存储管理"]')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[6]/ul/li[1]/span/a')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//span[text()="新 增"]')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks"]/div[1]/div/div/div[1]/div[2]/div/div/span/span/span')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks_name"]')).send_keys('localStorage001')
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks_provisioner"]')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks_provisioner"]')).send_keys(Keys.ENTER)
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks_workerName"]')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks_workerName"]')).send_keys(Keys.ENTER)
    sleep(1)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks_parameters_path"]')).send_keys('/data/test')
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//span[text()="保 存"]')).click()
    sleep(0.3)
    assert browser_obj.find_element((By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')).text == "新增存储资源池成功"


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_torage_administration_create_glusterfs(browser_obj):
    wd = WebDriverWait(browser_obj.driver, 10)
    sleep(1)
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="新 增"]')))
    browser_obj.find_element((By.XPATH,'//span[text()="新 增"]')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks"]/div[1]/div/div/div[1]/div[2]/div/div/span/span/span')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks_name"]')).send_keys('GlusterFS001')
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks_provisioner"]')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks_provisioner"]')).send_keys(Keys.DOWN)
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks_provisioner"]')).send_keys(Keys.ENTER)
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks_total"]')).send_keys('10G')
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks_GlusterFS_host"]')).send_keys('http://192.168.5.5:8443')
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks_GlusterFS_user"]')).send_keys('admin')
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks_GlusterFS_key"]')).send_keys('password')
    sleep(1)
    browser_obj.find_element((By.XPATH,'//span[text()="保 存"]')).click()
    sleep(0.3)
    assert browser_obj.find_element((By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')).text == "新增存储资源池成功"


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_torage_administration_create_cephfs(browser_obj):
    wd = WebDriverWait(browser_obj.driver, 10)
    sleep(1)
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="新 增"]')))
    browser_obj.find_element((By.XPATH,'//span[text()="新 增"]')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks"]/div[1]/div/div/div[1]/div[2]/div/div/span/span/span')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks_name"]')).send_keys('cephFS001')
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks_provisioner"]')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks_provisioner"]')).send_keys(Keys.DOWN)
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks_provisioner"]')).send_keys(Keys.DOWN)
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks_provisioner"]')).send_keys(Keys.ENTER)
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks_CephFS_mons"]')).send_keys('192.168.5.5:8443')
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks_CephFS_user"]')).send_keys('client.admin')
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks_CephFS_key"]')).send_keys('AQAnhIpgsP56KRAA91FiAFYTT2fzsAy5J6BLXA==')

    sleep(1)
    browser_obj.find_element((By.XPATH,'//span[text()="保 存"]')).click()
    sleep(0.3)
    assert browser_obj.find_element((By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')).text == "新增存储资源池成功"


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_torage_administration_create_cephrbd(browser_obj):
    wd = WebDriverWait(browser_obj.driver, 10)
    sleep(1)
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="新 增"]')))
    browser_obj.find_element((By.XPATH,'//span[text()="新 增"]')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks"]/div[1]/div/div/div[1]/div[2]/div/div/span/span/span')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks_name"]')).send_keys('cephRBD001')
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks_provisioner"]')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks_provisioner"]')).send_keys(Keys.DOWN)
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks_provisioner"]')).send_keys(Keys.DOWN)
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks_provisioner"]')).send_keys(Keys.DOWN)
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks_provisioner"]')).send_keys(Keys.ENTER)
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks_total"]')).send_keys('10G')
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks_CephRBD_mons"]')).send_keys('192.168.5.5:8443')
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks_CephRBD_user"]')).send_keys('client.admin')
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks_CephRBD_key"]')).send_keys('AQAnhIpgsP56KRAA91FiAFYTT2fzsAy5J6BLXA==')
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="control-hooks_CephRBD_pool"]')).send_keys('newben-rbd')
    sleep(1)
    browser_obj.find_element((By.XPATH,'//span[text()="保 存"]')).click()
    sleep(0.3)
    assert browser_obj.find_element((By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')).text == "新增存储资源池成功"


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_torage_administration_search(browser_obj):
    wd=WebDriverWait(browser_obj.driver,10)
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/header/div/div[2]/span/span/input')).send_keys('cephRBD001')
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/header/div/div[2]/span/button')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//span[text()="查看详情"]')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//span[text()="返 回"]')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//span[text()="查看处理详情"]')).click()
    sleep(0.3)
    browser_obj.driver.refresh()

    sleep(1)
    browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/header/div/div[2]/span/span/input')).send_keys('cephRBD001')
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/header/div/div[2]/span/button')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//span[text()="删除"]')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//span[text()="是"]')).click()
    sleep(0.3)
    assert browser_obj.find_element((By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')).text == "操作成功"
    browser_obj.driver.refresh()

    sleep(1)
    browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/header/div/div[2]/span/span/input')).send_keys('cephFS001')
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/header/div/div[2]/span/button')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//span[text()="删除"]')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//span[text()="是"]')).click()
    sleep(0.3)
    browser_obj.driver.refresh()

    sleep(1)
    browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/header/div/div[2]/span/span/input')).send_keys('GlusterFS001')
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/header/div/div[2]/span/button')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//span[text()="删除"]')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//span[text()="是"]')).click()
    sleep(0.3)
    browser_obj.driver.refresh()

    sleep(1)
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="ant-layout-header"]/div/div[2]/section[3]/section/span')))
    akik=browser_obj.find_element((By.XPATH, '//*[@class="ant-layout-header"]/div/div[2]/section[3]/section/span'))
    ActionChains(browser_obj.driver).move_to_element(akik).perform()
    sleep(1)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"退出登录")]')).click()
    sleep(1)