'''
1、用户查询、创建、修改、删除、激活
2、工资查询、创建、修改、删除
'''
import os
import json
import datetime
from peewee import *
from playhouse.pool import PooledSqliteExtDatabase

# db = SqliteDatabase("poet.db")
db = PooledSqliteExtDatabase(
    "poet.db",
    max_connections=8,
    stale_timeout=300
)


def db_add(act):
    def func():
        db.connect()
        act()
        db.close()

    return func


class BaseModel(Model):
    class Meta:
        database = db


class Poet(BaseModel):
    '''
    1、用户创建、用户查询、用户修改、用户删除
    2、请求绑定
    '''

    title = CharField(max_length=500)  # 题目
    author = CharField(default="", max_length=500, )  # 作者
    content = CharField(default="", max_length=500, )  # 内容

    created_date = DateTimeField(default=datetime.datetime.now)

    @classmethod
    def count_obj(cls, title="", author=""):
        ''''
        1、查询条件   查询所有或根据题目或者根据作者查询
        返回的是列表
        '''
        try:
            objs = Poet.select().count()
            return objs
        except Exception as e:
            print("查询error：{}".format(e))
            return None

    @classmethod
    def get_luck_obj(cls, title="", author=""):
        ''''
        1、查询条件   查询所有或根据题目或者根据作者查询
        返回的是列表
        '''
        try:
            objs = Poet.select().order_by(fn.Random()).limit(1)
            return objs
        except Exception as e:
            print("查询error：{}".format(e))
            return None

    @classmethod
    def get_page_obj(cls, title="", author=""):
        ''''
        分页查询，2是第几页，10是每页多少个
        返回的是列表
        '''
        try:
            objs = Poet.select().order_by(Poet.id).paginate(2, 10)
            return objs
        except Exception as e:
            print("查询error：{}".format(e))
            return None

    @classmethod
    def query_obj(cls, title="", author=""):
        ''''
        1、查询条件   查询所有或根据题目或者根据作者查询
        返回的是列表
        '''
        try:
            objs = Poet.select().order_by(Poet.created_date.desc())
            return objs
        except Exception as e:
            print("查询error：{}".format(e))
            return None

    @classmethod
    def create_obj(cls, title="", author="", content=""):  # 创建用户---微信端
        try:
            obj, created = Poet.get_or_create(title=title, author=author)
            print(obj)
            obj.content = content
            obj.save()
            print("新用户创建成功：{}".format(obj.title))
            return obj
        except Exception as e:
            print("创建error：{}".format(e))
            return None

    @classmethod
    def delete_obj(cls, id):  # 删除用户---微信端
        try:
            # 查询user是否存在，参数:员工编号emid
            obj = Poet.select().where(Poet.id == id).get()
            obj.delete_instance()
            return True
        except Exception as e:
            print("删除error：{}".format(e))
            return None


class Word(BaseModel):
    '''
    1、用户创建、用户查询、用户修改、用户删除
    2、请求绑定
    '''
    author = CharField(default="", max_length=500, )  # 作者
    content = CharField(default="", max_length=500, )  # 内容

    created_date = DateTimeField(default=datetime.datetime.now)


    @classmethod
    def count_obj(cls, title="", author=""):
        ''''
        1、查询条件   查询所有或根据题目或者根据作者查询
        返回的是列表
        '''
        try:
            objs = Word.select().count()
            return objs
        except Exception as e:
            print("查询error：{}".format(e))
            return None

    @db_add
    @classmethod
    def get_luck_obj(cls, title="", author=""):
        ''''
        1、查询条件   查询所有或根据题目或者根据作者查询
        返回的是列表
        '''
        try:
            objs = Word.select().order_by(fn.Random()).limit(1)
            return objs
        except Exception as e:
            print("查询error：{}".format(e))
            return None

    @classmethod
    def get_page_obj(cls, title="", author=""):
        ''''
        分页查询，2是第几页，10是每页多少个
        返回的是列表
        '''
        try:
            objs = Word.select().order_by(Word.id).paginate(2, 10)
            return objs
        except Exception as e:
            print("查询error：{}".format(e))
            return None

    @classmethod
    def query_obj(cls, title="", author=""):
        ''''
        1、查询条件   查询所有或根据题目或者根据作者查询
        返回的是列表
        '''
        try:
            objs = Word.select().order_by(Word.created_date.desc())
            return objs
        except Exception as e:
            print("查询error：{}".format(e))
            return None

    @classmethod
    def create_obj(cls, author="", content=""):  # 创建用户---微信端
        try:
            obj, created = Word.get_or_create(author=author, content=content)
            print(obj)
            obj.content = content
            obj.save()
            print("新用户创建成功：{}".format(obj.content))
            return obj
        except Exception as e:
            print("创建error：{}".format(e))
            return None

    @classmethod
    def delete_obj(cls, id):  # 删除用户---微信端
        try:
            # 查询user是否存在，参数:员工编号emid
            obj = Word.select().where(Word.id == id).get()
            obj.delete_instance()
            return True
        except Exception as e:
            print("删除error：{}".format(e))
            return None
