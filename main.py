import importlib
import os
from tqdm import tqdm

import pandas as pd

from error import Error
from model import Area, Family, Person
import openpyxl

records = set()


def load_execl(path: str, header: int):
    wb = openpyxl.load_workbook(path, read_only=True)
    ws = wb.active
    ws.reset_dimensions()
    headers = []
    for idx, row in enumerate(ws.rows):
        if idx < header:
            continue
        if idx == header:
            for j in row:
                headers.append(j.value)
        else:
            yield {key: cell.value for (key, cell) in zip(headers, row)}


def load_data(path):
    objectInfo = load_execl('./data/（自定义）监测对象信息 (22).xlsx', header=2)
    huInfo = load_execl('./data/（乡村建设）户信息_20231218.xlsx', header=2)
    outInfo = load_execl('./data/（务工月监测）已外出务工信息_20231218.xlsx', header=2)
    previewInfo = load_execl('./data/计划外出务工信息_20231218.xlsx', header=2)
    countryInfo = load_execl('./data/（自定义）行政村信息.xlsx', header=2)
    return objectInfo, huInfo, outInfo, previewInfo, countryInfo


def construct_model():
    objectInfo, huInfo, outInfo, previewInfo, countryInfo = load_data('')
    area = Area()
    for row in tqdm(objectInfo, desc='构建监测对象表', unit='条'):
        huId = row.get('户编号')
        family: Family = area.get([row.get('县'), row.get('乡'), row.get('村'), row.get('户编号')])
        if family is None:
            family = Family(huId)
            area.append([row.get('县'), row.get('乡'), row.get('村')], family)
        person = Person(row.get('证件号码'), objectInfo=row)
        person.family = family
        records.add(person)
        family.append(person)

    for row in tqdm(huInfo, desc='构建户信息表', unit='条'):
        person = Person(row.get('证件号码'), huInfo=row)
        family: Family = area.get([row.get('县(市、区、旗)'), row.get('乡(镇)'), row.get('行政村'), row.get('户编号')])
        if family is not None:
            person = family.append(person)
        else:
            huId = row.get('户编号')
            family = Family(huId)
            person.family = family
            person = family.append(person)
            area.append([row.get('县(市、区、旗)'), row.get('乡(镇)'), row.get('行政村')], family)
        records.add(person)

    for row in tqdm(outInfo, desc='构建外出务工信息表', unit='条'):
        person = Person(row.get('证件号码'), outInfo=[row])
        family: Family = area.get([row.get('县'), row.get('乡'), row.get('行政村'), row.get('户编号')])
        if family is not None:
            person = family.append(person)
        else:
            huId = row.get('户编号')
            family = Family(huId)
            person.family = family
            person = family.append(person)
            area.append([row.get('县'), row.get('乡'), row.get('行政村')], family)
        records.add(person)

    for row in tqdm(previewInfo, desc='构建计划外出务工表', unit='条'):
        person = Person(row.get('证件号码'), previewInfo=[row])
        family: Family = area.get([row.get('县'), row.get('乡'), row.get('行政村'), row.get('户编号')])
        if family is not None:
            person = family.append(person)
        else:
            huId = row.get('户编号')
            family = Family(huId)
            person = family.append(person)
            person.family = family
            area.append([row.get('县'), row.get('乡'), row.get('行政村')], family)
        records.add(person)
    print('模型建立完毕')


def walk(root_path, exclude=None):
    """
    遍历指定目录及其子目录下的所有文件

    :param root_path: 遍历的根目录
    :param exclude: 需要忽略的目录名列表
    """

    if exclude is None:
        exclude = []

    for dirpath, dirnames, filenames in os.walk(root_path):
        # 排除需要忽略的目录
        for e in exclude:
            if e in dirnames:
                dirnames.remove(e)
        for filename in filenames:
            if filename not in exclude:
                yield os.path.join(dirpath, filename)


def load_rules():
    rules = []
    for filepath in walk('rules'):
        if filepath.endswith('.py'):
            packages = filepath.split(os.path.sep)
            packages[-1] = packages[-1].rstrip('.py')
            package = '.'.join(packages)
            module = importlib.import_module(package)
            rules.append(module.process)
    return rules


def process():
    rules = load_rules()
    for record in records:
        for rule in rules:
            try:
                rule(record)
            except Error as e:
                print(e)


if __name__ == '__main__':
    construct_model()
    process()