from typing import List
from model import Person


class Error(Exception):
    no: str
    msg: str
    record: List[Person]

    def __init__(self, no: str, record: List[Person], msg: str = None):
        self.no = no
        self.msg = msg
        self.record = record
