import json
from libs.request_obj import RequstObj
from libs.log_obj import LogObj
from utils.decorator import retry, print_for_call

logger = LogObj().get_logger()


class ApiCommon:
    _api_header = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": None,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/96.0.4664.110 Safari/537.36"
    }

    def __init__(self, login_data, login_headers, login_url):
        self.login_data = login_data
        self.login_headers = login_headers
        self.login_url = login_url

    @property
    def request_obj(self):
        return RequstObj()

    @property
    @retry(tries=30, delay=2)
    def login(self):
        login_response = self.request_obj.call('post', self.login_url, data=json.dumps(self.login_data),
                                               headers=self.login_headers).json()

        if login_response['code'] == "200" and login_response['message'] == "success":
            logger.info("Re login api server {} successfully !".format(self.login_url))
            return login_response['data']['token']
        else:
            raise Exception("Re login api server {} failed, the error messages are [{}]".
                            format(self.login_url, login_response))

    @property
    def api_header(self):
        if self._api_header['Authorization'] is None:
            self._api_header['Authorization'] = self.login
        return self._api_header

    @retry(tries=5, delay=1)
    @print_for_call
    def create_api(self, url, data):
        response = self.request_obj.call('post', url, data=json.dumps(data), headers=self.api_header)
        try:
            response_json = response.json()
        except Exception as e:
            if "Expecting value: line 1 column 1 (char 0)" in str(e):
                logger.warning("The response: {}".format(response.content.decode()))
                logger.warning("The data happened error: {}".format(data))
                raise e

        if response_json['code'] == "200" and response_json['message'] == "success":
            logger.info("Use the <{}> done !".format(url))
            return response.elapsed.total_seconds()
        elif response_json['code'] == "401" and 'token is expired' in response_json['message']:
            self.api_header['Authorization'] = None
            raise Exception("The token has expired")
        else:
            raise Exception("Use the <{}> failed, the error messages are [{}]".format(url, response_json))

    @retry(tries=5, delay=1)
    @print_for_call
    def delete_api(self, url, data=None):
        if data:
            response = self.request_obj.call('delete', url, headers=self.api_header, data=json.dumps(data))
        else:
            response = self.request_obj.call('delete', url, headers=self.api_header)
        try:
            response_json = response.json()
        except Exception as e:
            if "Expecting value: line 1 column 1 (char 0)" in str(e):
                logger.warning("The response: {}".format(response.content.decode()))
                logger.warning("The url happened error: {}".format(url))
                raise e

        if response_json['code'] == "200" and response_json['message'] == "success":
            logger.info("Use the <{}> done !".format(url))
            return response.elapsed.total_seconds()
        elif response_json['code'] == "401" and 'token is expired' in response_json['message']:
            self.api_header['Authorization'] = None
            raise Exception("The token has expired")
        else:
            raise Exception("Use the <{}> failed, the error messages are [{}]".format(url, response_json))

    @retry(tries=5, delay=1)
    @print_for_call
    def update_api(self, url, data):
        response = self.request_obj.call('put', url, data=json.dumps(data), headers=self.api_header)

        try:
            response_json = response.json()
        except Exception as e:
            if "Expecting value: line 1 column 1 (char 0)" in str(e):
                logger.warning(response.content.decode())
                raise e

        if response_json['code'] == "200" and response_json['message'] == "success":
            logger.info("Use the <{}> done !".format(url))
            return response.elapsed.total_seconds()
        elif response_json['code'] == "401" and 'token is expired' in response_json['message']:
            self.api_header['Authorization'] = None
            raise Exception("The token has expired")
        else:
            raise Exception("Use the <{}> failed, the error messages are [{}]".format(url, response_json))

    @retry(tries=5, delay=1)
    @print_for_call
    def list_api(self, url):
        response = self.request_obj.call('get', url, headers=self.api_header)
        try:
            response_json = response.json()
        except Exception as e:
            if "Expecting value: line 1 column 1 (char 0)" in str(e):
                logger.warning("The response: {}".format(response.content.decode()))
                raise e

        if response_json['code'] == "200" and response_json['message'] == "success":
            logger.info("List by <{}> done !".format(url))
            return response.elapsed.total_seconds()
        elif response_json['code'] == "401" and 'token is expired' in response_json['message']:
            self.api_header['Authorization'] = None
            raise Exception("The token has expired")
        else:
            raise Exception("List by <{}> failed, the error messages are [{}]".format(url, response_json))

    def check_api(self, api_func):
        pass


if __name__ == '__main__':
    pass