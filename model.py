from __future__ import annotations

from typing import List, NewType, TypeVar, Dict, Optional, Generic
from uuid import uuid4


class DictRecord(dict):
    __uid = uuid4()
    
    def __hash__(self):
        return hash(self.__uid)


class Person:
    idCard: str = None
    objectInfo: DictRecord = None  # (基础信息) 监测对象信息
    huInfo: DictRecord = None  # (乡村建设) 户信息
    outInfo: List[DictRecord] = None  # (外出务工)
    previewInfo: List[DictRecord] = None  # (计划外出务工)
    countryInfo: DictRecord = None  # (行政村)
    family: 'Family' = None
    __uid = uuid4()

    def __init__(self, idCard, objectInfo=None, huInfo=None, outInfo=None, previewInfo=None, countryInfo=None):
        self.idCard = idCard
        self.objectInfo = objectInfo
        self.huInfo = huInfo
        self.outInfo = outInfo
        self.previewInfo = previewInfo
        self.countryInfo = countryInfo

    def merge(self, other: 'Person'):
        if self.objectInfo is None and other.objectInfo is not None:
            self.objectInfo = other.objectInfo

        if self.countryInfo is None and other.countryInfo is not None:
            self.countryInfo = other.countryInfo

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
        return hash(self.__uid)


class Family:
    member: List[Person] = None
    host: Person = None

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
            ret = last
        else:
            self.member.append(person)
            ret = person
        if ret.objectInfo is not None and ret.objectInfo.get("与户主关系") == '户主':
            self.host = ret
        return ret

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
        self.area: DictRecord[str, DictRecord[str, DictRecord[str, DictRecord[str, Family]]]] = DictRecord()

    def append(self, area: List[str], family: Family):
        """
        :param family:
        :param area: List[str]  #  县 / 乡 / 行政村
        :return:
        """
        top: DictRecord = self.area

        for i in area:
            if i not in top:
                top[i] = {}
            top = top[i]
        top[family.id] = family

    def get(self, area: List[str]) -> DictRecord | Family | None:
        top: DictRecord | Family = self.area
        for i in area:
            if i in top:
                top = top[i]
            else:
                return None
        return top


if __name__ == '__main__':

    a = Area()
    print(1)