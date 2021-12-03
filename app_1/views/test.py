"""
@Time    : 2021/11/18 11:39
@Author  : Musuer
@Contact : linxuzhao2018@163.com
@File    : test.py
@Software: PyCharm
"""
from tortoise import Tortoise

from FastApiProject.extension import return_json_response, response_err, err_log
from FastApiProject.orm.models import Users


# 授权用户
async def user_add(uid: int):
    try:
        conn = Tortoise.get_connection('default')
        user = await conn.execute_query_dict(
            'sql语句中使用%s占位',
            [uid]  # 这是语句中的占位信息，防注入
        )
        if not user:
            return response_err(message='库中用户不存在', status_code=404)
        await Users.create(**user[0])
        return return_json_response(data=user, message='用户授权成功', status_code=201)
    except Exception as e:
        # 日志记录
        err_log('user_add', e)
        if 'Duplicate' in str(e):
            return response_err(message='用户已授权', status_code=409)
        return response_err(e)


# 获取用户信息
async def user_get(uid: int):
    try:
        user = await Users.get_or_none(uid=uid).values()
        if not user:
            return response_err('达人不存在', status_code=404)
        return return_json_response(data=user, message='达人获取成功')
    except Exception as e:
        # 日志记录
        err_log('user_get', e)
        return response_err(e)


# 获取指定数量的用户信息
async def users_get(page: int = 1, limit: int = 10):
    try:
        start = (page - 1) * limit
        users = await Users.all().limit(limit).offset(start).values()
        if not users:
            return response_err('达人列表为空', status_code=404)
        return return_json_response(data=users, message='达人获取成功')
    except Exception as e:
        # 日志记录
        err_log('users_get', e)
        return response_err(e)


# 删除指定用户
async def user_del(uid: int):
    try:
        user = Users.filter(uid=uid)
        if not await user.values():
            return response_err(message='达人不存在', status_code=404)
        await user.delete()
        return return_json_response(message='用户%s已删除' % uid)
    except Exception as e:
        # 日志记录
        err_log('user_del', e)
        return response_err(e)