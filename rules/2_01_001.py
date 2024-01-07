from model import Person
from error import Error
from typing import Dict, List


'''
规则：脱贫人口民族为空
完成！！！！
'''


def process(record: Person):
    if record.objectInfo is None:
        return
    if len(str(record.objectInfo.get('民族')).strip()) == 0:
        msg = '{}成员民族为空'.format(record.idCard)
        raise Error(no='2_01_001', objectInfo=[record.objectInfo], msg=msg)
