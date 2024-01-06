from typing import List
from model import DictRecord


class Error(Exception):
    no: str
    msg: str
    objectInfo: List[DictRecord] = None  # (基础信息) 监测对象信息
    huInfo: List[DictRecord] = None  # (乡村建设) 户信息
    outInfo: List[DictRecord] = None  # (外出务工)
    previewInfo: List[DictRecord] = None  # (计划外出务工)
    countryInfo: List[DictRecord] = None  # (行政村)

    def __init__(self, no: str, objectInfo: List[DictRecord] = None, huInfo: List[DictRecord] = None,
                 outInfo: List[DictRecord] = None,
                 previewInfo: List[DictRecord] = None,
                 countryInfo: List[DictRecord] = None,
                 msg: str = None) -> object:
        self.no = no
        self.msg = msg
        self.objectInfo = objectInfo
        self.huInfo = huInfo
        self.outInfo = outInfo
        self.previewInfo = previewInfo
        self.countryInfo = countryInfo

    def __str__(self):
        return f'违反规则{self.no}'
