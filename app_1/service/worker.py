"""
@Time    : 2021/11/18 14:53
@Author  : Musuer
@Contact : linxuzhao2018@163.com
@File    : worker.py
@Software: PyCharm
"""
from . import celery_app
from . import item as item_service


@celery_app.task(acks_late=True)
def get_item_price(price: int) -> float:
    item = item_service.get_item(price)
    if not item:
        return -1.0
    return item['price']
