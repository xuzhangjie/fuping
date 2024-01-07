from model import Person
from error import Error
from typing import Dict, List
from datetime import datetime


'''
规则：脱贫人口小学小于6岁和大于十四岁
思路：根据（自定义）监测对象信息表的在校生状况筛选出小学生和脱贫户，用至今的日期减去出生日期计算年龄，小于6岁或大于14岁的信息抛出
完成！！！！
'''

def process(record: Person):
    if record.objectInfo is None:
        return
    if record.objectInfo.get('在校生状况') == '小学' and record.objectInfo.get('户类型') == '脱贫户':
        birthstr = record.objectInfo.get('出生日期')
        birthDate = datetime.strptime(birthstr, "%Y%m%d")
        currentDate = datetime.now()
        age = currentDate.year - birthDate.year - ((currentDate.month, currentDate.day) < (birthDate.month, birthDate.day))
        if age < 6 or age > 14:
            msg = '{}小学小于6岁或大于14岁'.format(record.idCard)
            raise Error(no='5_17_002', objectInfo=[record.objectInfo], msg=msg)



