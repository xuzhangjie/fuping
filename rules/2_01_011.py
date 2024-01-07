from model import Person
from error import Error
from typing import Dict, List
from datetime import datetime

'''
规则：16岁（不含）以下脱贫人口劳动能力不是无劳动能力
完成！！！！
'''


def process(record: Person):
    if record.objectInfo is None:
        return
    birthstr = record.objectInfo.get('出生日期')
    birthDate = datetime.strptime(birthstr, "%Y%m%d")
    currentDate = datetime.now()
    age = currentDate.year - birthDate.year - ((currentDate.month, currentDate.day) < (birthDate.month, birthDate.day))
    if age < 16 and record.objectInfo.get('劳动技能') != '无劳动力':
        msg = '脱贫{}成员{}岁劳动能力不是无劳动能力'.format(record.idCard, age)
        raise Error(no='2_01_011', objectInfo=[record.objectInfo], msg=msg)
