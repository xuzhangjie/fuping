from model import Person
from error import Error
from typing import Dict, List
from datetime import datetime


'''
规则：监测对象人口高中和中职教育小于15岁和大于20岁
思路：根据（自定义）监测对象信息表的在校生状况筛选出高中和中职教育，检测对象人口为整个表的对象，用至今的日期减去出生日期计算年龄，小于15岁或大于20岁的信息抛出
完成！！！！
'''

def process(record: Person):
    if record.objectInfo is None:
        return
    grade = str(record.objectInfo.get('在校生状况'))
    if '普通高中' in grade or '中职' in grade:
        birthstr = record.objectInfo.get('出生日期')
        birthDate = datetime.strptime(birthstr, "%Y%m%d")
        currentDate = datetime.now()
        age = currentDate.year - birthDate.year - ((currentDate.month, currentDate.day) < (birthDate.month, birthDate.day))
        if age < 15 or age > 20:
            msg = '{}{}小于15岁或大于20岁'.format(record.idCard,grade)
            raise Error(no='5_12_016', objectInfo=[record.objectInfo], msg=msg)