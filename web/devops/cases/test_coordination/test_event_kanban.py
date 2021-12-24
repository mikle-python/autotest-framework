import re
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from utils.times import sleep
from libs.log_obj import LogObj

logger = LogObj().get_logger()


@pytest.fixture(scope='function', autouse=True)
def enter_original_demand(browser_obj):
    # 进入事项看板初始页面
    browser_obj.click((By.XPATH, '//*[@id="/dashboard$Menu"]/li[2]/a'))
    sleep(2)


@pytest.mark.run(order=1)
def test_create_iteration_and_event(browser_obj):
    """
    测试快速创建迭代和事项
    :param browser_obj:
    :return:
    """
    # 1.快速创建迭代
    browser_obj.click((By.XPATH, '//button/span[contains(.,"创建迭代")]'))
    sleep(1)
    browser_obj.click((By.XPATH, '//*[@id="sprintTitle"]'))
    iteration_name = '自动化测试创建迭代版本1'
    browser_obj.send_key((By.XPATH, '//*[@id="sprintTitle"]'), iteration_name)
    browser_obj.click((By.XPATH, '//button/span[contains(.,"创 建")]'))
    sleep(1)
    # 断言判断
    assert browser_obj.get_text(
        (By.XPATH,
         '//*[@role="tabpanel"]/div[2]/div/div/div[1]/div/div/div/div[1]/div/div[1]/a')) == iteration_name
    assert browser_obj.get_text(
        (By.XPATH, '//*[@role="tabpanel"]/div[2]/div/div/div[1]/div/div/div/div[2]/div/div[1]/span')) == '未开始'

    # 2.快速创建事项
    # browser_obj.click((By.XPATH, '//*[@role="tabpanel"]/div[2]/div/div/div[1]/div/div[1]/div/div[1]/div'))
    browser_obj.click((By.CSS_SELECTOR, '.ant-collapse:nth-child(1) .ant-collapse-header > .anticon'))
    sleep(10)
    browser_obj.click(
        (By.XPATH, '//*[@role="tabpanel"]/div[2]/div/div/div[1]/div/div[2]/div/div/div[1]/div/button[1]/span[2]'))
    sleep(1)
    style_val = browser_obj.get_attribute(
        (By.XPATH, '//*[@role="tabpanel"]/div[2]/div/div/div[1]/div/div[2]/div/div[1]/div/div/ul/li/div/div[1]/span'),
        'style')
    browser_obj.click((By.XPATH, '//*[@id="issueTitle1"]'))
    event_name = '自动化测试迭代版本1新建事项1@a'
    browser_obj.send_key((By.XPATH, '//*[@id="issueTitle1"]'), event_name)
    browser_obj.click((By.XPATH, '//button/span[contains(.,"创 建")]'))
    sleep(1)
    # 断言判断
    assert browser_obj.get_attribute(
        (By.XPATH,
         '//*[@role="tabpanel"]/div[2]/div/div/div[1]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div[1]/li/div/div[1]/span'),
        'style') == style_val
    assert browser_obj.get_text((By.XPATH, '//h4/div/div[2]/span/span')) == event_name
    assert browser_obj.get_text((By.XPATH, '//ul/li[1]/span/sup')) == '低'


@pytest.mark.run(order=2)
def test_create_iteration_and_event_abnormal_scene(browser_obj):
    """
    测试异常场景（名字长度超过限定）创建迭代和事项
    :param browser_obj:
    :return:
    """
    # 迭代名称超过长度
    browser_obj.click((By.XPATH, '//button/span[contains(.,"创建迭代")]'))
    sleep(1)
    browser_obj.click((By.XPATH, '//*[@id="sprintTitle"]'))
    iteration_name = ''
    for i in range(65):
        iteration_name += 'a'
    browser_obj.send_key((By.XPATH, '//*[@id="sprintTitle"]'), iteration_name)
    sleep(1)
    assert browser_obj.get_text(
        (By.XPATH,
         '//*[@role="tabpanel"]/div[2]/div/div/div[last()-1]/div[1]/form/div/div/div/div/div[2]/div')) == '迭代标题最多64个字符'
    # 事项名称超过长度
    # browser_obj.click((By.XPATH, '//*[@role="tabpanel"]/div[2]/div/div/div[1]/div/div[1]/span'))
    # sleep(1)
    browser_obj.click(
        (By.XPATH, '//*[@role="tabpanel"]/div[2]/div/div/div[1]/div/div[2]/div/div/div[1]/div/button[1]/span[2]'))
    sleep(1)
    browser_obj.click((By.XPATH, '//*[@id="issueTitle1"]'))
    event_name = ''
    for i in range(301):
        event_name += 'a'
    browser_obj.send_key((By.XPATH, '//*[@id="issueTitle1"]'), event_name)
    sleep(1)
    assert browser_obj.get_text((By.XPATH, '//h4/div/div[2]/form/div/div/div/div/div[2]/div')) == '标题最长300个字符'

    # 恢复初始
    browser_obj.click((By.XPATH, '//*[@role="tabpanel"]/div[2]/div/div/div[last()-1]/div[3]/button/span'))
    browser_obj.click((By.XPATH, '//h4/div/div[4]/button/span'))
    browser_obj.click((By.XPATH, '//*[@role="tabpanel"]/div[2]/div/div/div[1]/div/div[1]/span'))
    sleep(1)


def test_search_event_by_id_and_title(browser_obj):
    """
    测试通过事项id和标题查找对应事项
    :param browser_obj:
    :return:
    """
    browser_obj.click((By.XPATH, '//*[@role="tabpanel"]/div[2]/div/div/div[1]/div/div[1]/span'))
    sleep(1)
    # 通过事项id查找
    event_id = browser_obj.get_text((By.XPATH, '//h4/div/div[1]'))
    browser_obj.click((By.XPATH, '//*[@id="keywords"]'))
    sleep(1)
    browser_obj.send_key((By.XPATH, '//*[@id="keywords"]'), event_id.split('#')[-1])
    browser_obj.click((By.XPATH, '//*[@role="tabpanel"]/form/div/div[4]/div/div/div/div/span/span/span[2]/button'))
    sleep(1)
    assert browser_obj.get_text((By.XPATH, '//h4/div/div[1]')) == event_id
    browser_obj.click((By.XPATH, '//*[@role="tabpanel"]/form/div/div[4]/div/div/div/div/span/span/span[1]/span/span'))
    sleep(1)
    # 通过事项标题查找，涵盖数字、字母、中文、特殊字符
    browser_obj.send_key((By.XPATH, '//*[@id="keywords"]'), '新建事项1@a')
    browser_obj.click((By.XPATH, '//*[@role="tabpanel"]/form/div/div[4]/div/div/div/div/span/span/span[2]/button'))
    sleep(1)
    assert browser_obj.get_text((By.XPATH, '//h4/div/div[2]/span/span')) == '自动化测试迭代版本1新建事项1@a'
    browser_obj.click((By.XPATH, '//*[@role="tabpanel"]/form/div/div[4]/div/div/div/div/span/span/span[1]/span/span'))
    sleep(1)

    # 恢复初始页面
    browser_obj.click((By.XPATH, '//*[@role="tabpanel"]/div[2]/div/div/div[1]/div/div[1]/span'))
    sleep(1)


def test_event_conditional_filter(browser_obj):
    """
    测试事项条件筛选
    :param browser_obj:
    :return:
    """
    pass


def test_create_iteration_complete(browser_obj):
    """
    测试完整创建迭代
    :param browser_obj:
    :return:
    """
    # 1.点击创建迭代
    browser_obj.click((By.XPATH, '//button/span[contains(.,"创建迭代")]'))
    sleep(1)
    # 2.点击完整创建
    above = browser_obj.find_element_by_xpath(
        '//*[@role="tabpanel"]/div[2]/div/div/div[last()-1]/div[2]/div/button[2]/span')
    ActionChains(browser_obj.driver).move_to_element(above).perform()  # 鼠标悬停
    click_element = browser_obj.find_element_by_xpath(
        '//*[@id="private-project"]/div[last()]/div/div/ul/li/span/span/span')
    ActionChains(browser_obj.driver).move_to_element(above).click(click_element).perform()  # 鼠标悬停后点击
    sleep(1)
    # 3.输入完整迭代信息，创建迭代
    # 输入迭代标题
    browser_obj.click((By.XPATH, '//*[@id="title"]'))
    sleep(1)
    title = '自动化测试创建完整迭代1'
    browser_obj.send_key((By.XPATH, '//*[@id="title"]'), title)

    # 输入迭代目标
    browser_obj.click((By.XPATH, '//*[@id="target"]'))
    sleep(1)
    browser_obj.send_key((By.XPATH, '//*[@id="target"]'), '迭代目标内容')

    # 选择负责人
    browser_obj.click((By.ID, 'principalId'))
    sleep(1)
    browser_obj.click((By.XPATH, '/html/body/div[last()]/div/div/div/div[2]/div[1]/div/div/div[1]/div'))
    sleep(1)

    # 选择日期
    # start_js = 'document.getElementById("rangeTime").value = "2021-11-24";'
    # browser_obj.script(start_js)
    # end_js = 'document.getElementsByTagName("input")[8].value = "2022-11-24";'
    # browser_obj.script(end_js)
    browser_obj.click((By.ID, 'rangeTime'))
    sleep(1)
    browser_obj.click((By.XPATH, '//table/tbody/tr[4]/td[4]/div'))
    sleep(1)

    browser_obj.click((By.XPATH, '//div/div/div/div[3]/input'))
    sleep(1)
    browser_obj.click((By.XPATH, '//div/div/div/div[2]/div/div[2]/div/div[2]/table/tbody/tr[4]/td[4]/div'))
    sleep(1)

    browser_obj.click((By.XPATH, '//div/button[2]/span[contains(., "创 建")]'))
    sleep(1)
    # 断言
    assert browser_obj.get_text(
        (By.XPATH, '//*[@role="tabpanel"]/div[2]/div/div/div[1]/div/div[1]/div/div[1]/div/div[1]/a')) == title


def test_create_event_complete(browser_obj):
    """
    测试完整创建事项
    :param browser_obj:
    :return:
    """
    # 1.点击创建事项
    browser_obj.click((By.XPATH, '//*[@role="tabpanel"]/div[2]/div/div/div[1]/div/div[1]/span'))
    sleep(1)
    browser_obj.click(
        (By.XPATH, '//*[@role="tabpanel"]/div[2]/div/div/div[1]/div/div[2]/div/div/div[1]/div/button[1]/span[2]'))
    sleep(1)

    # 2.点击完整创建
    above = browser_obj.find_element_by_xpath('//h4/div/div[3]/div/button[2]/span')
    ActionChains(browser_obj.driver).move_to_element(above).perform()  # 鼠标悬停
    click_element = browser_obj.find_element_by_xpath('//*[@id="private-project"]/div[4]/div/div/ul/li/span/span')
    ActionChains(browser_obj.driver).move_to_element(above).click(click_element).perform()  # 鼠标悬停后点击
    sleep(1)

    # 3.输入事项信息，创建事项
    browser_obj.click((By.XPATH, '//*[@id="issueTitle"]'))
    sleep(1)
    title = '创建完整事项'
    browser_obj.send_key((By.XPATH, '//*[@id="issueTitle"]'), title)

    browser_obj.click((By.XPATH, '//button/span[contains(., "确 定")]'))
    sleep(1)

    browser_obj.click((By.XPATH, '//div/div[2]/div/div/div[1]/button'))
    sleep(1)

    assert browser_obj.get_text((By.XPATH, '//h4/div/div[2]/span/span')) == title
    browser_obj.click((By.XPATH, '//*[@role="tabpanel"]/div[2]/div/div/div[1]/div/div[1]/span'))
    sleep(1)


def test_start_iteration(browser_obj):
    """
    测试开始迭代
    :param browser_obj:
    :return:
    """

    above = browser_obj.find_element_by_xpath(
        '//*[@role="tabpanel"]/div[2]/div/div/div[1]/div/div[1]/div/div[1]/div/div[2]/span')
    ActionChains(browser_obj.driver).move_to_element(above).perform()  # 鼠标悬停
    click_element = browser_obj.find_element_by_xpath('//div/div/ul/li[1]/span/span/span')
    ActionChains(browser_obj.driver).move_to_element(above).click(click_element).perform()  # 鼠标悬停后点击
    sleep(1)

    browser_obj.click((By.XPATH, '//div/div[2]/div[3]/button[2]/span'))
    sleep(1)

    assert browser_obj.get_text((By.XPATH, '//div/div[1]/div/div[2]/div/div[2]/span')) == '进行中'
    browser_obj.click((By.XPATH, '//*[@role="tabpanel"]/div[2]/div/div/div[1]/div/div[1]/span'))
    sleep(1)


def test_edit_iteration(browser_obj):
    """
    测试编辑迭代
    :param browser_obj:
    :return:
    """
    above = browser_obj.find_element_by_xpath(
        '//*[@role="tabpanel"]/div[2]/div/div/div[1]/div/div[1]/div/div[1]/div/div[2]/span')
    ActionChains(browser_obj.driver).move_to_element(above).perform()  # 鼠标悬停
    click_element = browser_obj.find_element_by_xpath('//*[@id="private-project"]/div[4]/div/div/ul/li[2]')
    ActionChains(browser_obj.driver).move_to_element(above).click(click_element).perform()  # 鼠标悬停后点击
    sleep(1)

    # 修改迭代标题
    # browser_obj.click((By.XPATH, '//*[@id="title"]'))
    # sleep(1)
    browser_obj.send_key((By.XPATH, '//*[@id="title"]'), Keys.CONTROL + 'a')  # 全选
    sleep(1)
    title = '自动化测试编辑迭代1'
    browser_obj.send_key((By.XPATH, '//*[@id="title"]'), title)

    # 修改迭代日期
    browser_obj.click((By.XPATH, '//*[@id="rangeTime"]'))
    sleep(1)
    browser_obj.click((By.XPATH, '//table/tbody/tr[2]/td[4]/div'))
    sleep(1)
    browser_obj.click((By.XPATH, '//div/div[2]/div/div[2]/table/tbody/tr[2]/td[6]/div'))
    sleep(1)

    browser_obj.click((By.XPATH, '//button/span[contains(., "保 存")]'))
    sleep(1)
    assert browser_obj.get_text(
        (By.XPATH, '//*[@role="tabpanel"]/div[2]/div/div/div[1]/div/div[1]/div/div[1]/div/div[1]/a')) == title


def test_jump_iteration(browser_obj):
    """
    测试迭代跳转
    :param browser_obj:
    :return:
    """
    browser_obj.click(
        (By.XPATH, '//*[@role="tabpanel"]/div[2]/div/div/div[1]/div/div[1]/div/div[1]/div/div[1]/a'))
    sleep(1)

    assert browser_obj.get_text(
        (By.XPATH, '//*[@id="root"]/section/section/header/div/div[1]/div/span[3]/span[1]/div')) == '迭代计划'
    assert browser_obj.get_text(
        (By.XPATH, '//*[@id="private-project"]/div[1]/div/div[3]/div[1]/button/span[2]')) == '新建事项'


def test_complete_iteration_wrongful(browser_obj):
    """
    完成迭代不合法
    :param browser_obj:
    :return:
    """
    above = browser_obj.find_element_by_xpath(
        '//*[@role="tabpanel"]/div[2]/div/div/div[1]/div/div[1]/div/div[1]/div/div[2]/span')
    ActionChains(browser_obj.driver).move_to_element(above).perform()  # 鼠标悬停
    click_element = browser_obj.find_element_by_xpath(
        '//*[@id="private-project"]/div[4]/div/div/ul/li[1]/span/span/span')
    ActionChains(browser_obj.driver).move_to_element(above).click(click_element).perform()  # 鼠标悬停后点击
    sleep(1)

    browser_obj.click((By.XPATH, '//button[2]/span[contains(., "确 定")]'))
    sleep(1)
    assert browser_obj.get_text(
        (By.XPATH, '//form/div[1]/div/div/div[2]/div[2]/div')) == '请选择迭代截止日期'

    browser_obj.click((By.XPATH, '//button[1]/span[contains(., "取 消")]'))
    sleep(1)


def test_complete_iteration(browser_obj):
    """
    测试完成迭代
    :param browser_obj:
    :return:
    """
    pass


def test_create_event_in_the_completed_iteration(browser_obj):
    """
    测试在已完成迭代中创建事项
    :param browser_obj:
    :return:
    """
    browser_obj.click((By.XPATH, '//*[@id="/dashboard$Menu"]/li[3]'))
    sleep(1)
    browser_obj.click((By.XPATH, '//*[@id="sprintStatus"]'))
    sleep(1)
    browser_obj.click((By.XPATH, '//*[@id="private-project"]/div[2]/div/div/div/div[2]/div[1]/div/div/div[3]/div'))
    sleep(1)
    browser_obj.click((By.XPATH, '//table/tbody/tr[1]/td[1]'))
    sleep(2)

    assert browser_obj.get_attribute((By.XPATH, '//*[@id="private-project"]/div/div/div[3]/div[1]/button'),
                                     'disabled') is not None


def test_delete_iteration(browser_obj):
    """
    测试删除迭代
    :param browser_obj:
    :return:
    """
    title = browser_obj.get_text(
        (By.XPATH, '//*[@role="tabpanel"]/div[2]/div/div/div[1]/div/div[1]/div/div[1]/div/div[1]/a'))
    above = browser_obj.find_element_by_xpath(
        '//*[@role="tabpanel"]/div[2]/div/div/div[1]/div/div[1]/div/div[1]/div/div[2]/span')
    ActionChains(browser_obj.driver).move_to_element(above).perform()  # 鼠标悬停
    click_element = browser_obj.find_element_by_xpath(
        '//*[@id="private-project"]/div[4]/div/div/ul/li[4]/span')
    ActionChains(browser_obj.driver).move_to_element(above).click(click_element).perform()  # 鼠标悬停后点击
    sleep(1)

    browser_obj.click((By.XPATH, '//button/span[contains(., "确 定")]'))
    sleep(1)
    assert browser_obj.get_text(
        (By.XPATH, '//*[@role="tabpanel"]/div[2]/div/div/div[1]/div/div[1]/div/div[1]/div/div[1]/a')) != title


def test_search_after_filter_event_types(browser_obj):
    """
    测试筛选事项类型后搜索
    :param browser_obj:
    :return:
    """
    # 筛选需求事项
    browser_obj.click((By.XPATH, '//form/div/div[1]/div/div[2]/div/div/div/div/span[2]'))
    sleep(1)
    browser_obj.click((By.XPATH, '//*[@id="private-project"]/div[4]/div/div/div/div[2]/div[1]/div/div/div[1]/div'))
    sleep(1)

    # 搜索
    browser_obj.send_key((By.XPATH, '//*[@id="keywords"]'), '完整事项')
    browser_obj.click((By.XPATH, '//div/div/div/div/span/span/span[2]/button'))
    sleep(1)

    browser_obj.click((By.XPATH, '//div[2]/div/div/div[1]/div/div/div/div[1]/div/div[1]/a'))
    sleep(1)

    assert browser_obj.get_text(
        (By.XPATH, '//*[@id="private-project"]/div[1]/div/div[4]/div/div/div[1]/div[2]/h3')) == '新建完整事项'


def test_iteration_basic_info_display(browser_obj):
    """
    测试进入迭代页面基本信息展示
    :param browser_obj:
    :return:
    """
    browser_obj.click((By.XPATH, '//div/div/div[1]/div/div/div/div[1]/div/div[1]/a'))
    sleep(2)

    text1 = browser_obj.get_text(
        (By.XPATH, '//*[@id="private-project"]/div/div/div[1]/div/div/span[2]/span[1]'))
    text2 = browser_obj.get_text(
        (By.XPATH, '//*[@id="private-project"]/div/div/div[1]/div/div/span[2]/span[2]'))

    assert '迭代时间' in text1 and '负责人' in text2


def test_event_priority_sort(browser_obj):
    """
    测试事项优先级排序
    :param browser_obj:
    :return:
    """
    browser_obj.click((By.XPATH, '//section/section/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div'))
    sleep(1)
    # 升序
    browser_obj.click((By.CSS_SELECTOR, 'span.anticon.anticon-caret-up.ant-table-column-sorter-up > svg'))
    sleep(1)
    tbody = browser_obj.find_element_by_xpath('//div[4]/div/div/div/div/div/table/tbody')
    tr_list = tbody.find_elements_by_xpath('tr')
    temp = []
    for tr in tr_list:
        text = tr.find_element_by_xpath('td[5]').text
        temp.append(text)
    next_button = browser_obj.find_element((By.XPATH, '//div[4]/div/div/ul/li[last()-1]/button'))
    val = next_button.get_attribute("disabled")
    while not val:
        next_button.click()
        sleep(1)
        tbody_n = browser_obj.find_element_by_xpath('//div[4]/div/div/div/div/div/table/tbody')
        tr_list_n = tbody_n.find_elements_by_xpath('tr')
        for tr in tr_list_n:
            text = tr.find_element_by_xpath('td[5]').text
            temp.append(text)
        val = next_button.get_attribute("disabled")
    logger.debug(len(temp))
    mapping = {
        '低': 1,
        '中': 2,
        '高': 3
    }
    check = list(map(lambda x: mapping[x], temp))
    logger.debug(temp)
    # 判断列表元素是否升序
    assert sorted(check) == check

    # 降序
    browser_obj.click((By.CSS_SELECTOR, 'span.anticon.anticon-caret-down.ant-table-column-sorter-down > svg'))
    sleep(10)
    tbody = browser_obj.find_element_by_xpath('//div[4]/div/div/div/div/div/table/tbody')
    tr_list = tbody.find_elements_by_xpath('tr')
    temp = []
    for tr in tr_list:
        text = tr.find_element_by_xpath('td[5]').text
        temp.append(text)
    next_button = browser_obj.find_element((By.XPATH, '//div[4]/div/div/ul/li[last()-1]/button'))
    val = next_button.get_attribute("disabled")
    while not val:
        next_button.click()
        sleep(1)
        tbody_n = browser_obj.find_element_by_xpath('//div[4]/div/div/div/div/div/table/tbody')
        tr_list_n = tbody_n.find_elements_by_xpath('tr')
        for tr in tr_list_n:
            text = tr.find_element_by_xpath('td[5]').text
            temp.append(text)
        val = next_button.get_attribute("disabled")
    logger.debug(len(temp))
    mapping = {
        '低': 1,
        '中': 2,
        '高': 3
    }
    check = list(map(lambda x: mapping[x], temp))
    logger.debug(temp)
    # 判断列表元素是否降序
    assert sorted(check, reverse=True) == check

    # 恢复初始页面
    browser_obj.click((By.CSS_SELECTOR, 'span.anticon.anticon-caret-down.ant-table-column-sorter-down > svg'))


def test_event_create_time_sort(browser_obj):
    """
    测试事项创建时间排序
    :param browser_obj:
    :return:
    """
    # 升序
    # browser_obj.click((By.XPATH, '//section/section/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div'))
    browser_obj.click((By.XPATH, '//section/section/main/div/div/div/div[1]/div[1]/div/div[2]/div'))
    sleep(1)
    browser_obj.click((By.XPATH, '//table/thead/tr/th[8]/div/div/span[2]/span/span[1]'))
    sleep(2)
    time_tds = browser_obj.find_elements((By.CSS_SELECTOR, 'td.ant-table-column-sort'))
    time_list = [td.text for td in time_tds]
    stamps = []
    for t in time_list:
        time_stamp = time.mktime(time.strptime(t, '%Y-%m-%d %H:%M:%S'))
        stamps.append(time_stamp)
    next_button = browser_obj.find_element((By.XPATH, '//div[4]/div/div/ul/li[last()-1]/button'))
    val = next_button.get_attribute("disabled")
    while not val:
        next_button.click()
        sleep(1)
        time_tds_n = browser_obj.find_elements((By.CSS_SELECTOR, 'td.ant-table-column-sort'))
        time_list_n = [td.text for td in time_tds_n]
        for t in time_list_n:
            time_stamp = time.mktime(time.strptime(t, '%Y-%m-%d %H:%M:%S'))
            stamps.append(time_stamp)
        val = next_button.get_attribute("disabled")
    logger.debug(stamps)
    # 断言
    assert sorted(stamps) == stamps

    # 降序
    browser_obj.click((By.XPATH, '//table/thead/tr/th[8]/div/div/span[2]/span/span[2]'))
    sleep(2)
    time_tds = browser_obj.find_elements((By.CSS_SELECTOR, 'td.ant-table-column-sort'))
    time_list = [td.text for td in time_tds]
    stamps = []
    for t in time_list:
        time_stamp = time.mktime(time.strptime(t, '%Y-%m-%d %H:%M:%S'))
        stamps.append(time_stamp)
    next_button = browser_obj.find_element((By.XPATH, '//div[4]/div/div/ul/li[last()-1]/button'))
    val = next_button.get_attribute("disabled")
    while not val:
        next_button.click()
        sleep(1)
        time_tds_n = browser_obj.find_elements((By.CSS_SELECTOR, 'td.ant-table-column-sort'))
        time_list_n = [td.text for td in time_tds_n]
        for t in time_list_n:
            time_stamp = time.mktime(time.strptime(t, '%Y-%m-%d %H:%M:%S'))
            stamps.append(time_stamp)
        val = next_button.get_attribute("disabled")
    logger.debug(stamps)

    # 恢复初始页面
    browser_obj.click((By.XPATH, '//table/thead/tr/th[8]/div/div/span[2]/span/span[2]'))


def test_create_event_legal(browser_obj):
    """
    测试创建事项合法
    :param browser_obj:
    :return:
    """
    # 进入全部事项页
    # browser_obj.click((By.XPATH, '//section/section/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div'))
    browser_obj.click((By.XPATH, '//section/section/main/div/div/div/div[1]/div[1]/div/div[2]/div'))
    sleep(1)
    # 创建事项
    browser_obj.click((By.XPATH, '//button/span[contains(., "创建事项")]'))
    sleep(1)
    # 输入事项标题
    title = '创建合法事项1'
    browser_obj.send_key((By.XPATH, '//*[@id="issueTitle"]'), title)
    # 选择事项类型（任务）
    browser_obj.click(
        (By.XPATH, '//*[@id="drawerBody"]/form/div[1]/div[2]/div[1]/div[2]/div/div[2]/div/div/div/div/span[2]'))
    sleep(1)
    browser_obj.click((By.XPATH, '//*[@id="drawerBody"]/div[1]/div/div/div/div[2]/div[1]/div/div/div[2]/div'))
    sleep(1)
    # 选择优先级(高)
    browser_obj.click((By.XPATH, '//*[@id="priority"]/label[3]/span[2]'))
    sleep(1)
    # 点击确定，创建事项
    browser_obj.click((By.XPATH, '//div[2]/button/span[contains(., "确 定")]'))
    sleep(2)
    # browser_obj.click((By.CSS_SELECTOR, 'div.ant-drawer-header > button > span'))
    # sleep(1)
    # 断言
    assert browser_obj.get_text((By.XPATH, '//table/tbody/tr[1]/td[3]/div/span')) == title


def test_edit_event_legal(browser_obj):
    """
    测试编辑事项信息合法
    :param browser_obj:
    :return:
    """
    # 进入全部事项页
    # browser_obj.click((By.XPATH, '//section/section/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div'))
    browser_obj.click((By.XPATH, '//section/section/main/div/div/div/div[1]/div[1]/div/div[2]/div'))
    sleep(1)

    browser_obj.click((By.XPATH, '//table/tbody/tr[1]/td[3]/div'))
    sleep(1)
    assert browser_obj.get_text(
        (By.XPATH, '//div/div/div[2]/div[5]/label')) == '隐藏详情'
    # 修改事项基础信息(优先级 高 --》 低)
    element = browser_obj.driver.find_element_by_css_selector('.ant-col:nth-child(1) > .ant-row .editCell___3icLl')
    ActionChains(browser_obj.driver).double_click(element).perform()  # 双击
    sleep(1)
    priority = browser_obj.get_text((By.XPATH, '//div[2]/div/div/div/div[2]/div/div/div/div/div'))
    browser_obj.click((By.XPATH, '//div[2]/div/div/div/div[2]/div/div/div/div/div'))
    sleep(1)

    # 修改事项状态
    browser_obj.click((By.XPATH, '//*[@id="drawerBody"]/div[1]/div/form/div[2]/div[1]/div/div/div/div/span[2]'))
    sleep(1)
    status = browser_obj.get_text(
        (By.XPATH, '//*[@id="drawerBody"]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div'))
    browser_obj.click((By.XPATH, '//*[@id="drawerBody"]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div'))
    sleep(1)

    browser_obj.click((By.XPATH, '//button/span[contains(.,"取 消")]'))
    sleep(1)

    # 断言
    assert browser_obj.get_text((By.XPATH, '//table/tbody/tr[1]/td[5]')) == priority.strip()
    assert browser_obj.get_text((By.XPATH, '//table/tbody/tr[1]/td[6]')) == status.strip()


def test_event_data_paging_view(browser_obj):
    """
    测试事项数据统计分页查看
    :param browser_obj:
    :return:
    """

    # 进入全部事项页
    browser_obj.click((By.XPATH, '//section/section/main/div/div/div/div[1]/div[1]/div/div[2]/div'))
    sleep(1)

    # 默认页查看数据统计
    def test_paging():
        total = browser_obj.get_text((By.XPATH, '//div[4]/div/div/ul/li[1]'))
        total = re.search('\d+', total).group()
        per_num = browser_obj.get_text((By.XPATH, '//div[4]/div/div/ul/li[last()]/div[1]/div[1]/span[2]'))
        per_num = re.search('\d+', per_num).group()
        pages = browser_obj.get_text((By.XPATH, '//div[4]/div/div/ul/li[last()-2]/a'))

        temp1 = int(total) % int(per_num)
        temp2 = int(total) / int(per_num)
        if temp1:
            assert int(pages) == int(temp2) + 1
        else:
            assert int(pages) == int(temp2)

    test_paging()

    # 选择每页显示数据（20条/页）查看数据统计
    browser_obj.click((By.XPATH, '//div[4]/div/div/ul/li[last()]/div[1]/div[1]/span[2]'))
    sleep(1)
    browser_obj.click((By.XPATH, '//div/div/ul/li[last()]/div[1]/div[2]/div/div/div/div[2]/div/div/div/div[2]/div'))
    sleep(2)
    test_paging()


def test_requirement_info_display(browser_obj):
    """
    测试事项（需求）信息展示
    :param browser_obj:
    :return:
    """
    # 进入需求页
    browser_obj.click((By.XPATH, '//section/section/main/div/div/div/div[1]/div[1]/div/div[3]/div'))
    sleep(1)

    assert browser_obj.get_text((By.XPATH, '//div[3]/div[1]/div/div[4]/div/button[1]/span[2]')) == '创建需求'


def test_create_requirement_legal(browser_obj):
    """
    测试创建需求合法
    :param browser_obj:
    :return:
    """
    # 进入需求页
    browser_obj.click((By.XPATH, '//section/section/main/div/div/div/div[1]/div[1]/div/div[3]/div'))
    sleep(1)

    # 创建需求
    browser_obj.click((By.XPATH, '//button[1]/span[contains(., "创建需求")]'))
    sleep(1)
    # 输入标题
    title = '创建需求1'
    browser_obj.send_key((By.XPATH, '//*[@id="issueTitle"]'), title)
    # 选择优先级（高）
    browser_obj.click((By.XPATH, '//*[@id="priority"]/label[3]'))
    sleep(1)

    browser_obj.click((By.XPATH, '//button/span[contains(., "确 定")]'))
    sleep(2)
    browser_obj.click((By.XPATH, '//button/span[contains(., "取 消")]'))
    sleep(1)

    assert browser_obj.get_text((By.XPATH, '//table/tbody/tr[1]/td[3]/div/span')) == title


def test_edit_requirement_legal(browser_obj):
    """
    测试编辑需求合法
    :param browser_obj:
    :return:
    """
    # 进入需求页
    browser_obj.click((By.XPATH, '//section/section/main/div/div/div/div[1]/div[1]/div/div[3]/div'))
    sleep(1)

    # 进入此需求
    browser_obj.click((By.XPATH, '//table/tbody/tr[1]/td[3]/div'))
    sleep(1)

    # 修改需求标题
    browser_obj.click((By.CSS_SELECTOR, '.ant-col:nth-child(1) > .ant-form-item-control-input .editCell___3icLl'))
    sleep(1)
    browser_obj.send_key((By.CSS_SELECTOR, '#issueTitle'), Keys.CONTROL + 'a')
    title = '修改需求标题'
    browser_obj.send_key((By.CSS_SELECTOR, '#issueTitle'), title)

    # 修改需求状态
    browser_obj.click((By.XPATH, '//form/div[2]/div[1]/div/div/div/div/span[2]'))
    sleep(1)
    status = browser_obj.get_text(
        (By.XPATH, '//*[@id="drawerBody"]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div'))
    browser_obj.click((By.XPATH, '//*[@id="drawerBody"]/div[2]/div/div/div/div[2]/div[1]/div/div/div[2]/div'))
    sleep(1)

    # 修改需求优先级
    priority = browser_obj.get_text(
        (By.XPATH, '//form/div[4]/div[1]/div/div[2]/div/div/div[1]/div/div/span/div/div[2]/div/div/div'))
    element = browser_obj.driver.find_element_by_xpath(
        '//form/div[4]/div[1]/div/div[2]/div/div/div[1]/div/div/span/div/div[2]/div/div/div')
    ActionChains(browser_obj.driver).double_click(element).perform()  # 双击
    sleep(1)
    browser_obj.click((By.XPATH, '//div[2]/div/div/div/div[2]/div/div/div/div/div[2]'))
    sleep(5)
    browser_obj.click((By.XPATH, '//button/span[contains(., "取 消")]'))
    sleep(1)

    assert browser_obj.get_text((By.XPATH, '//table/tbody/tr[1]/td[3]/div/span')) == title
    assert browser_obj.get_text((By.XPATH, '//table/tbody/tr[1]/td[6]')) == status.strip()
    assert browser_obj.get_text((By.XPATH, '//table/tbody/tr[1]/td[5]')) == priority.strip()


def test_delete_requirement(browser_obj):
    """
    测试删除需求
    :param browser_obj:
    :return:
    """
    # 获取将要删除的需求id
    require_id = browser_obj.get_text((By.XPATH, '//table/tbody/tr[1]/td[2]/a')).split('#')[-1]
    # 进入此需求
    browser_obj.click((By.XPATH, '//table/tbody/tr[1]/td[3]/div'))
    sleep(1)
    # 删除
    browser_obj.click((By.XPATH, '/html/body/div[3]/div/div/div/div/div[1]/div/div/div[2]/div[3]/div[3]/div[2]/span'))
    sleep(1)
    # 确认删除
    browser_obj.click((By.XPATH, '//button[2]/span[contains(., "删 除")]'))
    sleep(1)
    assert browser_obj.get_text((By.XPATH, '//table/tbody/tr[1]/td[2]/a')).split('#')[-1] != require_id


def test_requirements_page_refresh(browser_obj):
    """
    测试需求页面刷新
    :param browser_obj:
    :return:
    """
    # 进入需求页
    browser_obj.click((By.XPATH, '//section/section/main/div/div/div/div[1]/div[1]/div/div[3]/div'))
    sleep(1)

    # 进行条件筛选（暂时只验证根据状态进行筛选，后续可补充）
    browser_obj.click((By.XPATH, '//form/div/div[1]/div/div[1]/div/div/div/div[2]/div/div/div/div/span[2]'))
    sleep(1)
    status = browser_obj.get_text(
        (By.XPATH, '//*[@id="private-project"]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div')).strip()
    browser_obj.click((By.XPATH, '//*[@id="private-project"]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div'))
    sleep(1)

    # 点击刷新
    browser_obj.click((By.XPATH, '//button/span[2][contains(., "刷新")]/..'))
    sleep(1)

    # 检测刷新后不会清除筛选状态
    assert browser_obj.get_text(
        (By.XPATH, '//form/div/div[1]/div/div[1]/div/div/div/div[2]/div/div/div/div/span[1]/span[1]')) == status

    # 检测根据筛选条件, 显示结果正确
    tbody = browser_obj.find_element_by_xpath('//div[4]/div/div/div/div/div/table/tbody')
    first_td = tbody.find_element_by_xpath('tr[1]/td[1]').text
    if first_td != '暂无数据':
        tr_list = tbody.find_elements_by_xpath('tr')
        temp = []
        for tr in tr_list:
            text = tr.find_element_by_xpath('td[6]').text
            temp.append(text)
        next_button = browser_obj.find_element((By.XPATH, '//div[4]/div/div/ul/li[last()-1]/button'))
        val = next_button.get_attribute("disabled")
        while not val:
            next_button.click()
            sleep(1)
            tbody_n = browser_obj.find_element_by_xpath('//div[4]/div/div/div/div/div/table/tbody')
            tr_list_n = tbody_n.find_elements_by_xpath('tr')
            for tr in tr_list_n:
                text = tr.find_element_by_xpath('td[6]').text
                temp.append(text)
            val = next_button.get_attribute("disabled")
        for i in temp:
            assert i == status


def test_requirements_reset_query(browser_obj):
    """
    测试需求重置查询条件
    :param browser_obj:
    :return:
    """
    # 进入需求页
    browser_obj.click((By.XPATH, '//section/section/main/div/div/div/div[1]/div[1]/div/div[3]/div'))
    sleep(1)

    # 进行一些条件筛选查询
    # 状态筛选
    browser_obj.click((By.XPATH, '//form/div/div[1]/div/div[1]/div/div/div/div[2]/div/div/div/div/span[2]'))
    sleep(1)
    browser_obj.click((By.XPATH, '//*[@id="private-project"]/div[2]/div/div/div/div[2]/div[1]/div/div/div[1]/div'))
    sleep(1)
    # 优先级筛选
    browser_obj.click((By.XPATH, '//*[@id="priorityCode"]'))
    sleep(1)
    browser_obj.click((By.XPATH, '//*[@id="private-project"]/div[*]/div/div/div/div[2]/div[1]/div/div/div[1]/div'))
    sleep(1)

    # 重置条件查询
    browser_obj.click((By.XPATH, '//button/span[contains(., "重置查询")]'))
    sleep(1)

    #
    assert browser_obj.get_text(
        (By.XPATH, '//form/div/div[1]/div/div[1]/div/div/div/div[2]/div/div/div/div/span[2]')) == '请选择'
    assert browser_obj.get_text(
        (By.XPATH, '//form/div/div[4]/div/div[1]/div/div/div/div[2]/div/div/div/div/span[2]')) == '请选择'


def test_requirements_priority_sort(browser_obj):
    """
    测试需求优先级排序
    :param browser_obj:
    :return:
    """
    # 进入需求页
    browser_obj.click((By.XPATH, '//section/section/main/div/div/div/div[1]/div[1]/div/div[3]/div'))
    sleep(1)

    # 升序
    browser_obj.click((By.CSS_SELECTOR, 'tr > th:nth-child(5) span.anticon-caret-up > svg'))
    sleep(1)

    def priority_sort_list():
        tbody = browser_obj.find_element_by_xpath('//div[4]/div/div/div/div/div/table/tbody')
        first_td = tbody.find_element_by_xpath('tr[1]/td[1]').text
        if first_td != '暂无数据':
            tr_list = tbody.find_elements_by_xpath('tr')
            temp = []
            for tr in tr_list:
                text = tr.find_element_by_xpath('td[5]').text
                temp.append(text)
            next_button = browser_obj.find_element((By.XPATH, '//div[4]/div/div/ul/li[last()-1]/button'))
            val = next_button.get_attribute("disabled")
            while not val:
                next_button.click()
                sleep(1)
                tbody_n = browser_obj.find_element_by_xpath('//div[4]/div/div/div/div/div/table/tbody')
                tr_list_n = tbody_n.find_elements_by_xpath('tr')
                for tr in tr_list_n:
                    text = tr.find_element_by_xpath('td[5]').text
                    temp.append(text)
                val = next_button.get_attribute("disabled")
            logger.debug(temp)
            mapping = {
                '低': 1,
                '中': 2,
                '高': 3
            }
            return list(map(lambda x: mapping[x], temp))

    # 判断列表元素是否升序
    li = priority_sort_list()
    assert sorted(li) == li

    # 降序
    browser_obj.click((By.CSS_SELECTOR, 'tr > th:nth-child(5) span.anticon-caret-down > svg'))
    sleep(1)
    # 判断列表元素是否降序
    li = priority_sort_list()
    assert sorted(li, reverse=True) == li


def test_requirements_create_time_sort(browser_obj):
    """
    测试需求创建时间排序
    :param browser_obj:
    :return:
    """
    # 进入需求页
    browser_obj.click((By.XPATH, '//section/section/main/div/div/div/div[1]/div[1]/div/div[3]/div'))
    sleep(1)

    # 升序
    browser_obj.click((By.CSS_SELECTOR, 'tr > th:nth-child(8) span.anticon-caret-up > svg'))
    sleep(1)

    def create_time_sort_list():
        tbody = browser_obj.find_element_by_xpath('//div[4]/div/div/div/div/div/table/tbody')
        first_td = tbody.find_element_by_xpath('tr[1]/td[1]').text
        if first_td != '暂无数据':
            time_tds = browser_obj.find_elements((By.CSS_SELECTOR, 'td.ant-table-column-sort'))
            time_list = [td.text for td in time_tds]
            temp = []
            for t in time_list:
                time_stamp = time.mktime(time.strptime(t, '%Y-%m-%d %H:%M:%S'))
                temp.append(time_stamp)
            next_button = browser_obj.find_element((By.XPATH, '//div[4]/div/div/ul/li[last()-1]/button'))
            val = next_button.get_attribute("disabled")
            while not val:
                next_button.click()
                sleep(1)
                time_tds = browser_obj.find_elements((By.CSS_SELECTOR, 'td.ant-table-column-sort'))
                time_list = [td.text for td in time_tds]
                for t in time_list:
                    time_stamp = time.mktime(time.strptime(t, '%Y-%m-%d %H:%M:%S'))
                    temp.append(time_stamp)
                val = next_button.get_attribute("disabled")
            return temp

    # 判断列表元素是否升序
    li = create_time_sort_list()
    assert sorted(li) == li

    # 降序
    browser_obj.click((By.CSS_SELECTOR, 'tr > th:nth-child(8) span.anticon-caret-down > svg'))
    sleep(1)
    # 判断列表元素是否降序
    li = create_time_sort_list()
    assert sorted(li, reverse=True) == li
