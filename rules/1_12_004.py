from model import Person
from error import Error
from typing import Dict, List


'''
规则：防止返贫监测对象人口残疾人证不符合校验规则

'''
huID = []
checksum_dict = {0:'1', 1:'0', 2:'X', 3:'9', 4:'8', 5:'7', 6:'6', 7:'5', 8:'4', 9:'3', 10:'2'}
def check_id(id: str) -> bool:
    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    factors = [int(id[i]) * weights[i] for i in range(17)]
    checksum = sum(factors) % 11
    require_1 = checksum_dict.get(checksum) == id[17]
    require_2 = id[18] <= 7
    return require_2 and require_1

unstable_type = ['脱贫不稳定户', '边缘易致贫户']
def process(record: Person):
    if record.objectInfo is None:
        return
    if record.objectInfo.get('监测对象类别')  in unstable_type:
        if len(record.idCard) == 20:
            if not check_id(record.idCard):
                raise Error(no='1_12_004', objectInfo=[record.objectInfo])





