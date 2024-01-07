from model import Person
from error import Error
from typing import Dict, List


'''
规则：脱贫人口与户主关系与性别指标值逻辑错误
完成！！！！
'''

is_male = ['之子', '之曾孙子', '之父', '之公公', '之女婿', '之叔伯', '之孙子', '之外孙子', '之兄弟姐妹', '之岳父', '之侄儿', '之祖父','配偶','其他']
is_female =['之女', '之曾孙女', '之儿媳', '之母', '之婆婆', '之孙女', '之外孙女', '之兄弟姐妹', '之兄弟媳妇', '之岳母', '之侄女', '之祖母','配偶','其他']

def process(record: Person):
    if record.objectInfo is None:
        return
    if record.objectInfo.get('性别') == 1 and record.objectInfo.get('与户主关系') not in is_male:
        raise Error(no='2_01_004', objectInfo=[record.objectInfo])
    elif record.objectInfo.get('性别') == 2 and record.objectInfo.get('与户主关系') not in is_female:
        raise Error(no='2_01_004', objectInfo=[record.objectInfo])

