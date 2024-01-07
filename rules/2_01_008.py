from model import Person
from error import Error
from typing import Dict, List


'''
规则：脱贫人口是否参加城乡居民（城镇职工）基本医疗保险同时为空或否
完成！！！！
'''


def process(record: Person):
    if record.objectInfo is None:
        return

    if len(str(record.objectInfo.get('是否参加城乡居民基本医疗保险')).strip()) == 0 and len(str(record.objectInfo.get('是否参加城镇职工基本医疗保险')).strip()) == 0:
        msg = '脱贫{}成员是否参加城乡居民（城镇职工）基本医疗保险同时为空'.format(record.idCard)
        raise Error(no='2_01_008', objectInfo=[record.objectInfo], msg=msg)
    elif str(record.objectInfo.get('是否参加城乡居民基本医疗保险').strip()) == '否' and str(record.objectInfo.get('是否参加城镇职工基本医疗保险')).strip() == '否':
        msg = '脱贫{}成员是否参加城乡居民（城镇职工）基本医疗保险同时为否'.format(record.idCard)
        raise Error(no='2_01_008', objectInfo=[record.objectInfo], msg=msg)
