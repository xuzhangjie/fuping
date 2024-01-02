from model import Person
from error import Error

def process(record: Person):
    if record.objectInfo is None:
        return
    res = record.objectInfo.get('识别监测时间')
    print(11)
