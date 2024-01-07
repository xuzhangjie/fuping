from model import Person
from error import Error
from typing import Dict, List
from datetime import datetime

'''
规则：脱贫人口失学或辍学原因为因病或因残但健康状况为健康
完成！！！！
'''


def process(record: Person):
    if record.objectInfo is None:
        return

    if  record.objectInfo.get('义务教育阶段未上学原因') == '因病' or record.objectInfo.get('义务教育阶段未上学原因') == '因残':
        if record.objectInfo.get('健康状况') == '健康':
            msg = '脱贫{}成员失学或辍学原因为因病或因残但健康状况为健康'.format(record.idCard)
            raise Error(no='2_01_012', objectInfo=[record.objectInfo], msg=msg)
