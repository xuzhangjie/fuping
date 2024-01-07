from model import Person
from error import Error
from datetime import  datetime

'''
规则：防止返贫监测对象户识别后1个月及以上未落实帮扶措施
思路：防止返贫监测对象的范围为检测对象类别为【脱贫不稳定户、边缘易致贫户】的检测对象；
     计算识别检测时间至今的用时，再判断实施开发式帮扶情况一列的信息
完成！！！
'''
unstable_types = ['脱贫不稳定户', '边缘易致贫户']
def process(record: Person):
    if record.objectInfo is None:
        return
    data = record.objectInfo.get('识别监测时间')
    if record.objectInfo.get('检测对象类别') in unstable_types:
        if len(str(data).strip()) == 6:
            recognition_date = datetime.strptime(data,"%Y%m")
            today_date = datetime.now()
            if today_date.year == recognition_date.year:
                date_difference = today_date.month - recognition_date.month
            else:
                if (today_date.year - recognition_date.year) == 1:
                    date_difference = (12-recognition_date.month) + today_date.month
                else:
                    date_difference =(today_date.year - recognition_date.year - 1)*12 + (12 - recognition_date.month) + today_date.month
            if date_difference > 1 and record.objectInfo.get('实施开发式帮扶措施情况') == '尚未实施':
                raise Error(no='1_11_010.py', objectInfo=[record.objectInfo])






