from model import Person
from error import Error
from typing import Dict, List


'''
规则：防止返贫监测对象人口身份证号不符合校验规则（特指18位证件号码）
思路：防止返贫监测对象的范围为检测对象类别为【脱贫不稳定户、边缘易致贫户】的检测对象；
完成！！！！
'''
checksum_dict = {0:'1', 1:'0', 2:'X', 3:'9', 4:'8', 5:'7', 6:'6', 7:'5', 8:'4', 9:'3', 10:'2'}
unstable_types = ['脱贫不稳定户', '边缘易致贫户']
def check_id(id: str) -> bool:
    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    factors = [int(id[i]) * weights[i] for i in range(17)]
    checksum = sum(factors) % 11
    return checksum_dict.get(checksum) == id[17]

def process(record: Person):
    if record.objectInfo is None:
        return
    if record.objectInfo.get('检测对象类别') in unstable_types:
        if len(record.idCard) == 18:
            if not check_id(record.idCard):
                msg = '{}成员证件号码不符合校验规则'.format(record.idCard)
                raise Error(no='1_12_003', objectInfo=[record.objectInfo], msg=msg)
