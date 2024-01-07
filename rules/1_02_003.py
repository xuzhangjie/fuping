from model import Person
from error import Error
from typing import Dict, List


'''
规则：脱贫户有患病成员未参加大病保险但未纳入监测对象
完成！！！
'''

huID = []
def process(record: Person):
    if record.objectInfo is None:
        return
    error_list = []
    if record.objectInfo.get('户类型') == '脱贫户' and record.objectInfo.get('户编号') not in huID:
        sick_list = []
        for member in record.family.member:
            if member.objectInfo.get('是否参加大病保险') == '否' and member.objectInfo.get('健康状况') != '健康':
                sick_list.append(member.objectInfo)
    huID.append(record.objectInfo.get('户编号'))
    if len(sick_list) != 0:
        for member in record.family.member:
            if len(str(member.objectInfo.get('监测对象类别'))) == 0:
                error_list.append(member.objectInfo)
        raise  Error(no='1_02_003', objectInfo=error_list)



