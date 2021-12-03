"""
@Time    : 2021/11/18 15:43
@Author  : Musuer
@Contact : linxuzhao2018@163.com
@File    : redis.py
@Software: PyCharm
"""

from aioredis import create_redis_pool
from .config import REDIS_URL


def register_redis(app) -> None:
    """
    把redis挂载到app对象上面
    :param app:
    :return:
    """

    @app.on_event('startup')
    async def startup_event():
        """
        获取链接
        :return:
        """
        app.redis = await create_redis_pool(REDIS_URL)

    @app.on_event('shutdown')
    async def shutdown_event():
        """
        关闭
        :return:
        """
        app.redis.close()
        await app.redis.wait_closed()
