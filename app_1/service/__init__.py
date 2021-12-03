"""
@Time    : 2021/11/18 14:53
@Author  : Musuer
@Contact : linxuzhao2018@163.com
@File    : __init__.py.py
@Software: PyCharm
"""
from celery import Celery


celery_app = Celery('celery_tester',
                    broker='redis://:helloword@localhost:6379/0',
                    backend='redis://:helloword@localhost:6379/1')

celery_app.conf.update(task_track_started=True)
