import pytest
from selenium.webdriver.common.by import By
from utils.times import sleep


@pytest.fixture(scope='module', autouse=True)
def login(browser_obj, login_url):
    browser_obj.open_url(login_url)
    browser_obj.find_element((By.XPATH, '//*/input[@id="username"]')).send_keys('admin')
    browser_obj.find_element((By.XPATH, '//*/input[@id="password"]')).send_keys('000000')
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[2]/button')).click()
    sleep(0.1)
    # 进入项目协同模块
    browser_obj.find_element(
        (By.XPATH, '//*[@id="rc-tabs-0-panel--1"]/div/div[1]/div/div/div[1]/div[1]/div/div/div/div[1]')).click()
    sleep(0.1)
    browser_obj.find_element(
        (By.XPATH, '//*[@id="root"]/section/aside/div/div/ul[1]/li[2]/div')).click()
    sleep(0.1)
    yield
    browser_obj.close()