from model import Person
from error import Error
from typing import Dict, List


'''
规则：脱贫人口劳动技能为空
完成！！！！
'''


def process(record: Person):
    if record.objectInfo is None:
        return
    if len(str(record.objectInfo.get('劳动技能')).strip()) == 0:
        msg = '{}劳动技能为空'.format(record.idCard)
        raise Error(no='2_01_003', objectInfo=[record.objectInfo], msg=msg)
