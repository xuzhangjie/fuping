from model import Person
from error import Error
from typing import Dict, List


'''
规则：脱贫户未解决安全饮用水但未纳入防止返贫监测对象
完成！！！
'''


def process(record: Person):
    if record.objectInfo is None:
        return
    if record.objectInfo.get('户类型') == '脱贫户' and record.objectInfo.get('是否解决安全饮用水') == '否':
        if len(str(record.objectInfo.get('监测对象类别')).strip()) == 0:
            raise Error(no='1_02_002', objectInfo=[record.objectInfo])

