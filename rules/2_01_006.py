from model import Person
from error import Error
from typing import Dict, List


'''
规则：脱贫人口是否参加大病保险为空
完成！！！！
'''


def process(record: Person):
    if record.objectInfo is None:
        return
    if len(str(record.objectInfo.get('是否参加大病保险')).strip()) == 0 and str(record.objectInfo.get('户类型')) == '脱贫户':
        msg = '脱贫{}成员是否参加大病保险为空'.format(record.idCard)
        raise Error(no='2_01_006', objectInfo=[record.objectInfo], msg=msg)
