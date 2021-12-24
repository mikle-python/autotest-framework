from libs.log_obj import LogObj
from stress.newben.common.common import get

logger = LogObj().get_logger()


def check_role_mapping(json_data):
    assert json_data["data"]["hasAuth"] == True


def check_type_corresponding_permission(json_data):
    assert json_data["message"] == "success"


def check_search_role(json_data, request_obj, url, header, param):
    total = json_data["data"]["total"]
    size = json_data["data"]["size"]
    current_page = json_data["data"]["page"]
    length = len(json_data["data"]["list"])
    pages = int(total / size) + 1 if total % size else int(total / size)
    roles_name = [role["name"] for role in json_data["data"]["list"]]
    assert size == param["size"]
    assert current_page == param["page"]
    for role in roles_name:
        assert "ro" in role
    while current_page < pages:
        assert size == param["size"] == length
        current_page += 1
        param = param.copy()
        param["page"] = current_page
        get(request_obj, url, header, param)


def check_search_authorization(json_data, request_obj, url, header, param):
    total = json_data["data"]["total"]
    size = json_data["data"]["size"]
    current_page = json_data["data"]["page"]
    length = len(json_data["data"]["list"])
    pages = int(total / size) + 1 if total % size else int(total / size)
    authorizations_name = [role["name"] for role in json_data["data"]["list"]]
    assert size == param["size"]
    assert current_page == param["page"]
    for authorization in authorizations_name:
        assert "auth" in authorization
    while current_page < pages:
        assert size == param["size"] == length
        current_page += 1
        param = param.copy()
        param["page"] = current_page
        get(request_obj, url, header, param)
