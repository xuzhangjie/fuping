from model import Person
from error import Error
from typing import Dict, List

id2record: Dict[str, List[Person]] = {}


def process(record: Person):
    if record.objectInfo is None:
        return
    if record.idCard in id2record:
        id2record[record.idCard].append(record)
        raise Error(no='1_01_001', record=id2record[record.idCard])
    else:
        id2record[record.idCard] = [record]