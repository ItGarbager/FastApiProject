"""
@Time    : 2021/11/16 15:19
@Author  : Musuer
@Contact : linxuzhao2018@163.com
@File    : extension.py
@Software: PyCharm
"""
import base64
import json
import os
from datetime import date, datetime, timedelta
from time import localtime, strftime

import pytz
from fastapi.responses import JSONResponse

from FastApiProject.config import TIME_ZONE


class MyEncoder(json.JSONEncoder):
    # 重写 json.dumps
    def default(self, obj):
        # if isinstance(obj, datetime.datetime):
        #     return int(mktime(obj.timetuple()))
        if isinstance(obj, datetime):
            utc_timezone = pytz.timezone(TIME_ZONE)  # 定义上海时区的对象
            obj = obj.astimezone(utc_timezone)  # 将当前的时间转换为上海的时间
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


# 检查文件夹是否存在，不存在创建
def mkdir(path: str) -> None:
    if not os.path.isdir(path):
        os.makedirs(path)


# 检查文件是否存在
def isfile(file: str) -> bool:
    return os.path.isfile(file)


# 使用自己的 encoder
def loadJson(data):
    data = json.loads(json.dumps(data, cls=MyEncoder))
    return data


# 全局 json 返回格式
def return_json_response(data=None, status_code=200, message='success', response=None):
    if data is None:
        data = None
    data = loadJson(data)
    if response is None:
        response = {
            "code": status_code,
            "data": data,
            "message": message
        }
    return JSONResponse(response, status_code=status_code)


# 错误日志
def err_log(filename, err):
    local_time = get_local_time()
    filename = './log/err/' + filename
    path = os.path.dirname(filename)
    mkdir(path)
    filename = filename + f'-{local_time}.log'
    with open(filename, "a") as f:
        f.write(f"[{get_local_time('%H:%M:%S')}] => {str(err)}\n")
        f.close()


# 接口或系统异常返回
def response_err(message='Error', status_code=500):
    return return_json_response(status_code=status_code, message=str(message))


# 获取当前时间
# param format_time 时间格式化
def get_local_time(format_time='%y%m%d'):
    time_str = datetime.now().strftime(format_time)
    return time_str


# 检查是否是当天的文件
def is_today(path):
    filemt = localtime(os.path.getmtime(path))
    target_date = strftime("%Y-%m-%d", filemt)

    c_year = datetime.now().year
    c_month = datetime.now().month
    c_day = datetime.now().day

    date_list = target_date.split("-")
    t_year = int(date_list[0])
    t_month = int(date_list[1])
    t_day = int(date_list[2])

    return c_year == t_year and c_month == t_month and c_day == t_day


# 获取进几次的日期周一到周天
def get_current_week():
    one_day = timedelta(days=1)
    monday, sunday = date.today() - 7 * one_day, date.today() - 7 * one_day
    while monday.weekday() != 0:
        monday -= one_day
    while sunday.weekday() != 6:
        sunday += one_day
    # 返回当前的星期一和星期天的日期
    fmt = "%Y-%m-%d"
    return date.strftime(monday, fmt), date.strftime(sunday, fmt)


def enc_b64(code):
    bytes_url = code.encode("utf-8")
    str_url = base64.b64encode(bytes_url).decode("utf-8")  # 被编码的参数必须是二进制数据

    return str_url
