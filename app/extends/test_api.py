import requests

from app.extends.random_code import md5_code


class TestAPI(object):
    def __init__(self, url, data):
        self.url = url
        self.data = data

    def res(self, method):
        if method == "GET":
            response = requests.get(url=self.url, params=self.data)
        elif method == "POST":
            response = requests.post(url=self.url, json=self.data)
        print("status:" + str(response.status_code) + "\n")
        print("content:" + response.text)


if __name__ == '__main__':
    # url = "http://127.0.0.1:8000/api/verify_code/"
    # data = {
    #     "token": "123456"
    # }
    # test_api = TestAPI(url=url, data=data)
    # test_api.res("GET")

    url = "http://127.0.0.1:8000/api/user/"
    data = {
        "name": "gyw",
        "sex": "男",
        "email": "1299622716@qq.com",
        "password": "123456",
        "token": "123456",
        "code": md5_code("7909")
    }
    test_api = TestAPI(url=url, data=data)
    test_api.res("POST")