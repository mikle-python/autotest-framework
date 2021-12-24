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
def test_virtual_mirror_creat(browser_obj):
    '''镜像管理-虚拟机镜像'''
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
    wd.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[5]/ul/li[2]/span/a')))
    browser_obj.find_element((By.XPATH, '/html/body/div[1]/div/section/section/div/main/div/div/div/section/aside/div/ul/li[5]/ul/li[2]/span/a')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[contains(text(),"上传镜像")]')))
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"上传镜像")]')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="name"]')))
    browser_obj.find_element((By.XPATH, '//*[@id="name"]')).send_keys('nginx-test')
    browser_obj.find_element((By.XPATH, '//*[@id="minDisk"]')).send_keys('0.5')
    browser_obj.find_element((By.XPATH, '//*[@id="minMemory"]')).send_keys('0.5')
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="点击上传文件"]')))
    browser_obj.find_element((By.XPATH, '//span[text()="点击上传文件"]')).click()
    sleep(5)
    a = os.path.abspath('..')
    sleep(1)
    b = os.path.join(a, r'ghostcloudtest\web\newben\data\nginx-test.qcow2')
    sleep(1)
    dialog = win32gui.FindWindow('#32770', '打开')  # 对话框
    ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, 'ComboBoxEx32', None)
    ComboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, 'ComboBox', None)
    Edit = win32gui.FindWindowEx(ComboBox, 0, 'Edit', None)  # 上面三句依次寻找对象，直到找到输入框Edit对象的句柄
    button = win32gui.FindWindowEx(dialog, 0, 'Button', None)  # 确定按钮Button
    sleep(1)
    win32gui.SendMessage(Edit, win32con.WM_SETTEXT, None,b)  # 往输入框输入绝对地址
    win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 按button
    sleep(3)
    browser_obj.find_element((By.XPATH, '//span[text()="确 定"]')).click()
    sleep(0.5)
    assert browser_obj.find_element((By.XPATH,'/html/body/div[2]/div/div/div/div/div/span[2]')).text == "镜像文件上传成功"


@pytest.mark.flaky(retun=3,runs_delay=2)
def test_virtual_mirror_view_details_delect(browser_obj):
    '''查看详情,下载镜像,删除镜像'''
    wd=WebDriverWait(browser_obj.driver,10)

    wd.until(EC.visibility_of_element_located((By.XPATH, '//a[text()="查看详情"]')))
    browser_obj.find_element((By.XPATH, '//a[text()="查看详情"]')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="下载镜像"]')))
    browser_obj.find_element((By.XPATH, '//span[text()="下载镜像"]')).click()
    sleep(3)
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="删除"]')))
    browser_obj.find_element((By.XPATH, '//span[text()="删除"]')).click()
    wd.until(EC.visibility_of_element_located((By.XPATH, '//span[text()="是"]')))
    browser_obj.find_element((By.XPATH, '//span[text()="是"]')).click()
    sleep(0.5)
    assert browser_obj.find_element((By.XPATH,'/html/body/div[2]/div/div/div/div/div/span[2]')).text == "删除成功"

    sleep(0.5)
    wd.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="ant-layout-header"]/div/div[2]/section[3]/section/span')))
    akik=browser_obj.find_element((By.XPATH, '//*[@class="ant-layout-header"]/div/div[2]/section[3]/section/span'))
    ActionChains(browser_obj.driver).move_to_element(akik).perform()
    sleep(1)
    browser_obj.find_element((By.XPATH, '//span[contains(text(),"退出登录")]')).click()
    sleep(1)



