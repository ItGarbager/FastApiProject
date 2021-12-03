"""
@Time    : 2021/11/16 13:58
@Author  : Musuer
@Contact : linxuzhao2018@163.com
@File    : config.py
@Software: PyCharm
"""
# 生产模式为 1 线上 0 本地
PRODUCT = 0
# 启动模式
RUN_DEBUG: bool = False if PRODUCT else True

# 使用 uvion 项目启动配置
APP_RUN_CONFIG = {
    'host': '0.0.0.0',  # 启动 host
    'port': 81,  # 启动 port 端口
    'reload': RUN_DEBUG  # 是否已 reload 模式启动 默认与当前生产模式有关`
}

# swagger_ui 设置
SWAGGER_UI = {
    'title': 'FastApiProject',  # 标题
    'version': 'v1',
    # description 使用 markdown 语法
    'description': '''# 项目描述
......
    ''',  # 描述
    'docs_url': '/openapi/docs',  # openapi 文档地址 默认为 docs 此处修改为 /openapi/docs
    'openapi_url': '/openapi/openapi.json',  # 文档关联请求数据接口
    'redoc_url': '/openapi/redoc',  # redoc 文档
    # 'terms_of_service': 'http://example.com/terms/',
    # 'contact': {
    #     "name": "Deadpoolio the Amazing",
    #     "url": "http://x-force.example.com/contact/",
    #     "email": "dp@x-force.example.com",
    # },
    'license_info': {
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    # 接口描述
    'openapi_tags': [
        {
            "name": "test",
            "description": "openapi docs 中该接口的描述",
            # "externalDocs": { # 额外三方 url
            #     "description": "Items external docs",
            #     "url": "https://fastapi.tiangolo.com/",
            # },
        },

    ]
}

# jwt 密钥
SECRET_KEY = "xxxxxxxxxxxxxx"
# 加密方式
ALGORITHM = "HS256"

# 数据库地址 用户名:密码@主机:端口/数据库名
DATABASE_URLS = {
    'default': {
        'user': '这里是用户名',
        'password': '这里是用户密码',
        'host': (PRODUCT == 1) and '127.0.0.1' or 'x.x.x.x',  # 此处 host 自行设计若服务与mysql同属一个服务器可以采取
        'port': 3306,
        'database': '选择的数据库',
        'charset': 'utf8mb4',
    },
    'app_1_db': {
        'user': 'root',
        'password': 'xxxx',
        'host': '127.0.0.1',
        'port': 3306,
        'database': 'cps',
        'charset': 'utf8mb4',
    }
}

# redis 链接
REDIS_URL = "redis://127.0.0.1:6379/1"

# tortoise-orm 配置可以获取上方
TORTOISE_ORM = {
    'connections': {
        # # Dict format for connection
        # 'default': {
        #     'engine': 'tortoise.backends.mysql',
        #     'credentials': DATABASE_URLS.get('default')
        # },
        'app_1': {
            'engine': 'tortoise.backends.mysql',
            'credentials': DATABASE_URLS.get('app_1_db')
        },
    },
    'apps': {
        'models': {
            # 'models': ['aerich.models', 'app_1.orm.models'],
            'models': ['aerich.models', 'FastApiProject.orm.models'],
            # If no default_connection specified, defaults to 'default'
            'default_connection': 'app_1',  # connections中的配置默认
        }
    }
}

# 时区
TIME_ZONE = 'Asia/Shanghai'  # 数据库返回接口时使用
