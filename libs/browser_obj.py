import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from settings.global_settings import PROJECT_PATH


class BrowserObj(object):
    def __init__(self, browser):
        browser = browser.lower()
        if browser == 'edge':
            self.service_obj = Service(executable_path=os.path.join(PROJECT_PATH, "bin\\webdriver\\msedgedriver.exe"))
            self.driver = webdriver.Edge(service=self.service_obj)
        elif browser == 'chrome':
            self.service_obj = Service(executable_path=os.path.join(PROJECT_PATH, "bin\\webdriver\\chromedriver.exe"))
            self.driver = webdriver.Chrome(service=self.service_obj)
        elif browser == 'ie':
            self.service_obj = Service(executable_path=os.path.join(PROJECT_PATH, "bin\\webdriver\\IEDriverServer.exe"))
            self.driver = webdriver.Ie(service=self.service_obj)
        elif browser == 'firefox':
            self.service_obj = Service(executable_path=os.path.join(PROJECT_PATH, "bin\\webdriver\\geckodriver.exe"))
            self.driver = webdriver.Firefox(service=self.service_obj)
        else:
            raise Exception('Don\'t support browser {0}!'.format(browser))
        self.timeout = 10
        self.wait = WebDriverWait(self.driver, self.timeout)

    def open_url(self, url):
        self.driver.maximize_window()
        self.driver.get(url)

    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def implicitly_wait(self, seconds):
        self.driver.implicitly_wait(seconds)

    def refresh(self):
        self.driver.refresh()

    def forward(self):
        self.driver.forward()

    def back(self):
        self.driver.back()

    def quit(self):
        self.driver.quit()

    def close(self):
        self.driver.close()

    def save_screenshot(self, pic_path):
        self.driver.save_screenshot(pic_path)

    def click(self, locator):
        """
        点击
        :param locator:
        :return:
        """
        self.find_element(locator).click()

    def send_key(self, locator, content):
        """
        输入内容
        :param locator:
        :param content:
        :return:
        """
        self.find_element(locator).send_keys(content)

    def get_text(self, locator):
        """
        获取标签文本
        :param locator:
        :return:
        """
        return self.find_element(locator).text

    def script(self, src):
        """
        调用JavaScript
        :param src:
        :return:
        """
        self.driver.execute_script(src)

    def switch_alert(self):
        """
        警告框处理
        :return:
        """
        return self.driver.switch_to.alert
        
    def find_element_by_xpath(self, xpath):
        """
        xpath查找元素
        :param xpath:
        :return:
        """
        return self.driver.find_element(By.XPATH, xpath)


if __name__ == '__main__':
    browser_obj = BrowserObj('edge')
    browser_obj.open_url('http://192.168.0.14/#/login')
    browser_obj.find_element((By.XPATH, '//*/input[@id="username"]')).send_keys('admin')
    browser_obj.find_element((By.XPATH, '//*/input[@id="password"]')).send_keys('adminP@ssw0rd')
    browser_obj.find_element((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[2]/button')).click()
    browser_obj.save_screenshot('C:/test/test.png')
    browser_obj.quit()