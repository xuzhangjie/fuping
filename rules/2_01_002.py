from model import Person
from error import Error
from typing import Dict, List


'''
规则：脱贫人口健康状况为空
完成！！！！
'''


def process(record: Person):
    if record.objectInfo is None:
        return
    if len(str(record.objectInfo.get('健康状况')).strip()) == 0:
        msg = '{}健康状况为空'.format(record.idCard)
        raise Error(no='2_01_002', objectInfo=[record.objectInfo], msg=msg)
