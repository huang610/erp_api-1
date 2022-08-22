from utils.LogUtil import my_log
import json,ast,jsonpatch

class AssertUtil:
    def __init__(self):
        self.log = my_log("AssertUtil")

    def assert_code(self,code,expected_code):
        """
        code相等,验证返回状态码
        :param code:
        :param expected_code:
        :return:
        """
        try:
            assert int(code) == int(expected_code)
            return True
        except:
            self.log.error("code error,code is %s,expected_code is %s"%(code,expected_code))

            raise

    def assert_body(self,body,expected_body):
        """
        body相等，验证返回结果内容相等
        :param body:
        :param expected_body:
        :return:
        """
        try :
            assert body == expected_body
            return True
        except:
            self.log.error("body error,body is %s,expected_body is %s"%(body,expected_body))
            raise


    def assert_json_body(self,body,expected_body):
        """
        body相等，验证返回结果内容相等
        body和expected_body两个必须是字典
        :param body:
        :param expected_body:
        :return:
        """
        patch = jsonpatch.JsonPatch.from_diff(body,expected_body)
        print('patch is %s'%list(patch))
        try:
            assert len(list(patch)) == 0
            return True
        except:
            self.log.debug('期望结果与实际结果不相等，实际结果为：{},期望结果为：{}'.format(body,expected_body))
            self.log.debug('期望结果与实际结果的差异为：{}'.format(patch))
            raise


    def assert_in_body(self,body,expected_body):
        """
        将expected_body转成字典格式，然后取到期望结果里所有key，比较两个body中同一个key的值是否相等
        :param body:
        :param expected_body:
        :return:
        """
        expected_body_dic = ast.literal_eval(expected_body)
        expected_body_dic_keys = expected_body_dic.keys()
        try:
            for expected_key in expected_body_dic_keys:
                self.log.error("key是%s，expected_body is %s,body is %s"%(expected_key,expected_body_dic[expected_key],body[expected_key]))
                assert expected_body_dic[expected_key] == body[expected_key]

            return True
        except:
            self.log.error("不包含或者body是错误，body is %s,expected_body is %s"%(body,expected_body))
            raise


    def assert_in_body_dic(self,body,expect_result):
        """
        转换成json格式，验证返回结果是否包含期望的结果
        :param body:
        :param expected_body:
        :return:
        """
        body=json.dumps(body,ensure_ascii=False)
        expect_result_dic=ast.literal_eval(expect_result)
        expect_result=json.dumps(expect_result_dic,ensure_ascii=False)
        expect_result_list=expect_result.split(',')


        for e_body in expect_result_list:
            e_body = e_body.replace('{','').replace('}','')
            my_log().debug('e_body is %s'%e_body)
            try:
                assert e_body in body
            except AssertionError:
                my_log().debug('e_body is not in body;e_body=%s,body=%s'%(e_body,body))
                raise
        return True
