"""
@Time    : 2021/11/16 14:07
@Author  : Musuer
@Contact : linxuzhao2018@163.com
@File    : urls.py
@Software: PyCharm
"""
from app_1.urls import app1_router


def register_routers(app) -> None:
    # 注册主页
    app.include_router(app1_router, prefix='/test')
