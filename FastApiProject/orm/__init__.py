from tortoise.contrib.fastapi import register_tortoise

from ..config import TORTOISE_ORM


def register_tortoise_app(app):
    register_tortoise(  # 这里是启动app的，之后会考虑和使用uvicorn启动的性能差别
        app,
        config=TORTOISE_ORM,
        # db_url="sqlite://:memory:",  # 数据库信息
        # modules={'models': ['']},  # models列表
        generate_schemas=False,  # 如果数据库为空，则自动生成对应表单,生产环境不要开
        add_exception_handlers=False,  # 生产环境不要开，会泄露调试信息
    )
