# -*- encoding: utf-8 -*-
from .Basewoker import BaseWorker


class Cassandra(BaseWorker):
    def run(self):
        logs = self.read_from_file(mode=list)
        # print(logs)
        for log in logs:
            t, log = log
            try:
                s1_list = []
                s2_list = []
                patt = r'Op rate|Latency mean'
                pattern = self.re.compile(patt)
                test_list = []
                for line in log:
                    result = self.re.findall(pattern, line)
                    if (result):
                        test_list.append(line.split()[3])
                s1_list.extend(test_list[:2])
                s1_list.extend(test_list[len(test_list)//2-11:len(test_list)//2-1])
                s2_list.extend(test_list[len(test_list)//2:len(test_list)//2+2])
                s2_list.extend(test_list[-10:])
                if len(s1_list) != 12 or len(s2_list) != 12:
                    self.failed(t, 'error logfile')
                    self.merge(None)
                    continue
                self.merge(s1_list)
                self.merge(s2_list)
                self.status(t)
            except Exception as Ex:
                self.failed(t, Ex)
                self.merge(None)
                continue


    def to_excel(self):
        pass
