from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles

from .config import SECRET_KEY, ALGORITHM, RUN_DEBUG, SWAGGER_UI
from .middleware import register_middleware
# from .model.models import register_mysql # 封装好的数据库链接池
from .orm import register_tortoise_app
from .register_redis import register_redis
from .urls import register_routers


def CreateApp():
    app = FastAPI(
        debug=RUN_DEBUG,
        **SWAGGER_UI  # 加载 SWAGGER——UI
    )
    # 注册 tortoise_orm
    register_tortoise_app(app)

    # 注册中间件
    register_middleware(app)

    # 注册路由
    register_routers(app)

    # 注册 redis
    register_redis(app)

    # # 注册 mysql
    # register_mysql(app_1)

    # 批量添加 openapi_id
    use_route_names_as_operation_ids(app)

    # 注册静态路由 静态文件夹为 ./app_1/static
    app.mount("/", StaticFiles(directory="./static"), name="static")

    return app


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name  # in this case, 'read_items'
