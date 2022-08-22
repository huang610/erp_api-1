import os,yagmail
from utils.ExcelUtil import ExcelReader
from config.Conf import ConfigYaml
from config import setting

#初始化测试用例文件
case_file_path = os.path.join(setting.data_path,ConfigYaml().get_excel_file())
print(case_file_path)


def makeCase():
    sheet_name_list = ExcelReader(case_file_path).get_sheet_name()
    base_case_str = open(setting.Base_txt_path,encoding='utf-8').read()
    for sheet_name in sheet_name_list:
        sheet_name = sheet_name
        class_name = 'Test_'+ sheet_name.capitalize()
        content = base_case_str%(sheet_name,class_name,sheet_name)
        py_file_path = os.path.join(setting.CASE_PATH,class_name)

        if os.path.exists(py_file_path+'.py'):
            pass
        else:
            open('%s.py'%py_file_path,'w',encoding='utf-8').write(content)

# yy = makeCase()

def db_res_dic(check_lis):
    '''
    sql获取的数据Decimal转成int或float
    :param check_lis:
    :return:
    '''
    new_check_lis = []

    new_dic={}
    for k,v in check_lis.items():
        if type(v) != str:
            if v == None:
                new_dic[k]=None
            elif v == 0:
                new_dic[k]=0
            elif type(v) == 'datetime.datetime':
                new_dic[k]=v
            else:
                if '.' in str(v):
                    new_dic[k]=float(v)
                else:
                    new_dic[k]=int(v)
        else:
            new_dic[k]=v
    new_check_lis.append(new_dic)
    return new_check_lis



def sendmail(title,content,attrs=None):
    m = yagmail.SMTP(host=setting.MAIL_HOST,user=setting.MAIL_USER
                 ,password=setting.MAIL_PASSWRD
                )
    m.send(to=setting.TO,subject=title,
           contents=content,
           attachments=attrs)