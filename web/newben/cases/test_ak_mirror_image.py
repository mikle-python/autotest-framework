import pytest
import pywinauto
from libs.log_obj import LogObj
from selenium.webdriver.common.by import By
from utils.times import sleep
from utils.util import generate_string
from web import arguments
from selenium.webdriver.common.keys import Keys
from pywinauto.keyboard import send_keys
import os
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import win32con
import win32gui

args = arguments.parse_arg()
logger = LogObj().get_logger()


@pytest.fixture(scope='module', autouse=True)
def open_login_url(browser_obj, login_url):
    browser_obj.open_url(login_url)


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_mirror_image_uploading(browser_obj):
    '''镜像管理-镜像上传'''
    browser_obj.implicitly_wait(10)
    wd=WebDriverWait(browser_obj.driver,10)
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="userName"]')))
    browser_obj.find_element((By.XPATH, '//*[@id="userName"]')).send_keys('admin')
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]')))
    browser_obj.find_element((By.XPATH, '//*[@id="password"]')).send_keys('password')
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[4]/div/div/div/button')))
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/div[2]/div[2]/div/div[2]/div/form/div[4]/div/div/div/button')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[contains(text(),"镜像管理")]')))
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"镜像管理")]')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[5]/ul/li[1]/span/a')))
    browser_obj.find_element((By.XPATH, '/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[5]/ul/li[1]/span/a')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="上传镜像"]')))
    browser_obj.find_element((By.XPATH, '//span[text()="上传镜像"]')).click()
    wd.until(EC.presence_of_element_located((By.XPATH, '//span[contains(text()," 选择文件")]')))
    browser_obj.find_element((By.XPATH, '//span[contains(text()," 选择文件")]')).click()
    sleep(3)
    a = os.path.abspath('..')
    sleep(1)
    b = os.path.join(a, r'ghostcloudtest\web\newben\data\nginx.tar')
    sleep(1)
    dialog = win32gui.FindWindow('#32770', '打开')  # 对话框
    ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, 'ComboBoxEx32', None)
    ComboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, 'ComboBox', None)
    Edit = win32gui.FindWindowEx(ComboBox, 0, 'Edit', None)  # 上面三句依次寻找对象，直到找到输入框Edit对象的句柄
    button = win32gui.FindWindowEx(dialog, 0, 'Button', None)  # 确定按钮Button
    sleep(1)
    win32gui.SendMessage(Edit, win32con.WM_SETTEXT, None,b)  # 往输入框输入绝对地址
    win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 按button
    # a = os.path.abspath('..')
    # sleep(1)
    # b = os.path.join(a, r'ghostcloudtest\web\newben\data\nginx.tar')
    # sleep(1)
    # pywinauto.keyboard.send_keys(b)
    # sleep(3)
    # pywinauto.keyboard.send_keys("{ENTER}")
    sleep(3)
    browser_obj.find_element((By.XPATH, '//span[text()="关 闭"]')).click()


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_mirror_image_online_production(browser_obj,nginx):
    '''在线制作镜像'''
    wd=WebDriverWait(browser_obj.driver,10)

    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[contains(text(),"在线制作")]')))
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"在线制作")]')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="name"]')))
    browser_obj.find_element((By.XPATH, '//*[@id="name"]')).send_keys('image-test')
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//*[@id="tag"]')).send_keys('v1')
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="tpy"]')).click()
    sleep(1)
    browser_obj.find_element((By.XPATH, '//*[@id="tpy"]')).send_keys(Keys.ENTER)
    sleep(1)
    browser_obj.find_element((By.XPATH, '//*[@id="baseImage"]')).click()
    sleep(1)
    browser_obj.find_element((By.XPATH, '//*[@id="baseImage"]')).send_keys(nginx)
    sleep(1)
    browser_obj.find_element((By.XPATH, '//*[@id="baseImage"]')).send_keys(Keys.ENTER)
    sleep(1)
    browser_obj.find_element((By.XPATH, '//*[@id="baseTag"]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="baseTag"]')).send_keys(Keys.ENTER)
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//span[text()="点击上传文件"]')).click()
    sleep(3)
    a = os.path.abspath('..')
    sleep(1)
    b = os.path.join(a, r'ghostcloudtest\web\newben\data\commons-fileupload-1.4.jar')
    sleep(1)
    dialog = win32gui.FindWindow('#32770', '打开')  # 对话框
    ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, 'ComboBoxEx32', None)
    ComboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, 'ComboBox', None)
    Edit = win32gui.FindWindowEx(ComboBox, 0, 'Edit', None)  # 上面三句依次寻找对象，直到找到输入框Edit对象的句柄
    button = win32gui.FindWindowEx(dialog, 0, 'Button', None)  # 确定按钮Button
    sleep(1)
    win32gui.SendMessage(Edit, win32con.WM_SETTEXT, None,b)  # 往输入框输入绝对地址
    win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 按button
    sleep(2)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"确 定")]')).click()
    sleep(6)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"取 消")]')).click()


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_mirror_image_view_details(browser_obj):
    '''查看详情+快速部署+下载'''
    wd=WebDriverWait(browser_obj.driver,10)

    wd.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/section[1]/div/div[2]/span/span/input')))
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/section[1]/div/div[2]/span/span/input')).send_keys('nginx-tester')
    wd.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/section[1]/div/div[2]/span/button')))
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/section[1]/div/div[2]/span/button')).click()
    wd.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/section[2]/div/div/div/div[1]/div/div/div/div/div/div/div[1]/div/div/div/span[2]/a')))
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/section[2]/div/div/div/div[1]/div/div/div/div/div/div/div[1]/div/div/div/span[2]/a')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="快速部署"]')))
    browser_obj.find_element((By.XPATH, '//span[text()="快速部署"]')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="base_applicationName"]')))
    browser_obj.find_element((By.XPATH, '//*[@id="base_applicationName"]')).send_keys('nginx-test001')
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//*[@id="base_imagePullPolicy"]')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="base_imagePullPolicy"]')).send_keys(Keys.ENTER)
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//*[@id="base_cpuResource"]')).send_keys('100')
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//*[@id="base_memoryResource"]')).send_keys('100')
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//*[@id="base_gpuResource"]')).send_keys('10')
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//span[text()="提 交"]')).click()
    sleep(1)
    assert browser_obj.find_element((By.XPATH,'/html/body/div[2]/div/div/div/div/div/span[2]')).text == "创建成功"
    sleep(0.3)


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_mirror_image_delect(browser_obj):
    '''删除'''
    wd=WebDriverWait(browser_obj.driver,10)

    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="返 回"]')))
    browser_obj.find_element((By.XPATH, '//span[text()="返 回"]')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/section[1]/div/div[2]/span/span/input')))
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/section[1]/div/div[2]/span/span/input')).send_keys('nginx-tester')
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/section[1]/div/div[2]/span/button')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/section[2]/div/div/div/div[1]/div/div/div/div/div/div/div[1]/div/div/div/span[2]/a')))
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/section[2]/div/div/div/div[1]/div/div/div/div/div/div/div[1]/div/div/div/span[2]/a')).click()
    sleep(0.3)
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="删除"]')))
    browser_obj.find_element((By.XPATH, '//span[text()="删除"]')).click()
    sleep(2)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"是")]')).click()
    sleep(2)
    assert browser_obj.find_element((By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')).text == "删除Tag成功"

    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/section[1]/div/div[2]/span/span/input')))
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/section[1]/div/div[2]/span/span/input')).send_keys('image-test')
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/section[1]/div/div[2]/span/button')).click()
    sleep(0.3)
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/section[2]/div/div/div/div[1]/div/div/div/div/div/div/div[1]/div/div/div/span[2]/a')).click()
    sleep(0.3)
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="删除"]')))
    browser_obj.find_element((By.XPATH, '//span[text()="删除"]')).click()
    sleep(1)
    browser_obj.find_element((By.XPATH, '//span[text()="是"]')).click()
    sleep(2)
    assert browser_obj.find_element((By.XPATH, '/html/body/div[2]/div/div/div/div/div/span[2]')).text == "删除Tag成功"
    # 点击应用管理
    sleep(1)
    browser_obj.find_element((By.XPATH,'//span[text()="应用管理"]')).click()
    # 点击我的应用
    sleep(0.5)
    browser_obj.find_element((By.XPATH,'/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[2]/ul/li[1]/span/a')).click()
    sleep(0.5)
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/section/section/div/main/div/div/div/section/section/div/main/div/div[1]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr[1]/td[6]/div/a')).click()
    sleep(0.5)
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="删除"]')))
    browser_obj.find_element((By.XPATH,'//span[text()="删除"]')).click()
    sleep(2)
    browser_obj.find_element((By.XPATH,'//span[text()="是"]')).click()
    sleep(2)
    assert browser_obj.find_element((By.XPATH,'/html/body/div[2]/div/div/div/div/div/span[2]')).text == "操作成功"
    sleep(1)

    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="ant-layout-header"]/div/div[2]/section[3]/section/span')))
    akik=browser_obj.find_element((By.XPATH, '//*[@class="ant-layout-header"]/div/div[2]/section[3]/section/span'))
    ActionChains(browser_obj.driver).move_to_element(akik).perform()
    sleep(1)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"退出登录")]')).click()
    sleep(1)



