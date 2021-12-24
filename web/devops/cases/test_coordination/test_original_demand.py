import re
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from utils.times import sleep
from libs.log_obj import LogObj

logger = LogObj().get_logger()


@pytest.fixture(scope='function', autouse=True)
def enter_original_demand(browser_obj):
    # 进入原始需求初始页面
    browser_obj.find_element(
        (By.XPATH, '//*[@id="/dashboard$Menu"]/li[1]/a')).click()
    sleep(4)


@pytest.mark.run(order=1)
def test_new_requirement_islegal(browser_obj):
    """
    测试新建需求是否合法
    :param browser_obj:
    :return:
    """
    browser_obj.click((By.XPATH, '//*[@id="private-project"]/div[2]/div/div[1]/div[1]/div/div[2]/span/button'))
    sleep(0.1)
    # 1.添加需求概览
    overviews = '自动化测试新建需求'
    browser_obj.send_key((By.XPATH, '//*[@id="summarize"]'), overviews)
    # 2.添加需求描述
    describe = '自动化测试新建需求描述'
    browser_obj.send_key((By.CSS_SELECTOR, '.notranslate'), describe)
    time.sleep(0.1)
    # 3. 添加需求来源
    source = '外部客户'
    browser_obj.send_key((By.XPATH, '//*[@id="source"]'), source)
    browser_obj.click((By.XPATH, '/html/body/div[2]/div/div[2]/div/div/div[3]/div/div[2]/div/div[2]/button'))
    sleep(0.1)
    # 刷新下页面
    browser_obj.script('location.reload()')
    assert browser_obj.get_text(
        (By.XPATH,
         '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[2]/a/div')) == overviews


@pytest.mark.run(order=2)
def test_edit_requirement_islegal(browser_obj):
    """
    测试编辑需求是否合法
    :param browser_obj:
    :return:
    """
    # 点击需求概览进项进入编辑
    browser_obj.click(
        (By.XPATH, '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[2]/a/div'))
    sleep(1)
    # 1.编辑需求概述
    browser_obj.click(
        (By.XPATH, '//*[@id="drawerBody"]/form/div[1]/div[1]/div/div[1]/span/div/div[2]/div/div/div'))
    sleep(1)
    browser_obj.script('document.getElementById("summarize").value = "";')
    browser_obj.find_element((By.XPATH, '//*[@id="summarize"]')).send_keys('编辑自动化测试新建需求概述')
    sleep(1)
    browser_obj.click((By.XPATH, '//*[@id="drawerBody"]/form/div[1]/div[1]/div/div[2]/span[1]'))
    sleep(1)
    # 刷新下页面
    browser_obj.click((By.XPATH, '//*[@id="private-project"]/div[2]/div/div[1]/div[1]/div/div[3]/button'))
    sleep(1)
    # 断言判断
    assert browser_obj.get_text(
        (By.XPATH,
         '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[2]/a/div')) == \
           '编辑自动化测试新建需求概述'


@pytest.mark.run(order=3)
def test_modify_requirement(browser_obj):
    """
    测试修改需求
    :param browser_obj:
    :return:
    """
    browser_obj.click(
        (By.XPATH, '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[2]/a/div'))
    sleep(1)
    browser_obj.click(
        (By.XPATH, '//*[@id="drawerBody"]/form/div[1]/div[1]/div/div[1]/span/div/div[2]/div/div/div'))
    sleep(1)
    browser_obj.script('document.getElementById("summarize").value = "";')
    browser_obj.find_element((By.XPATH, '//*[@id="summarize"]')).send_keys('修改自动化测试新建需求概述')
    sleep(1)
    browser_obj.click((By.XPATH, '//*[@id="drawerBody"]/form/div[1]/div[1]/div/div[2]/span[1]'))
    sleep(1)
    # 刷新下页面
    browser_obj.click((By.XPATH, '//*[@id="private-project"]/div[2]/div/div[1]/div[1]/div/div[3]/button'))
    sleep(1)
    # 断言判断
    assert browser_obj.get_text(
        (By.XPATH,
         '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[2]/a/div')) == \
           '修改自动化测试新建需求概述'


@pytest.mark.run(order=4)
def test_delete_requirement(browser_obj):
    """
    测试删除原始需求
    :param browser_obj:
    :return:
    """

    require_id = browser_obj.get_text(
        (By.XPATH,
         '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]/button/span'))

    browser_obj.click(
        (By.XPATH,
         '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]/button'))
    sleep(1)
    browser_obj.click(
        (By.CSS_SELECTOR,
         '.ant-btn-primary.ant-btn-dangerous'))
    sleep(1)
    browser_obj.click(
        (By.CSS_SELECTOR,
         'div > div.ant-modal-confirm-btns > button.ant-btn.ant-btn-primary'))
    sleep(1)
    check_point = browser_obj.get_text(
        (By.XPATH,
         '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]/button/span'))

    assert require_id != check_point


@pytest.mark.run(order=5)
def test_handle_requirement(browser_obj):
    """
    测试处理原始需求
    :param browser_obj:
    :return:
    """
    # 需求接受
    # 第一种：将需求添加到待办事项
    # 1.新建一个需求
    browser_obj.click((By.XPATH, '//*[@id="private-project"]/div[2]/div/div[1]/div[1]/div/div[2]/span/button'))
    sleep(1)
    overviews = '新建需求'
    browser_obj.send_key((By.XPATH, '//*[@id="summarize"]'), overviews)
    browser_obj.click((By.XPATH, '//span[contains(.,"确 定")]'))
    sleep(1)
    # 2.点击此需求
    browser_obj.click((By.CSS_SELECTOR, '.ant-table-row:nth-child(1) .ant-btn > span'))
    # 3.点击接纳
    browser_obj.click((By.XPATH, '//span[contains(.,"接 纳")]'))
    sleep(1)
    # 4.添加至待办事项(默认)
    # 5.点击需求反馈，添加反馈内容
    browser_obj.click((By.CSS_SELECTOR, '.ant-form-item-control-input-content > .ant-input'))
    sleep(1)
    content = '添加此需求到待办事项'
    browser_obj.send_key((By.CSS_SELECTOR, '.ant-form-item-control-input-content > .ant-input'), content)
    sleep(1)
    # 6.点击确定
    browser_obj.click((By.CSS_SELECTOR, '.ant-col:nth-child(3) > .ant-btn-primary > span'))
    sleep(1)
    # 7.断言判断
    check = browser_obj.get_text(
        (
            By.XPATH,
            '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[3]/div/a/div'))
    assert check == '未开始'

    # 第二种：将需求关联至已有卡片
    # 1.新建一个需求
    browser_obj.click((By.XPATH, '//*[@id="private-project"]/div[2]/div/div[1]/div[1]/div/div[2]/span/button'))
    sleep(1)
    overviews = '阿大撒'
    browser_obj.send_key((By.XPATH, '//*[@id="summarize"]'), overviews)
    browser_obj.click((By.XPATH, '//span[contains(.,"确 定")]'))
    sleep(1)
    # 2.点击此需求
    browser_obj.click((By.CSS_SELECTOR, '.ant-table-row:nth-child(1) .ant-btn > span'))
    # 3.点击接纳
    browser_obj.click((By.XPATH, '//span[contains(.,"接 纳")]'))
    sleep(1)
    # 4.添加需求关联卡片，输入关联的需求项
    browser_obj.click((By.CSS_SELECTOR, '.ant-col > .ant-radio-wrapper > span:nth-child(1)'))
    sleep(1)
    browser_obj.click((By.XPATH, '//div[2]/div/div/span/input'))
    sleep(1)
    browser_obj.click((By.XPATH, '//span[contains(.,"新建需求")]'))
    sleep(1)
    # 5.点击需求反馈，添加反馈内容
    browser_obj.click((By.CSS_SELECTOR, '.ant-form-item-control-input-content > .ant-input'))
    sleep(1)
    content = '关联需求'
    browser_obj.send_key((By.CSS_SELECTOR, '.ant-form-item-control-input-content > .ant-input'), content)
    sleep(1)
    # 6.点击确定
    browser_obj.click((By.CSS_SELECTOR, '.ant-col:nth-child(3) > .ant-btn-primary > span'))
    sleep(1)
    # 7.断言判断
    browser_obj.click((By.CSS_SELECTOR, '.ant-table-row:nth-child(1) .ant-btn > span'))
    sleep(1)
    check = browser_obj.get_text((By.XPATH, '//*[@id="drawerBody"]/form/div[1]/div[9]/div/div[1]/label'))
    assert check == '已关联事项'

    # 第三种：将需求标记为已完成
    # 1.新建一个需求
    browser_obj.click((By.XPATH, '//*[@id="private-project"]/div[2]/div/div[1]/div[1]/div/div[2]/span/button'))
    sleep(1)
    overviews = '新建需求'
    browser_obj.send_key((By.XPATH, '//*[@id="summarize"]'), overviews)
    browser_obj.click((By.XPATH, '//span[contains(.,"确 定")]'))
    sleep(1)
    # 2.点击此需求
    browser_obj.click((By.CSS_SELECTOR, '.ant-table-row:nth-child(1) .ant-btn > span'))
    # 3.点击接纳
    browser_obj.click((By.XPATH, '//span[contains(.,"接 纳")]'))
    sleep(4)
    # 4.标记为已完成
    # browser_obj.click((By.CSS_SELECTOR, '.ant-radio-wrapper:nth-child(3) .ant-radio-inner'))
    browser_obj.click((By.XPATH, '//label[2]/span'))
    sleep(1)
    # 5.点击需求反馈，输入反馈内容
    browser_obj.click((By.CSS_SELECTOR, '.ant-form-item-control-input-content > .ant-input'))
    sleep(1)
    content = '接受此需求'
    browser_obj.send_key((By.CSS_SELECTOR, '.ant-form-item-control-input-content > .ant-input'), content)
    sleep(1)
    # 6.点击确定
    browser_obj.click((By.CSS_SELECTOR, '.ant-col:nth-child(3) > .ant-btn-primary > span'))
    sleep(1)
    # 7.断言判断
    check = browser_obj.get_text(
        (
            By.XPATH,
            '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[3]/div/a/div'))
    assert check == '已完成'

    # 拒绝需求
    # 1.新建一个需求
    browser_obj.click((By.XPATH, '//*[@id="private-project"]/div[2]/div/div[1]/div[1]/div/div[2]/span/button'))
    sleep(1)
    overviews = '新建需求'
    browser_obj.send_key((By.XPATH, '//*[@id="summarize"]'), overviews)
    browser_obj.click((By.XPATH, '//span[contains(.,"确 定")]'))
    sleep(1)
    # 2.点击此需求
    browser_obj.click((By.CSS_SELECTOR, '.ant-table-row:nth-child(1) .ant-btn > span'))
    # 3.点击拒绝
    browser_obj.click((By.XPATH, '//span[contains(.,"拒 绝")]'))
    sleep(1)
    browser_obj.click((By.XPATH, '//span[contains(.,"确 定")]'))
    sleep(1)
    # 4.断言判断
    check = browser_obj.get_text(
        (
            By.XPATH,
            '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[3]/div/a/div'))
    assert check == '已拒绝'


def test_find_original_requirements(browser_obj):
    """
    测试查找原始需求
    :param browser_obj:
    :return:
    """
    # 1.通过需求编号查询
    search_input = browser_obj.find_element(
        (By.XPATH, '//*[@id="private-project"]/div[2]/div/div[1]/div[1]/div/div[1]/span/span/input'))
    search_button = browser_obj.find_element(
        (By.XPATH, '//*[@id="private-project"]/div[2]/div/div[1]/div[1]/div/div[1]/span/span/span/button'))

    require_id = browser_obj.find_element(
        (By.XPATH,
         '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]/button/span')).text
    search_input.send_keys(require_id)
    search_button.click()
    sleep(0.1)
    assert browser_obj.find_element(
        (By.XPATH,
         '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody/tr/td[1]/button/span')).text \
           == require_id
    # 清空查找框
    js = 'document.getElementsByTagName("input")[0].value="";'
    browser_obj.script(js)

    # 2.通过需求概览查询
    require_overview = browser_obj.find_element(
        (By.XPATH,
         '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[2]/a/div')).text
    search_input.send_keys(require_overview)
    search_button.click()
    sleep(0.1)
    assert browser_obj.find_element(
        (By.XPATH,
         '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody/tr/td[2]/a/div')).text \
           == require_overview
    browser_obj.script(js)

    # 3.通过创建人查询
    require_creater = browser_obj.find_element(
        (By.XPATH,
         '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[5]')).text
    search_input.send_keys(require_creater)
    search_button.click()
    sleep(0.1)
    assert browser_obj.find_element(
        (By.XPATH,
         '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[5]')).text \
           == require_creater
    browser_obj.script(js)


def test_find_requirement_by_keyword(browser_obj):
    """
    测试通过关键字查找原始需求（模糊查找）
    :param browser_obj:
    :return:
    """
    # 1.通过需求编号关键字查找
    require_id = browser_obj.get_text(
        (By.XPATH,
         '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]/button/span'))
    browser_obj.click((By.XPATH, '//*[@id="private-project"]/div[2]/div/div[1]/div[1]/div/div[1]/span/span/input'))
    sleep(0.1)
    browser_obj.send_key((By.XPATH, '//*[@id="private-project"]/div[2]/div/div[1]/div[1]/div/div[1]/span/span/input'),
                         require_id.split('-')[-1])
    browser_obj.click(
        (By.XPATH, '//*[@id="private-project"]/div[2]/div/div[1]/div[1]/div/div[1]/span/span/span/button'))
    sleep(0.1)
    text = browser_obj.get_text(
        (By.XPATH,
         '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]/button/span'))
    assert text == require_id
    js = 'document.getElementsByTagName("input")[0].value="";'
    browser_obj.script(js)
    # 2.通过需求概览关键字查找
    require_overview = browser_obj.get_text(
        (By.XPATH,
         '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[2]/a/div'))
    browser_obj.click((By.XPATH, '//*[@id="private-project"]/div[2]/div/div[1]/div[1]/div/div[1]/span/span/input'))
    sleep(0.1)
    browser_obj.send_key((By.XPATH, '//*[@id="private-project"]/div[2]/div/div[1]/div[1]/div/div[1]/span/span/input'),
                         require_overview[:len(require_overview) - 1])
    browser_obj.click(
        (By.XPATH, '//*[@id="private-project"]/div[2]/div/div[1]/div[1]/div/div[1]/span/span/span/button'))
    sleep(0.1)
    text = browser_obj.get_text(
        (By.XPATH,
         '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[2]/a/div'))
    assert text == require_overview


def test_original_requirements_paging_info(browser_obj):
    """
    测试原始需求分页信息
    :param browser_obj:
    :return:
    """
    total_str = browser_obj.get_text(
        (By.XPATH, '//*[@id="private-project"]/div[2]/div/div[2]/div/div/ul/li[1]'))
    total = re.search('\d+', total_str).group()

    per_str = browser_obj.get_attribute(
        (By.XPATH, '//*[@id="private-project"]/div[2]/div/div[2]/div/div/ul/li[last()]/div[1]/div[1]/span[2]'), 'title')
    per = re.search('\d+', per_str).group()

    pages_str = browser_obj.get_attribute(
        (By.XPATH, '//*[@id="private-project"]/div[2]/div/div[2]/div/div/ul/li[last()-2]'), 'title')
    pages = re.search('\d+', pages_str).group()
    result = int(total) / int(per)
    remainder = int(total) % int(per)
    if remainder == 0:
        assert int(pages) == int(result)
    else:
        assert int(pages) == int(result) + 1


def test_status_filter(browser_obj):
    """
    测试需求状态筛选
    :param browser_obj:
    :return:
    """
    # 筛选待处理状态的需求
    browser_obj.click((By.CSS_SELECTOR, '.anticon-filter path'))
    sleep(1)
    browser_obj.click((By.XPATH, '//li[1]/label/span/input'))
    sleep(1)
    browser_obj.click((By.CSS_SELECTOR, '.ant-btn:nth-child(2) > span'))
    sleep(1)
    tbody = browser_obj.find_element_by_xpath(
        '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody')
    tr_list = tbody.find_elements_by_xpath('tr')
    temp = []
    for tr in tr_list:
        status_val = tr.find_element_by_xpath('td[3]/div/a/div').text
        temp.append(status_val)
    next_button = browser_obj.find_element(
        (By.XPATH, '//*[@id="private-project"]/div[2]/div/div[2]/div/div/ul/li[last()-1]/button'))
    val = next_button.get_attribute("disabled")
    while not val:
        next_button.click()
        sleep(1)
        tbody_n = browser_obj.find_element_by_xpath(
            '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody')
        tr_list_n = tbody_n.find_elements_by_xpath('tr')
        for tr in tr_list_n:
            status_val = tr.find_element_by_xpath('td[3]/div/a/div').text
            temp.append(status_val)
        val = next_button.get_attribute("disabled")
    logger.debug(len(temp))
    check = [i for i in temp if i != '待处理']
    assert check == []

    # 恢复初始页面
    browser_obj.click((By.CSS_SELECTOR, '.anticon-filter path'))
    sleep(1)
    browser_obj.click((By.CSS_SELECTOR, '.ant-btn-sm:nth-child(1) > span'))


def test_priority_filter(browser_obj):
    """
    测试需求优先级筛选
    :param browser_obj:
    :return:
    """
    # 升序
    browser_obj.click((By.CSS_SELECTOR, '.ant-table-column-sorter-up > svg'))
    sleep(1)
    tbody = browser_obj.find_element_by_xpath(
        '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody')
    tr_list = tbody.find_elements_by_xpath('tr')
    temp = []
    for tr in tr_list:
        text = tr.find_element_by_xpath('td[4]').text
        temp.append(text)
    next_button = browser_obj.find_element(
        (By.XPATH, '//*[@id="private-project"]/div[2]/div/div[2]/div/div/ul/li[last()-1]/button'))
    val = next_button.get_attribute("disabled")
    while not val:
        next_button.click()
        sleep(1)
        tbody_n = browser_obj.find_element_by_xpath(
            '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody')
        tr_list_n = tbody_n.find_elements_by_xpath('tr')
        for tr in tr_list_n:
            text = tr.find_element_by_xpath('td[4]').text
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
    browser_obj.click((By.CSS_SELECTOR, '.ant-table-column-sorter-down > svg'))
    sleep(1)
    tbody = browser_obj.find_element_by_xpath(
        '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody')
    tr_list = tbody.find_elements_by_xpath('tr')
    temp = []
    for tr in tr_list:
        text = tr.find_element_by_xpath('td[4]').text
        temp.append(text)
    next_button = browser_obj.find_element(
        (By.XPATH, '//*[@id="private-project"]/div[2]/div/div[2]/div/div/ul/li[last()-1]/button'))
    val = next_button.get_attribute("disabled")
    while not val:
        next_button.click()
        sleep(1)
        tbody_n = browser_obj.find_element_by_xpath(
            '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody')
        tr_list_n = tbody_n.find_elements_by_xpath('tr')
        for tr in tr_list_n:
            text = tr.find_element_by_xpath('td[4]').text
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
    browser_obj.click((By.CSS_SELECTOR, '.ant-table-column-sorter-down > svg '))


def test_create_time_sort(browser_obj):
    """
    测试需求创建时间排序
    :param browser_obj:
    :return:
    """
    # 升序
    browser_obj.click(
        (By.XPATH,
         '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/thead/tr/th[7]/div/div/span[2]/span/span[1]'))
    sleep(1)
    time_tds = browser_obj.find_elements((By.CSS_SELECTOR, 'td.ant-table-column-sort'))
    time_list = [td.text for td in time_tds]
    stamps = []
    for t in time_list:
        time_stamp = time.mktime(time.strptime(t, '%Y-%m-%d %H:%M:%S'))
        stamps.append(time_stamp)
    logger.debug(stamps)
    # 断言
    assert sorted(stamps) == stamps

    # 降序
    browser_obj.click(
        (By.XPATH,
         '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/thead/tr/th[7]/div/div/span[2]/span/span[2]'))
    sleep(1)
    time_tds = browser_obj.find_elements((By.CSS_SELECTOR, 'td.ant-table-column-sort'))
    time_list = [td.text for td in time_tds]
    stamps = []
    for t in time_list:
        time_stamp = time.mktime(time.strptime(t, '%Y-%m-%d %H:%M:%S'))
        stamps.append(time_stamp)
    logger.debug(stamps)
    # 断言
    assert sorted(stamps, reverse=True) == stamps

    # 恢复初始页面
    browser_obj.click(
        (By.XPATH,
         '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/thead/tr/th[7]/div/div/span[2]/span/span[2]'))


def test_requirement_comment_legal(browser_obj):
    """
    测试原始需求评论合法
    :param browser_obj:
    :return:
    """
    browser_obj.click(
        (By.XPATH,
         '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]/button'))
    sleep(1)
    browser_obj.click((By.XPATH, '//*[@id="drawerBody"]/div/div/div/div/div[1]/div[1]/div/div[2]/div'))
    sleep(1)
    locator = (By.CSS_SELECTOR, 'textarea[id*=mentions]')
    browser_obj.click(locator)
    sleep(1)
    comment = 'asdasdasdas'
    browser_obj.send_key(locator, comment)
    sleep(1)
    browser_obj.send_key(locator, Keys.ENTER)
    sleep(1)
    assert browser_obj.get_text(
        (By.XPATH, '//*[@id="drawerBody"]/form/div[1]/div/div/ul/div[last()]/div/div/div[2]/div[2]/div')) == comment

    browser_obj.click((By.XPATH, '/html/body/div[2]/div/div/div/div/div[1]/button'))


def test_requirement_comment_wrongful(browser_obj):
    """
    测试原始需求评论不合法
    :param browser_obj:
    :return:
    """
    browser_obj.click(
        (By.XPATH,
         '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]/button'))
    sleep(1)
    browser_obj.click((By.XPATH, '//*[@id="drawerBody"]/div/div/div/div/div[1]/div[1]/div/div[2]/div'))
    sleep(1)
    locator = (By.CSS_SELECTOR, 'textarea[id*=mentions]')
    browser_obj.click(locator)
    sleep(1)
    # 评论为空
    # 评论超过300字符
    comment = ''
    for i in range(301):
        comment += 'a'
    browser_obj.send_key(locator, comment)
    assert browser_obj.get_text(
        (By.XPATH, '//*[@id="drawerBody"]/form/div[last()]/div/div/div/div[2]/div')) == '回复字数最多300字符'

    browser_obj.click((By.XPATH, '/html/body/div[2]/div/div/div/div/div[1]/button'))


def test_requirement_comment_carry_url(browser_obj):
    """
    测试需求评论里携带url
    :param browser_obj:
    :return:
    """
    browser_obj.click(
        (By.XPATH,
         '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]/button'))
    sleep(1)
    browser_obj.click((By.XPATH, '//*[@id="drawerBody"]/div/div/div/div/div[1]/div[1]/div/div[2]/div'))
    sleep(1)
    locator = (By.CSS_SELECTOR, 'textarea[id*=mentions]')
    browser_obj.click(locator)
    sleep(1)
    # 评论携带url
    comment = "https://www.baidu.com/"
    browser_obj.send_key(locator, comment)
    sleep(1)
    browser_obj.send_key(locator, Keys.ENTER)
    assert browser_obj.find_element(
        (By.XPATH, '//*[@id="drawerBody"]/form/div[1]/div/div/ul/div[last()]/div/div/div[2]/div[2]/div/a'))

    browser_obj.click((By.XPATH, '/html/body/div[2]/div/div/div/div/div[1]/button'))


def test_requirement_comment_thumbs(browser_obj):
    """
    测试需求评论点赞, 取消点赞
    :param browser_obj:
    :return:
    """
    # 点赞
    browser_obj.click(
        (By.XPATH,
         '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]/button/span'))
    sleep(1)
    browser_obj.click((By.XPATH, '//*[@id="drawerBody"]/div/div/div/div/div[1]/div[1]/div/div[2]/div'))
    sleep(1)
    browser_obj.click((By.CSS_SELECTOR, 'span > svg[data-icon="like"]'))
    sleep(2)
    assert browser_obj.get_text(
        (By.XPATH,
         '//*[@id="drawerBody"]/form/div[1]/div/div/ul/div[1]/div/div/div[2]/ul/li/div/div[1]/span[2]')) == '1'
    # 取消点赞
    browser_obj.click((By.CSS_SELECTOR, 'span > svg[data-icon="like"]'))
    sleep(2)
    assert browser_obj.get_text(
        (By.XPATH,
         '//*[@id="drawerBody"]/form/div[1]/div/div/ul/div[1]/div/div/div[2]/ul/li/div/div[1]/span[2]')) == '0'

    browser_obj.click((By.XPATH, '/html/body/div[2]/div/div/div/div/div[1]/button'))


def test_related_requirement_display_jump(browser_obj):
    """
    测试关联需求事项展示和跳转
    :param browser_obj:
    :return:
    """
    # 1.新建需求
    browser_obj.click((By.XPATH, '//*[@id="private-project"]/div[2]/div/div[1]/div[1]/div/div[2]/span/button'))
    sleep(1)
    browser_obj.send_key((By.XPATH, '//*[@id="summarize"]'), '关联卡片的需求')
    browser_obj.click((By.XPATH, '//span[contains(.,"确 定")]'))
    sleep(1)
    # 2.添加此需求关联已有卡片
    browser_obj.click((By.CSS_SELECTOR, '.ant-table-row:nth-child(1) .ant-btn > span'))
    sleep(1)
    browser_obj.click((By.XPATH, '//span[contains(.,"接 纳")]'))
    sleep(1)
    browser_obj.click((By.CSS_SELECTOR, '.ant-col > .ant-radio-wrapper > span:nth-child(1)'))
    sleep(1)
    browser_obj.click((By.XPATH, '//div[2]/div/div/span/input'))
    sleep(1)
    browser_obj.click((By.XPATH, '//span[contains(.,"新建需求")]'))
    sleep(1)
    browser_obj.click((By.CSS_SELECTOR, '.ant-col:nth-child(3) > .ant-btn-primary > span'))
    sleep(1)
    # 3.点击查看原始需求详情
    browser_obj.click((By.CSS_SELECTOR, '.ant-table-row:nth-child(1) .ant-btn > span'))
    sleep(1)
    # 4.断言判断
    text = browser_obj.get_text(
        (By.XPATH, '//*[@id="drawerBody"]/form/div[1]/div[9]/div/div[2]/div/div/div/button /span'))
    event_title = text.split('-')[-1]
    browser_obj.click((By.XPATH, '//*[@id="drawerBody"]/form/div[1]/div[9]/div/div[2]/div/div/div/button/span'))
    sleep(1)
    check = browser_obj.get_text(
        (By.XPATH, '//*[@id="itemDetailContainer"]/form/div[1]/div/div/div/span/div/div/div/div/div'))
    assert check == event_title


def test_modify_related_requirement(browser_obj):
    """
    测试修改关联的需求
    :param browser_obj:
    :return:
    """
    # 1.点击关联卡片的需求，查看详情
    browser_obj.click((By.CSS_SELECTOR, '.ant-table-row:nth-child(1) .ant-btn > span'))
    sleep(1)
    browser_obj.click((By.XPATH, '//*[@id="drawerBody"]/form/div[1]/div[9]/div/div[2]/div/div/div/button/span'))
    sleep(1)
    # 2.修改关联事项标题
    browser_obj.click((By.XPATH, '//div[@id="itemDetailContainer"]/form/div/div/div/div/span/div/div/div/div/div'))
    sleep(1)
    browser_obj.click((By.XPATH, '//input[@id="issueTitle"]'))

    # todo 这里修改需求关联事项标题，元素定位报错
    check = '修改事项标题'
    # browser_obj.send_key((By.XPATH, '//input[@id="issueTitle"]'), check)
    js = 'document.getElementsByClassName("editCell___3icLl")[0].innerText = "{}"'.format(check)
    browser_obj.script(js)
    sleep(1)
    # 3.断言判断
    browser_obj.click((By.CSS_SELECTOR, '.anticon-arrow-left > svg'))
    sleep(1)
    text = browser_obj.get_text(
        (By.XPATH, '//*[@id="drawerBody"]/form/div[1]/div[9]/div/div[2]/div/div/div/button/span'))
    event_title = text.split('-')[-1]
    assert check == event_title


def test_handle_requirement_abnormal_scene(browser_obj):
    """
    测试异常场景（需求被处理或用户无权限）处理原始需求
    :param browser_obj:
    :return:
    """
    # 1.该需求已被处理
    browser_obj.click((By.CSS_SELECTOR, '.anticon-filter path'))
    sleep(0.2)
    # 筛选所有已处理的需求
    browser_obj.click((By.XPATH, '//li[2]/label/span/input'))
    browser_obj.click((By.XPATH, '//li[3]/label/span/input'))
    browser_obj.click((By.XPATH, '//li[4]/label/span/input'))
    browser_obj.click((By.XPATH, '//li[5]/label/span/input'))
    sleep(0.2)
    browser_obj.click((By.XPATH, '//span[contains(.,"确 定")]'))
    sleep(0.2)
    browser_obj.click(
        (By.XPATH,
         '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]/button/span'))
    # 断言判断
    assert browser_obj.get_attribute(
        (By.XPATH, '/html/body/div[2]/div/div/div/div/div[3]/div/div[2]/div/div[2]/div/button'), 'disabled')
    # 2.todo 用户无权限操作


def test_upload_attachment_abnormal_scene(browser_obj):
    """
    测试异常场景（已处理的需求）上传附件
    :param browser_obj:
    :return:
    """
    browser_obj.click((By.CSS_SELECTOR, '.anticon-filter path'))
    sleep(0.2)
    # 筛选所有已处理的需求
    browser_obj.click((By.XPATH, '//li[2]/label/span/input'))
    browser_obj.click((By.XPATH, '//li[3]/label/span/input'))
    browser_obj.click((By.XPATH, '//li[4]/label/span/input'))
    browser_obj.click((By.XPATH, '//li[5]/label/span/input'))
    sleep(0.2)
    browser_obj.click((By.XPATH, '//span[contains(.,"确 定")]'))
    sleep(0.2)
    browser_obj.click(
        (By.XPATH,
         '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]/button/span'))
    sleep(1)
    assert browser_obj.get_attribute(
        (By.XPATH,
         '//*[@id="drawerBody"]/form/div[1]/div[7]/div/div/div/div[2]/div/div/span/div/span/button/span[2]/..'),
        'disabled')

    browser_obj.click((By.XPATH, '/html/body/div[2]/div/div/div/div/div[1]/button'))


def test_related_requirement_jump_matter(browser_obj):
    """
    测试关联需求能跳转到事项详情看板
    :param browser_obj:
    :return:
    """
    # 1.新建需求
    browser_obj.click((By.XPATH, '//*[@id="private-project"]/div[2]/div/div[1]/div[1]/div/div[2]/span/button'))
    sleep(1)
    browser_obj.send_key((By.XPATH, '//*[@id="summarize"]'), '关联卡片的需求')
    browser_obj.click((By.XPATH, '//span[contains(.,"确 定")]'))
    sleep(1)
    # 2.添加此需求关联已有卡片
    browser_obj.click((By.CSS_SELECTOR, '.ant-table-row:nth-child(1) .ant-btn > span'))
    sleep(1)
    browser_obj.click((By.XPATH, '//span[contains(.,"接 纳")]'))
    sleep(1)
    browser_obj.click((By.CSS_SELECTOR, '.ant-col > .ant-radio-wrapper > span:nth-child(1)'))
    sleep(1)
    browser_obj.click((By.XPATH, '//div[2]/div/div/span/input'))
    sleep(1)
    browser_obj.click((By.XPATH, '//span[contains(.,"新建需求")]'))
    sleep(1)
    browser_obj.click((By.CSS_SELECTOR, '.ant-col:nth-child(3) > .ant-btn-primary > span'))
    sleep(1)
    # 3.点击查看原始需求详情
    browser_obj.click((By.CSS_SELECTOR, '.ant-table-row:nth-child(1) .ant-btn > span'))
    sleep(1)
    # 4. 点击关联事项
    browser_obj.click((By.CSS_SELECTOR, '.ant-table-row:nth-child(1) .ant-btn > span'))
    sleep(1)
    browser_obj.click((By.XPATH, '//*[@id="drawerBody"]/form/div[1]/div[9]/div/div[2]/div/div/div/button/span'))
    sleep(1)
    # 断言判断
    assert browser_obj.get_text(
        (By.XPATH, '//*[@id="root"]/section/section/header/div/div[1]/div/span[3]/span[1]/div')) == '事项详情'


def test_requirement_status_multiple_choice(browser_obj):
    """
    测试需求状态多选
    :param browser_obj:
    :return:
    """
    # 1.勾选待处理和未开始状态的需求，查看筛选结果是否正确
    browser_obj.click((By.CSS_SELECTOR, '.anticon-filter path'))
    sleep(0.2)
    # 筛选待处理和未开始的请求
    browser_obj.click((By.XPATH, '//li[1]/label/span/input'))
    browser_obj.click((By.XPATH, '//li[2]/label/span/input'))
    sleep(0.2)
    browser_obj.click((By.XPATH, '//span[contains(.,"确 定")]'))
    sleep(1)
    # 断言判断, 判断筛选结果是否正确
    # 获取第一页数据
    tbody = browser_obj.find_element_by_xpath(
        '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody')
    tr_list = tbody.find_elements_by_xpath('tr')
    temp = []
    for tr in tr_list:
        status_val = tr.find_element_by_xpath('td[3]/div/a/div').text
        temp.append(status_val)
    # 循环遍历获取所有数据
    next_button = browser_obj.find_element(
        (By.XPATH, '//*[@id="private-project"]/div[2]/div/div[2]/div/div/ul/li[last()-1]/button'))
    val = next_button.get_attribute("disabled")
    while not val:
        next_button.click()
        sleep(1)
        tbody_n = browser_obj.find_element_by_xpath(
            '//*[@id="private-project"]/div[2]/div/div[2]/div/div/div/div/div/table/tbody')
        tr_list_n = tbody_n.find_elements_by_xpath('tr')
        for tr in tr_list_n:
            status_val = tr.find_element_by_xpath('td[3]/div/a/div').text
            temp.append(status_val)
        val = next_button.get_attribute("disabled")
    logger.debug(len(temp))
    check = [i for i in temp if i not in ['待处理', '未开始']]
    assert check == []

    # 恢复初始页面
    browser_obj.click((By.CSS_SELECTOR, '.anticon-filter path'))
    sleep(1)
    browser_obj.click((By.CSS_SELECTOR, '.ant-btn-sm:nth-child(1) > span'))
