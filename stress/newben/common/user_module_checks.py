from libs.log_obj import LogObj
from stress.newben.common.common import get

logger = LogObj().get_logger()


def check_search_users(json_data, request_obj, url, header, param):
    total = json_data["data"]["total"]
    size = json_data["data"]["size"]
    current_page = json_data["data"]["page"]
    length = len(json_data["data"]["list"])
    pages = int(total / size) + 1 if total % size else int(total / size)
    users_name = [user["username"] for user in json_data["data"]["list"]]
    assert size == param["size"]
    assert current_page == param["page"]
    for user in users_name:
        assert "adm" in user
    while current_page < pages:
        assert size == param["size"] == length
        current_page += 1
        param = param.copy()
        param["page"] = current_page
        get(request_obj, url, header, param)
