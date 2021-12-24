from libs.log_obj import LogObj
from stress.newben.common.common import get
from utils.decorator import retry

logger = LogObj().get_logger()


def get_per_page_storage_data(request_obj, url, header, param):
    response = request_obj.call('get', url, headers=header, param=param)
    response_json = None
    try:
        response_json = response.json()
    except Exception as e:
        if "Expecting value: line 1 column 1 (char 0)" in str(e):
            logger.warning("The response: {}".format(response.content.decode()))
            raise e

    if response_json['code'] == 200:
        return response_json
    else:
        raise Exception("Use the <{}> failed, the error messages are [{}]".format(url, response_json))


@retry(20, 3)
def check_all_create_storage_status(request_obj, url, header, param, storage_data):
    json_data = get_per_page_storage_data(request_obj, url, header, param)
    total = json_data["data"]["total"]
    size = json_data["data"]["size"]
    current_page = json_data["data"]["page"]
    pages = int(total / size) + 1 if total % size else int(total / size)
    status_list = []
    for data in json_data["data"]["list"]:
        if data["name"] in storage_data:
            status_list.append((data["name"], data["status"]))
    while current_page < pages:
        current_page += 1
        param1 = param.copy()
        param1["page"] = current_page
        next_data = get_per_page_storage_data(request_obj, url, header, param1)
        for data in next_data["data"]["list"]:
            if data["name"] in storage_data:
                status_list.append((data["name"], data["status"]))
    for status in status_list:
        if status[1] != "available":
            logger.warning("The status of <{}> is not available!".format(status[0]))
            raise Exception("Check failed.")


def check_search_storage_pool(json_data, request_obj, url, header, param):
    total = json_data["data"]["total"]
    size = json_data["data"]["size"]
    current_page = json_data["data"]["page"]
    length = len(json_data["data"]["list"])
    pages = int(total / size) + 1 if total % size else int(total / size)
    storage_pool_name = [data["name"] for data in json_data["data"]["list"]]
    assert size == param["size"]
    assert current_page == param["page"]
    for storage_pool in storage_pool_name:
        assert "stora" in storage_pool
    while current_page < pages:
        assert size == param["size"] == length
        current_page += 1
        param = param.copy()
        param["page"] = current_page
        get(request_obj, url, header, param)


def check_search_storage_volume(json_data, request_obj, url, header, param):
    total = json_data["data"]["total"]
    size = json_data["data"]["size"]
    current_page = json_data["data"]["page"]
    length = len(json_data["data"]["list"])
    pages = int(total / size) + 1 if total % size else int(total / size)
    storage_volume_name = [data["name"] for data in json_data["data"]["list"]]
    assert size == param["pageSize"]
    assert current_page == param["page"]
    for storage_pool in storage_volume_name:
        assert "volum" in storage_pool
    while current_page < pages:
        assert size == param["pageSize"] == length
        current_page += 1
        param = param.copy()
        param["page"] = current_page
        get(request_obj, url, header, param)
