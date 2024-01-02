import importlib
import os

import pandas as pd

from error import Error
from model import Area, Family, Person

records = set()


def load_data(path):
    objectInfo = pd.read_excel('./data/（自定义）监测对象信息 (22).xlsx', header=2).to_dict(orient='records')
    huInfo = pd.read_excel('./data/（乡村建设）户信息_20231218.xlsx', header=2).to_dict(orient='records')
    outInfo = pd.read_excel('./data/（务工月监测）已外出务工信息_20231218.xlsx', header=2).to_dict(orient='records')
    previewInfo = pd.read_excel('./data/计划外出务工信息_20231218.xlsx', header=2).to_dict(orient='records')
    countryInfo = pd.read_excel('./data/（自定义）行政村信息.xlsx', header=2).to_dict(orient='records')
    return objectInfo, huInfo, outInfo, previewInfo, countryInfo


def construct_model():
    objectInfo, huInfo, outInfo, previewInfo, countryInfo = load_data('')
    area = Area()
    for row in objectInfo:
        huId = row.get('户编号')
        family: Family = area.get([row.get('县'), row.get('乡'), row.get('村'), row.get('户编号')])
        if family is None:
            family = Family(huId)
            area.append([row.get('县'), row.get('乡'), row.get('村')], family)
        person = Person(row.get('证件号码'), objectInfo=row)
        person.family = family
        records.add(person)
        family.append(person)

    for row in huInfo:
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

    for row in outInfo:
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

    for row in previewInfo:
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