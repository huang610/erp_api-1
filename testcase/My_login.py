# _*_coding:utf-8_*_
import json
from config import setting
from utils.RequestsUtil import Request
from config.Conf import ConfigYaml

request = Request()

class Login_password(object):
    def login(self):
        '''
        密码登录
        :return:
        '''
        base_url = ConfigYaml().get_conf_sso_url()
        url =base_url+'/v1/auth/login'
        data = setting.login_userinfo
        res = request.post(url,json=data)
        token={}
        token['token']=res['body']['data']['token']
        return token


my_login=Login_password()
# my_login.login()