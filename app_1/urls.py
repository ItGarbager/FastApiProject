"""
@Time    : 2021/11/16 14:48
@Author  : Musuer
@Contact : linxuzhao2018@163.com
@File    : urls.py
@Software: PyCharm
"""
from fastapi import APIRouter

from app_1.views import test

app1_router = APIRouter()

'''
路由注册
app1_router.add_api_route(path:str, func:callable[, tags:list, methods:list])
@path str 路由
@func callable 视图函数
@tags list 路由标签，openapi/dosc 上会按照 tags 进行分组
@methods list Http 请求方法 默认 ['GET', 'POST']
'''

# user
app1_router.add_api_route('/user/{uid}', test.user_get, tags=['v1-user'], description='用户获取接口，需要提供 uid',
                          methods=['GET'])
app1_router.add_api_route('/user/{uid}', test.user_add, tags=['v1-user'], description='用户授权接口，需要提供 uid',
                          methods=['POST'])
app1_router.add_api_route('/user/{uid}', test.user_del, tags=['v1-user'], description='用户删除接口，需要提供 uid',
                          methods=['DELETE'])
app1_router.add_api_route('/user', test.users_get, tags=['v1-user'], description='多用户获取接口', methods=['GET'])

