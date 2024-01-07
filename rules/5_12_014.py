from model import Person
from error import Error
from typing import Dict, List
from datetime import datetime


'''
规则：监测对象人口小学小于6岁和大于十四岁
思路：根据（自定义）监测对象信息表的在校生状况筛选出小学生，检测对象人口为整个表的对象，用至今的日期减去出生日期计算年龄，小于6岁或大于14岁的信息抛出
完成！！！！
'''

def process(record: Person):
    if record.objectInfo is None:
        return
    if record.objectInfo.get('在校生状况') == '小学':
        birthstr = record.objectInfo.get('出生日期')
        birthDate = datetime.strptime(birthstr, "%Y%m%d")
        currentDate = datetime.now()
        age = currentDate.year - birthDate.year - ((currentDate.month, currentDate.day) < (birthDate.month, birthDate.day))
        if age < 6 or age > 14:
            msg = '{}小学小于6岁或大于14岁'.format(record.idCard)
            raise Error(no='5_12_014', objectInfo=[record.objectInfo], msg=msg)
