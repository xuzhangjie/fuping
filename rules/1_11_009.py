from model import Person
from error import Error


'''
规则：通过帮扶消除致贫返贫风险的监测对象未享受帮扶措施
思路：根据（自定义）检测对象信息表中的风险消除方式和实施开发式帮扶措施情况确定规则
完成！！！
'''
def process(record: Person):
    if record.objectInfo is None:
        return
    if record.objectInfo.get('风险消除方式') == '帮扶消除' and record.objectInfo.get('实施开发式帮扶措施情况') != '已实施':
        raise Error(no='1_11_009.py', record=[record.objectInfo])

