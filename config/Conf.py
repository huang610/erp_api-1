import os,config.setting
from utils.YamlUtil import YamlReader

#获取项目基本目录
current = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(os.path.dirname(current))


# 读取配置文件
class ConfigYaml:
    def __init__(self):
        '''
        初始yaml读取配置文件
        :return:
        '''
        self.config = YamlReader(config.setting.config_file).data()
        self.db_config = YamlReader(config.setting.db_config_file).data()

    def get_conf_sso_url(self):
        '''
        获取测试用例的url
        :return:
        '''
        return self.config["BASE"]["test"]["sso_url"]

    def get_conf_erp_url(self):
        '''
        获取测试用例的url
        :return:
        '''
        return self.config["BASE"]["test"]["erp_url"]

    def get_excel_file(self):
        """
        获取测试用例excel名称
        :return:
        """
        return self.config["BASE"]["test"]["case_file"]

    def get_excel_url(self):
        '''
        获取测试用例的url
        :return:
        '''
        return self.config["BASE"]["excel"]["url"]

    def get_db_conf_info(self,db_alias):
        """
        根据db_alias获取该名称下的数据库信息
        :param db_alias:
        :return:
        """
        return self.db_config[db_alias]

    def get_test_local_redis(self):
        '''
        获取本地测试环境redis
        :return:
        '''
        return self.config["redis"]["redis_test_local"]

    def get_test_test_server(self):
        '''
        获取正式环境-服务器redis
        :return:
        '''
        return self.config["redis"]["redis_test_server"]

    def get_email_info(self):
        """
        获取邮件配置相关信息
        :return:
        """
        return self.config["email"]

if __name__ == "__main__":
    import ast,json
    conf_read = ConfigYaml()
    # print(conf_read.get_db_conf_info("db_1"))
    # print(conf_read.get_db_conf_info("db_2"))
    # print(conf_read.get_db_conf_info("db_3"))
    #1、初始化数据库信息，Base.py init_db
    #2、接口用例返回结果内容进数据库验证
    print(conf_read.get_conf_erp_url())