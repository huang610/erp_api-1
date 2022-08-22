import os
import yaml


class YamlReader:
    def __init__(self,yamlf):
        '''
        初始化，文件是否存在
        :param yamlf:
        :return:
        '''
        if os.path.exists(yamlf):
            self.yamlf = yamlf
        else:
            raise FileNotFoundError("文件不存在")
        self._data = None
        self._data_all = None

    def data(self):
        '''
        第一次调用data，单个yaml文档读取，如果不是，直接返回之前保存的数据
        :return:
        '''
        if not self._data:
            with open(self.yamlf,"rb") as f:
                self._data = yaml.safe_load(f)
        return self._data

    def data_all(self):
        #第一次调用data，多个yaml文档读取，如果不是，直接返回之前保存的数据
        if not self._data_all:
            with open(self.yamlf,"rb") as f:
                self._data_all = list(yaml.safe_load_all(f))
        return self._data_all