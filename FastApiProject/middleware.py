"""
@Time    : 2021/11/16 14:05
@Author  : Musuer
@Contact : linxuzhao2018@163.com
@File    : middleware.py
@Software: PyCharm
"""

import jwt
from fastapi import Cookie
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError

from .extension import response_err
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from FastApiProject import RUN_DEBUG
from .config import SECRET_KEY, ALGORITHM
from tortoise import Tortoise


def register_middleware(app) -> None:
    """
    中间件注册
    :param app:
    :return:
    """
    # # 测试中间件
    # @app_1.middleware("http")
    # async def add_process_time_header(request: Request, call_next):
    #     start_time = time.time()
    #     response = await call_next(request)
    #     process_time = time.time() - start_time
    #     response.headers["X-Process-Time"] = str(process_time)
    #     return response

    # 若线上添加
    if not RUN_DEBUG:
        # 跨域设置
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # allowed host 设置
        app.add_middleware(
            TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1"]
        )

    # 添加自定义 jwt 验证 #不用可注释掉
    @app.middleware("http")
    async def jwt_authentication(
            request: Request,
            call_next,
            csrftoken: str = Cookie(None, title='csrftoken', description='jwt cstftoken 验证'),
    ):
        """
        除了开放API、登录、注册以外，其他均需要认证
        :param request:
        :param call_next: 执行获取响应
        :param csrftoken:获取 cookie 中的 csrftoken
        :return:
        """
        response = await call_next(request)

        if RUN_DEBUG:  # 线下就忽视验证
            return response

        start_url = request.url.path.lower()

        # 允许通过验证的 url
        allow_urls = (
            '/openapi', '/upload/', '/test'
        )
        for url in allow_urls:
            if start_url.startswith(url):
                return response

        if csrftoken:
            try:
                payload = jwt.decode(csrftoken, SECRET_KEY, algorithms=[ALGORITHM])
            except:
                payload = None
        else:
            payload = None
        if payload is None:
            return response_err(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Could not validate credentials",
            )
        else:
            Id = payload.get('sub')
            if not Id:
                return response_err(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    message="Could not validate credentials",
                )
            conn = Tortoise.get_connection('default')
            http_path_dict = await conn.execute_query_dict(
                'select http_path from ssodb.tb_permissions where modular_id in (select modular_id from ssodb.tb_role_permissions where role_id = (select role_id from ssodb.tb_role_users where uuid = (select uuid from ssodb.tb_users where id=%s)))',
                Id)

            http_path_list = [i.get('http_path') for i in http_path_dict]
            url_path = str(request.url).split(str(request.base_url))[1].split('?')[0]
            if url_path not in http_path_list:
                return response_err(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    message="Permisson Not Found",
                )
        return response

    # # 为以后反爬做相应措施
    # @app_1.middleware('http')
    # async def path_enc(
    #         request: Request,
    #         call_next,
    # ):
    #     response = await call_next(request)
    #     print(request.path_params)
    #     for k, v in request.path_params.items():
    #         request.path_params[k] = enc_b64(v)
    #     print(request.path_params)
    #
    #     return response
