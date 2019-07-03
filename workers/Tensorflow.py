# -*- encoding: utf-8 -*-
"""
@Time    : 7/2/19 2:04 AM
@Author  : xiahaulou
@Email   : 390306467@qq.com
"""
from .Basewoker import BaseWorker


class Tensorflow(BaseWorker):
    def run(self):
        logs = self.read_from_file(mode=list)
        for log in logs:
            t, log = log
            container = []
            for _ in log:
                if _.strip().startswith("Total duration:"):
                    container.append(_.strip().split()[-2])
            self.merge([container[0]])
            self.merge([container[1]])
            self.status(t)

    def to_excel(self):
        pass