import os

#获取当前项目的绝对路径
current = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(os.path.dirname(current))


#----登录账号-
login_userinfo ={"account_name":"ak","passwd":"111111"}
header = {"Content-Type": "application/json"}


#定义config目录的路径
config_path = BASE_DIR + os.sep + "config"

#定义base.txt文件路径
Base_txt_path= config_path + os.sep + 'base.txt'
Base_txt_pre_path= config_path + os.sep + 'base_pre.txt'

#定义data目录的路径
data_path = BASE_DIR + os.sep + "data"

#定义conf.yml文件的路径
config_file = config_path + os.sep +"conf.yml"

#定义db_conf.yml路径
db_config_file =  config_path + os.sep +"db_conf.yml"

#定义logs文件路径
log_path = BASE_DIR + os.sep + "logs"

#定义report目录的路径
report_path = BASE_DIR + os.sep + "report"


#定义testcase目录的路径
CASE_PATH = BASE_DIR + os.sep + "testcase"

#日志级别
log_level = "debug"
#日志文件扩展名
log_extension = ".log"



#----数据库--

