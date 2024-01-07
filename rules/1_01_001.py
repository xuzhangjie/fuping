from model import Person
from error import Error
from typing import Dict, List

'''
规则：省内脱贫人口证件号码重复
完成！！！！
'''
id2record: Dict[str, List[Person]] = {}

def process(record: Person):
    if record.objectInfo is None:
        return
    if record.idCard in id2record and record.objectInfo.get('户类型') == '脱贫户':
        raise Error(no='1_01_001', objectInfo=[record.objectInfo])
    elif record.objectInfo.get('户类型') == '脱贫户':
        id2record[record.idCard] = [record]