import requests
from utils.LogUtil import my_log


class Request:
    def __init__(self):
        self.log = my_log("Requests")
    def requests_api(self,url,data = None,json=None,headers=None,cookies=None,method="get"):
        '''
        判断请求方式，获取结果内容，#内容存到字典，返回
        :param url:
        :param data:
        :param json:
        :param headers:
        :param cookies:
        :param method:
        :return:
        '''
        if method =="get":
            # self.log.debug("发送get请求，请求url：{}".format(url))
            r = requests.get(url, data = data, json=json, headers=headers,cookies=cookies)
        elif method == "post":
            # self.log.debug("发送post请求，请求url：{}".format(url))
            r = requests.post(url,data = data,  json=json, headers=headers,cookies=cookies)

        code = r.status_code
        try:
            body = r.json()
        except Exception as e:
            body = r.text

        res = dict()
        res["code"] = code
        res["body"] = body
        return res

    def get(self,url,**kwargs):
        '''
        定义参数url,json,headers,cookies,method
        调用公共方法
        :param url:
        :param kwargs:
        :return:
        '''
        return self.requests_api(url,method="get",**kwargs)

    def post(self,url,**kwargs):
        '''
        定义参数url,json,headers,cookies,method
        调用公共方法
        :param url:
        :param kwargs:
        :return:
        '''
        return self.requests_api(url,method="post",**kwargs)