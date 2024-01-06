import importlib
import os
from tqdm import tqdm
from typing import Dict, Set, List
import pandas as pd

from error import Error
from model import Area, Family, Person, DictRecord
import openpyxl

records = set()
errors_records: Dict[str, Dict[str, Set[DictRecord]]] = {}
countryRecords: List[DictRecord] = []


def read_excel(path: str, header: int):
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
            yield DictRecord({key: cell.value for (key, cell) in zip(headers, row)})


def load_data(path):
    objectInfo = pd.read_excel('./data/（自定义）监测对象信息 (22).xlsx', header=2, dtype=str, keep_default_na=False).to_dict(orient='records')
    huInfo = pd.read_excel('./data/（乡村建设）户信息_20231218.xlsx', header=2, dtype=str, keep_default_na=False).to_dict(orient='records')
    outInfo = pd.read_excel('./data/（务工月监测）已外出务工信息_20231218.xlsx', header=2, dtype=str, keep_default_na=False).to_dict(orient='records')
    previewInfo = pd.read_excel('./data/计划外出务工信息_20231218.xlsx', header=2, dtype=str, keep_default_na=False).to_dict(orient='records')
    countryInfo = pd.read_excel('./data/（自定义）行政村信息.xlsx', header=2, dtype=str, keep_default_na=False).to_dict(orient='records')
    return objectInfo, huInfo, outInfo, previewInfo, countryInfo


def construct_model():
    objectInfo, huInfo, outInfo, previewInfo, countryInfo = load_data('')
    area = Area()
    for row in tqdm(objectInfo, desc='构建监测对象表', unit='条'):
        row = DictRecord(row)
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
        row = DictRecord(row)
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
        row = DictRecord(row)
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
        row = DictRecord(row)
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
    for row in tqdm(countryInfo, desc='构建行政村', unit='条'):
        row = DictRecord(row)
        countryRecords.append(row)
        section: Dict[str, Family] = area.get([row.get('县'), row.get('乡'), row.get('村')])
        if section is not None:
            for family in section.values():
                for person in family.member:
                    person.countryInfo = row

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


def load_rules(path):
    rules = []
    for filepath in walk(path):
        if filepath.endswith('.py'):
            packages = filepath.split(os.path.sep)
            packages[-1] = packages[-1].rstrip('.py')
            package = '.'.join(packages)
            module = importlib.import_module(package)
            rules.append(module.process)
    return rules


def export_excel():
    # table_to_excel = {
    #     "自定义基础表": "./data/（基础信息）户信息_20231218.xlsx",
    #     "务工月监测已外出务工表": "./data/（务工月监测）已外出务工信息_20231218.xlsx",
    #     "务工月监测计划外出务工表": "./data/计划外出务工信息_20231218.xlsx",
    #     "乡村建设基础表": "./data/（乡村建设）户信息_20231218.xlsx"
    # }
    #
    # export_listing = pd.read_excel("./data/20231216 豁免清单总梳理.xlsx")
    # row = export_listing.loc[export_listing["编号"] == rule]
    # tables : str = row.loc[0, "Unnamed: 11"].split("、")
    # for table in tables:
    #     if table not in table_to_excel.keys():
    #         continue
    #     # 加载需要导出的表头信息
    #     df = pd.read_excel(table_to_excel[table])
    #     # 获取表头信息
    #     headers = df.columns.tolist()
    #     print()
    # print()
    try:
        os.mkdir('result')
    except:
        pass
    for no, errors in errors_records.items():
        with pd.ExcelWriter(f'./result/{no}.xlsx') as writer:
            for sheet_name, data in errors.items():
                pd.DataFrame(data).to_excel(writer, sheet_name=sheet_name, index=False)


def process():
    rules = load_rules('rules')
    countrysideRules = load_rules('countryside')
    for rule in rules:
        for record in records:
            try:
                rule(record)
            except Error as e:
                print(e)
                if e.no not in errors_records:
                    errors_records[e.no] = {key: set() for key in ['自定义基础表', '务工月监测已外出务工表', '务工月监测计划外出务工表', '乡村建设基础表', '自定义行政村表']}
                no = errors_records[e.no]
                if e.objectInfo is not None:
                    no.get('自定义基础表').update(set(e.objectInfo))

                if e.outInfo is not None:
                    no.get('务工月监测已外出务工表').update(set(e.outInfo))

                if e.huInfo is not None:
                    no.get('乡村建设基础表').update(set(e.huInfo))

                if e.previewInfo is not None:
                    no.get('务工月监测计划外出务工表').update(set(e.previewInfo))

                if e.countryInfo is not None:
                    no.get('自定义行政村表').update(set(e.countryInfo))
    for rule in countrysideRules:
        for record in countryRecords:
            try:
                rule(record)
            except Error as e:
                print(e)
                if e.no not in errors_records:
                    errors_records[e.no] = {key: set() for key in
                                            ['自定义基础表', '务工月监测已外出务工表', '务工月监测计划外出务工表', '乡村建设基础表', '自定义行政村表']}
                no = errors_records[e.no]
                if e.countryInfo is not None:
                    no.get('自定义行政村表').update(set(e.countryInfo))


if __name__ == '__main__':
    construct_model()
    process()
    export_excel()