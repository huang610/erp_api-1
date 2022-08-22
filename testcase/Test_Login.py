from config.Conf import ConfigYaml
import os,json,pytest,allure,ast,config.setting
from common.ExcelData import Data
from utils.LogUtil import my_log
from common import ExcelConfig
from utils.RequestsUtil import Request
from common import Base
from utils.AssertUtil import AssertUtil

#初始化测试用例文件的绝对路径
case_file_path = os.path.join(config.setting.data_path,ConfigYaml().get_excel_file())
sheet_name = 'login'
#获取运行测试用例列表
run_list = Data(case_file_path).get_run_data(sheet_name)
log = my_log()

#初始化dataconfig，获取Excel表头当做key，获取values
data_key = ExcelConfig.DataConfig

class Test_Login:
    def run_api(self,url,method,params=None,header=None,cookie=None):
        request = Request()
        if len(str(params).strip()) != 0:
            params = json.loads(params)
        if str(method).lower() == "get":
            log.debug("发送get请求，请求url：{}".format(url))
            res = request.get(url, json=params, headers=header, cookies=cookie)
        elif str(method).lower() == "post":
            log.debug("发送post请求，请求url：{}".format(url))
            log.debug('传入参数为：{}{}'.format(type(params),params))
            res = request.post(url, json=params, headers=header, cookies=cookie)
        else:
            log.error("错误请求method: {}".format(method))
        return res

    #执行前置条件用例
    def run_pre(self,pre_case):
        '''
        初始化前置条件的数据,执行前置条件用例
        :param pre_case:
        :return:
        '''
        url = ConfigYaml().get_conf_sso_url() + case[data_key.url]
        method = pre_case[data_key.method]
        params = pre_case[data_key.params]
        params = self.get_token_correlation(params)
        log.error("前置用例传入的参数：{}".format(params))
        header = pre_case[data_key.headers]
        cookie = pre_case[data_key.cookies]
        # cookie = json.loads(cookie)
        # header = json.loads(header)

        res = self.run_api(url,method,params,header,cookie)
        return res


    @pytest.mark.parametrize("case",run_list)
    def test_login(self,case):
        '''
        循环测试用例，初始化url等数据，并执行
        :param case:
        :return:
        '''
        log.debug('------------开始执行用例------------')
        log.debug('执行用例为：{}'.format(case))
        url = ConfigYaml().get_conf_sso_url() + case[data_key.url]
        case_id = case[data_key.case_id]
        case_model = case[data_key.case_model]
        case_name = case[data_key.case_name]
        pre_exec = case[data_key.pre_exec]
        method = case[data_key.method]
        params_type = case[data_key.params_type]
        params = case[data_key.params]
        log.debug('传入参数为：{}'.format(params))
        expect_result = case[data_key.expect_result]
        log.debug('期望结果为：{}{}'.format(type(expect_result),expect_result))
        header = case[data_key.headers]
        log.debug('header类型为：{}'.format(type(header)))
        cookie =case[data_key.cookies]
        code = case[data_key.code]
        db_verify = case[data_key.db_verify]

        # if pre_exec:
        #     pre_case = Data(case_file_path).get_case_pre(pre_exec,sheet_name)
        #     log.debug('前置用例为：{}'.format(pre_case))
        #
        #     pre_res = self.run_pre(pre_case)
        #     log.debug('前置用例执行结果为：{}'.format(pre_res))
        #
        #     params = self.get_params_correlation_all(params,pre_res)
        #     log.debug('替换后的params为：{}'.format(params))
        # else:
        #     params = self.get_token_correlation(params)

        res = self.run_api(url, method, params)
        log.debug('用例执行返回结果的body为：{}'.format(res["body"]))

        #动态获取sheet名称 作为 feature 一级标签
        allure.dynamic.feature(sheet_name)
        #动态获取模块  作为 story 二级标签
        allure.dynamic.story(case_model)
        #动态获取用例ID+接口名称 作为 title
        allure.dynamic.title(case_id+case_name)
        #请求URL  请求类型 期望结果 实际结果描述
        desc = f"<font color='red'>请求URL: </font> {url}<Br/>" \
               f"<font color='red'>请求类型: </font>{method}<Br/>" \
               f"<font color='red'>请求header: {type(header)}</font>{header}<Br/>" \
               f"<font color='red'>请求参数: </font>{params}<Br/>" \
               f"<font color='red'>期望结果: </font>{expect_result}<Br/>" \
               f"<font color='red'>实际结果: </font>{res}"
        allure.dynamic.description(desc)

        #断言验证
        assert_util = AssertUtil()
        assert_util.assert_in_body_dic(res['body'], expect_result)


if __name__ == '__main__':
    pytest.main(["-s","Test_login.py"])