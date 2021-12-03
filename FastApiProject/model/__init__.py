import os
import warnings
from ..config import DATABASE_URLS
warnings.filterwarnings('ignore')


# 检查文件夹是否存在，不存在创建
def mkdir(path: str) -> None:
    if not os.path.isdir(path):
        os.makedirs(path)


# 检查文件是否存在shu
def isfile(file: str) -> bool:
    return os.path.isfile(file)


class SQLHelper(object):
    def __init__(self, POOL=None):

        if POOL:
            self.POOL = POOL
        else:
            self.POOL = DATABASE_URLS['websitedb']

    def open(self):
        conn = self.POOL.connection()
        cursor = conn.cursor()
        return conn, cursor

    def close(self, conn, cursor):
        conn.commit()
        cursor.close()
        conn.close()

    def fetch_one(self, sql, *args):
        conn, cursor = self.open()
        cursor.execute(sql, *args)
        obj = cursor.fetchone()
        self.close(conn, cursor)
        return obj

    def fetch_all(self, sql, *args):
        conn, cursor = self.open()
        cursor.execute(sql, *args)
        obj = cursor.fetchall()
        self.close(conn, cursor)
        return obj

    def commit(self, sql, *args):
        conn, cursor = self.open()
        cursor.execute(sql, *args)
        self.close(conn, cursor)
