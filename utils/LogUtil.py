import logging
import datetime,os
from config import setting

#定义日志级别的映射
log_l = {
    "info": logging.INFO,
    "debug": logging.DEBUG,
    "warning": logging.WARNING,
    "error": logging.ERROR
}

class Logger:
    def __init__(self,log_file,log_name,log_level):
        '''
        定义参数 输出文件名称，Loggername，
        #日志文件名称 = logs目录 + 当前时间+扩展名,日志级别
        :param log_file:
        :param log_name:
        :param log_level:
        :return:
        '''
        self.log_file = log_file
        self.log_name = log_name
        self.log_level = log_level

        # 设置logger名称
        self.logger = logging.getLogger(self.log_name)
        # 设置log级别
        self.logger.setLevel(log_l[self.log_level])
        #判断handlers是否存在
        if not self.logger.handlers:
            # 输出控制台
            fh_stream = logging.StreamHandler()
            fh_stream.setLevel(log_l[self.log_level])
            formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s ')
            fh_stream.setFormatter(formatter)
            # 写入文件
            fh_file = logging.FileHandler(self.log_file,encoding="utf-8",mode="a")
            fh_file.setLevel(log_l[self.log_level])
            fh_file.setFormatter(formatter)

            # 添加handler
            self.logger.addHandler(fh_stream)
            self.logger.addHandler(fh_file)

#log目录
log_path = setting.log_path
#当前时间
current_time = datetime.datetime.now().strftime("%Y-%m-%d")
#扩展名
log_extension = setting.log_extension
logfile = os.path.join(log_path,current_time+log_extension)

#日志文件级别
loglevel = setting.log_level

def my_log(log_name = __file__):
    '''
    对外方法，初始log工具类，提供其它类使用
    :param log_name:
    :return:
    '''
    return Logger(log_file=logfile,log_name=log_name,log_level=loglevel).logger


# if __name__ == "__main__":
#     my_log().debug("this is a debug")