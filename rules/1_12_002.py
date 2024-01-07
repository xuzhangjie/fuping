from model import Person
from error import Error
from typing import Dict, List


'''
规则：防止返贫监测对象人口证件号码位数异常（证件号码非18、20、22位）
思路：防止返贫监测对象的范围为检测对象类别为【脱贫不稳定户、边缘易致贫户】的检测对象；
完成！！！！
'''

unstable_types = ['脱贫不稳定户', '边缘易致贫户']
def process(record: Person):
    if record.objectInfo is None:
        return
    standard_num = [18, 20, 22]
    if record.objectInfo.get('检测对象类别') in unstable_types:
        if len(record.idCard) not in standard_num:
            msg = '{}成员证件号码位数异常'.format(record.idCard)
            raise Error(no='1_12_002', objectInfo=[record.objectInfo], msg=msg)
