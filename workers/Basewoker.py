# -*- encoding: utf-8 -*-
"""
@Time    : 7/1/19 1:26 AM
@Author  : xiahaulou
@Email   : 390306467@qq.com
"""
from libs import config
import abc
import pandas as pd
import numpy as np
import re
import time
import os
import sys


class BaseWorker(metaclass=abc.ABCMeta):
    def __init__(self):
        self.pd = pd
        self.np = np
        self.re = re
        self.times = config.config.getint('test_times', 'times')
        self.containers = []

    @abc.abstractclassmethod
    def run(self):
        pass

    @abc.abstractclassmethod
    def to_excel(self):
        pass

    @staticmethod
    def swap(*args):
        data, pos_one, pos_two = args
        temp = data[pos_one]
        data[pos_one] = data[pos_two]
        data[pos_two] = temp

    @staticmethod
    def now():
        return time.strftime("%Y%m%d", time.localtime())

    def to_csv(self, t, df):
        micro = type(self).__name__.lower()
        micro_path = os.path.join(os.getcwd(), 'data/csv/{}'.format(micro))
        if not os.path.exists(micro_path):
            os.mkdir(micro_path)
        df.to_csv(os.path.join(micro_path, '{}.csv'.format(t)),
                  index=None, header=None, encoding='utf-8')

    @property
    def datest_logs(self):
        path = self.get_logfiles(os.path.join(os.getcwd(), 'data/log'), [])
        if sys.platform in ['win32', 'win64', 'cygwin']:
            path = [_ for _ in path if _.split('\\')[-1].startswith(type(self).__name__.lower())]
            path = sorted(path, key=lambda s: s.split('\\')[-1], reverse=True)[:self.times]
        else:
            path = [_ for _ in path if _.split('/')[-1].startswith(type(self).__name__.lower())]
            path = sorted(path, key=lambda s: s.split('/')[-1], reverse=True)[:self.times]
        return path

    def read_from_file(self, mode=list):
        logs = []
        files = self.datest_logs
        try:
            for _ in files:
                with open(_, 'r') as f:
                    if sys.platform in ['win32', 'win64', 'cygwin']:
                        if mode is list:
                            logs.append((_.split('\\')[-1].split('.log')[0], f.readlines()))
                        elif mode is str:
                            logs.append((_.split('\\')[-1].split('.log')[0], f.read()))
                    else:
                        if mode is list:
                            logs.append((_.split('/')[-1].split('.log')[0], f.readlines()))
                        elif mode is str:
                            logs.append((_.split('/')[-1].split('.log')[0], f.read()))
        except Exception as Ex:
            print(Ex)
        return logs

    @classmethod
    def get_logfiles(cls, dir, fileList):
        newDir = dir
        if os.path.isfile(dir):
            fileList.append(dir)
        elif os.path.isdir(dir):
            for s in os.listdir(dir):
                newDir = os.path.join(dir, s)
                cls.get_logfiles(newDir, fileList)
        return fileList

    def status(self, t):
        print('task {} done, Status:Sucess'.format(t))
        pass

    def merge(self, data):
        '''
        :param data: type list,docker data or clear data
        :return:
        '''
        container_name = '{}_container'.format(type(self).__name__.lower())
        _container = getattr(self, container_name)
        _container.append(data)
        if len(_container) == self.times * 2:
            ret_index_odd = []
            ret_index_even = []
            for _ in range(len(_container)):
                if _ % 2 == 0:
                    ret_index_even.append(_container[_])
                else:
                    ret_index_odd.append(_container[_])
            ret_index_even.extend(ret_index_odd)
            _container.clear()
            df = self.pd.DataFrame(ret_index_even).T
            self.to_csv('{}{}'.format(type(self).__name__.lower(), self.now()), df)
