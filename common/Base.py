import json,ast
import re
import subprocess
from config.Conf import ConfigYaml
from utils.AssertUtil import AssertUtil
from utils.LogUtil import my_log
from utils.MysqlUtil import Mysql
from utils.EmailUtil import SendEmail
from lib.tools import db_res_dic
from utils import Md5Util

p_data = '\$\{(.*?)\}\$'
log = my_log()


def init_db(db_alias):
    '''
    初始数据化信息，通过配置
    初始化mysql对象
    :param db_alias:
    :return:
    '''
    db_info = ConfigYaml().get_db_conf_info(db_alias)
    host = db_info["db_host"]
    user = db_info["db_user"]
    password = db_info["db_password"]
    db_name = db_info["db_name"]
    charset = db_info["db_charset"]
    port = int(db_info["db_port"])

    conn = Mysql(host,user,password,db_name,charset,port)
    return conn

def assert_db(db_name,result,db_verify):
    '''
    数据库的结果与接口返回的结果验证
    :param db_name:
    :param result:
    :param db_verify:
    :return:
    '''
    assert_util =  AssertUtil()
    conn = init_db(db_name)
    db_res = conn.fetchone(db_verify)  #查询sql，excel定义好的
    db_res=db_res_dic(db_res)
    log.debug("数据库查询结果：{}".format(str(db_res)))

    verify_list = list(dict(db_res[0]).keys())  # 获取数据库结果的key
    # 根据key获取数据库结果，接口结果
    for line in verify_list:
        res_line = result[line]
        res_db_line = db_res[0][line]
        assert_util.assert_body(res_line, res_db_line)

def get_db_res_dic(db_verify):
    '''
    需要从多个库里查询时，
    先将Excel里取到的字符串转成字典，循环该字典，key即为库名
    然后链接数据库，执行value也就是对应的sql，取得查询结果为list
    :param db_verify:
    :param res:
    :return:
    '''
    db_res_dic = {}
    db_verify_dic = ast.literal_eval(db_verify)
    for db, sql in db_verify_dic.items():
        db_res = init_db(db).fetchall(sql)
        for i in db_res:
            for k, v in i.items():
                db_res_dic[k] = v
    return db_res_dic

def get_db_res(db_verify):
    '''
    需要从多个库里查询时，
    先将Excel里取到的字符串转成字典，循环该字典，key即为库名
    然后链接数据库，执行value也就是对应的sql，取得查询结果为list
    :param db_verify:
    :param res:
    :return:
    '''
    db_res=[]
    db_verify_dic = ast.literal_eval(db_verify)
    for db, sql in db_verify_dic.items():
        db_res = init_db(db).fetchall(sql)
    return db_res

def json_parse(data):
    """
    格式化字符，转换字典
    :param data:
    :return:
    """
    # if headers:
    #     header = json.loads(headers)
    # else:
    #     header = headers
    return json.loads(data) if data else data

def res_find(data,pattern_data=p_data):
    """
    查询
    :param data:
    :param pattern_data:
    :return:
    """
    pattern = re.compile(pattern_data)
    re_res = pattern.findall(data)
    return re_res

def res_sub(data,replace,pattern_data=p_data):
    """
    替换
    :param data: 原字符串
    :param replace:  要替换成的目标
    :param pattern_data: 正则表达式
    :return:
    """
    pattern = re.compile(pattern_data)
    re_res = pattern.findall(data)
    if re_res:
        return re.sub(pattern_data,replace,data)
    return re_res

def cookie_find(headers,cookies):
    """
    验证请求中是否有${}$需要结果关联，有则找到{}中的字段组成一个list返回
    :param headers:
    :param cookies:
    :return:
    """
    if "${" in headers:
        headers = res_find(headers)
    if "${" in cookies:
        cookies = res_find(cookies)
    return headers,cookies

def header_find(header):
    """
    验证请求中是否有${}$需要结果关联，有则找到{}中的字段组成一个list返回
    :param params:
    :return:
    """
    # if "${" in params:
    #     params = res_find(params)
    # return params
    params_find_list = []
    if "${" in header:
        params_find_list = res_find(header)
    return params_find_list

def allure_report(report_result,report_html):
    """
    subprocess.call 执行命令 allure generate,生成allure的HTML报告文件
    :param report_path:
    :param report_html:
    :return:
    """
    allure_cmd ="allure generate %s -o %s --clean"%(report_result,report_html)

    log.info("报告地址:{}".format(report_html))
    try:
        subprocess.call(allure_cmd,shell=True)
    except:
        log.error("执行用例失败，请检查一下测试环境相关配置")
        raise

def send_mail(report_html_path="",content="",title="稽核测试报告"):
    """
    发送邮件
    :param report_html_path:
    :param content:
    :param title:
    :return:
    """
    email_info = ConfigYaml().get_email_info()
    smtp_addr = email_info["smtpserver"]
    username = email_info["username"]
    password = email_info["password"]
    recv = email_info["receiver"]
    # smtp_addr= setting.MAIL_HOST
    # username = setting.MAIL_USER
    # password = setting.MAIL_PASSWRD
    # recv = setting.TO

    email = SendEmail(
        smtp_addr=smtp_addr,
        username=username,
        password=password,
        recv=recv,
        title=title,
        content=content,
        file=report_html_path)
    email.send_mail()