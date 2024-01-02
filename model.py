from typing import List, NewType, TypeVar, Dict, Optional, Generic
from uuid import uuid4


class Person:
    idCard: str = None
    objectInfo: Dict = None  # (基础信息) 监测对象信息
    huInfo: Dict = None  # (乡村建设) 户信息
    outInfo: List[Dict] = None  # (外出务工)
    previewInfo: List[Dict] = None  # (计划外出务工)
    family: 'Family' = None
    uid = uuid4()

    def __init__(self, idCard, objectInfo=None, huInfo=None, outInfo=None, previewInfo=None):
        self.idCard = idCard
        self.objectInfo = objectInfo
        self.huInfo = huInfo
        self.outInfo = outInfo
        self.previewInfo = previewInfo

    def merge(self, other: 'Person'):
        if self.objectInfo is None and other.objectInfo is not None:
            self.objectInfo = other.objectInfo

        if self.huInfo is None and other.huInfo is not None:
            self.huInfo = other.huInfo

        if self.outInfo is None and other.outInfo is not None:
            self.outInfo = other.outInfo
        elif self.outInfo is not None and other.outInfo is not None:
            self.outInfo.extend(other.outInfo)

        if self.previewInfo is None and other.previewInfo is not None:
            self.previewInfo = other.previewInfo
        elif self.previewInfo is not None and other.previewInfo is not None:
            self.previewInfo.extend(other.previewInfo)

    def __eq__(self, other):
        if isinstance(other, Person):
            return other.idCard == self.idCard
        return False

    def __hash__(self):
        return hash(self.uid)


class Family:
    member: List[Person] = None

    def __init__(self, fid: str):
        self.id = fid
        self.member = []

    def append(self, person: Person):
        last = None
        for i in self.member:
            if i == person:
                last = i
                break
        if last is not None:
            last.merge(person)
            return last
        else:
            self.member.append(person)
            return person

    def pop(self, index):
        return self.member.pop(index)

    def __eq__(self, other):
        if isinstance(other, Family):
            return other.id == self.id
        elif type(other) == str:
            return self.id == other
        return False


class Area:
    def __init__(self):
        self.area: Dict[str, Dict[str, Dict[str, Dict[str, Family]]]] = dict()

    def append(self, area: List[str], family: Family):
        """
        :param family:
        :param area: List[str]  #  县 / 乡 / 行政村
        :return:
        """
        top: Dict = self.area

        for i in area:
            if i not in top:
                top[i] = {}
            top = top[i]
        top[family.id] = family

    def get(self, area: List[str]) -> Dict | Family | None:
        top: Dict | Family = self.area
        for i in area:
            if i in top:
                top = top[i]
            else:
                return None
        return top


if __name__ == '__main__':

    a = Area()
    print(1)