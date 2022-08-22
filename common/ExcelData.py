from utils.ExcelUtil import ExcelReader
from common.ExcelConfig import DataConfig

class Data:
    def __init__(self,testcase_file):
        '''
        使用excel工具类，获取结果list
        :param testcase_file:
        :param sheet_name:
        :return:
        '''
        self.reader = ExcelReader(testcase_file)
        # print(self.reader.data(sheet_name))

    def get_run_data(self,sheet_name):
        """
        根据是否运行列==y，获取需执行的测试用例，放到新的列表
        :return:
        """
        run_list = list()
        for line in self.reader.data(sheet_name):
            if str(line[DataConfig().is_run]).lower() == "y":
                run_list.append(line)
        return run_list

    def get_case_list(self,sheet_name):
        """
        获取全部测试用例，为一个list里面元素为:字典
        :return:
        """
        # run_list=list()
        # for line in self.reader.data():
        #         run_list.append(line)
        run_list = [ line for line in self.reader.data(sheet_name)]
        return run_list

    def get_case_pre(self,pre,sheet_name):
        """
        根据前置条件：从全部测试用例取到对应的测试用例，返回
        :param pre:
        :return:
        """
        run_list = self.get_case_list(sheet_name)
        for line in run_list:
            if pre in dict(line).values():
                return line
        return None

# y = Data(r"C:\Users\Administrator\Desktop\pytest_allure_correlation\data\auditcase.xlsx")