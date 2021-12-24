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
def test_torage_administration_create_list(browser_obj):
    '''存储管理-存储卷'''
    browser_obj.implicitly_wait(10)
    wd=WebDriverWait(browser_obj.driver,10)

    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="userName"]')))
    browser_obj.find_element((By.XPATH, '//*[@id="userName"]')).send_keys('admin')
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]')))
    browser_obj.find_element((By.XPATH, '//*[@id="password"]')).send_keys('password')
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[4]/div/div/div/button')))
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[4]/div/div/div/button')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="存储管理"]')))
    browser_obj.find_element((By.XPATH,'//span[text()="存储管理"]')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[6]/ul/li[2]/span/a')))
    browser_obj.find_element((By.XPATH,'/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[6]/ul/li[2]/span/a')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//span[text()="新 增"]')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="volume-create-form-id"]/div[1]/div/div/div[1]/div[2]/div/div/span/span/span')))
    browser_obj.find_element((By.XPATH,'//*[@id="volume-create-form-id"]/div[1]/div/div/div[1]/div[2]/div/div/span/span/span')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="name"]')).send_keys('localStorage-pv')
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="storagePool"]')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="storagePool"]')).send_keys(Keys.ENTER)
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//span[text()="确 定"]')).click()
    sleep(0.3)
    assert browser_obj.find_element((By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')).text == "创建成功"


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_torage_administration_create_list_detail(browser_obj):
    wd=WebDriverWait(browser_obj.driver,10)

    wd.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/section/section/div/main/div/div/div/section/section/div/main/div/div/div/div/header/div/div[2]/span/span/input')))
    browser_obj.find_element((By.XPATH,'/html/body/div[1]/div/section/section/div/main/div/div/div/section/section/div/main/div/div/div/div/header/div/div[2]/span/span/input')).send_keys('localStorage-pv')
    sleep(1)
    browser_obj.find_element((By.XPATH,'/html/body/div[1]/div/section/section/div/main/div/div/div/section/section/div/main/div/div/div/div/header/div/div[2]/span/button/span')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="查看配置"]')))
    browser_obj.find_element((By.XPATH,'//span[text()="查看配置"]')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="确 定"]')))
    browser_obj.find_element((By.XPATH,'//span[text()="确 定"]')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="查看处理详情"]')))
    browser_obj.find_element((By.XPATH,'//span[text()="查看处理详情"]')).click()
    sleep(0.3)
    browser_obj.driver.refresh()

    wd.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/section/section/div/main/div/div/div/section/section/div/main/div/div/div/div/header/div/div[2]/span/span/input')))
    browser_obj.find_element((By.XPATH,'/html/body/div[1]/div/section/section/div/main/div/div/div/section/section/div/main/div/div/div/div/header/div/div[2]/span/span/input')).send_keys('localStorage-pv')
    sleep(1)
    browser_obj.find_element((By.XPATH,'/html/body/div[1]/div/section/section/div/main/div/div/div/section/section/div/main/div/div/div/div/header/div/div[2]/span/button/span')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//span[text()="删除"]')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//span[text()="确 定"]')).click()
    sleep(0.3)
    assert browser_obj.find_element((By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')).text == "操作成功"

    sleep(0.3)
    browser_obj.find_element((By.XPATH,'/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[6]/ul/li[1]/span/a')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH,'//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/header/div/div[2]/span/span/input')).send_keys('localStorage001')
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




