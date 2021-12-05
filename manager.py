import uvicorn
from FastApiProject import CreateApp
from FastApiProject.config import APP_RUN_CONFIG

app = CreateApp()

if __name__ == "__main__":
    # 启动服务，因为我们这个文件叫做 manager.py，所以需要启动 manager.py 里面的 app
    # 第一个参数 "main:app" 就表示这个含义，然后是 host 和 port 表示监听的 ip 和端口
    uvicorn.run("manager:app", **APP_RUN_CONFIG)
