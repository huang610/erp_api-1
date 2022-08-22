import os
import xlrd


# class SheetTypeError:
#     '''
#     自定义异常
#     '''
#     pass

class ExcelReader:
    def __init__(self,excel_file):
        '''
        验证文件是否存在，存在读取，不存在报错
        :param excel_file:
        :param sheet_by:
        :return:
        '''
        if os.path.exists(excel_file):
            self.excel_file = excel_file
            self.workbook = xlrd.open_workbook(self.excel_file)
            # self.sheet_by = sheet_by
            self._data=list()
        else:
            raise  FileNotFoundError("文件不存在")

    def get_sheet_name(self):
        '''
        获取所有sheet名称
        :return:
        '''
        sheet_name_list = self.workbook.sheet_names()

        return sheet_name_list

    def data(self,sheet_name):
        '''
        通过名称，索引读取sheet内容，
        读取sheet内容 返回一个list里面元素为:字典

        先获取首行
        再遍历剩余测试行，与首行组成dict，放在list

        :return:
        '''
        sheet = self.workbook.sheet_by_name(sheet_name)
        title = sheet.row_values(0)
        for col in range(1,sheet.nrows):
            col_value = sheet.row_values(col)
            self._data.append(dict(zip(title, col_value)))

        return self._data



# if __name__ == "__main__":
    # reader = ExcelReader("../data/testdata.xls")
    # print(reader.get_sheet_name())
    # print(reader.data("login"))