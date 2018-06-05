import asyncio
import json
import aiofiles
import os
import json
import random
from poet_db import Poet


# 当前目录
def get_current_dir():
    file_dir = os.path.dirname(os.path.abspath(__file__))
    # print("当前目录：",file_dir)
    return file_dir


###############
# 诗词文件列表
###############
def get_poet_list():
    face_path = os.path.join(get_current_dir(), "store")
    if os.path.exists(face_path):
        faces_list = os.listdir(face_path)
        return [os.path.join(face_path, i) for i in faces_list if "poet" in i]
    else:
        return


##############
#
##############
def get_cfg_path():
    current_path = get_current_dir()
    file_path = os.path.join(current_path, "config.json")
    return file_path


#############
# 读取诗词
############


async def get_content_async():
    with aiofiles.open('filename', mode='r') as f:
        contents = await json.loads(f.read())
    print(contents)
    return contents


def test_io():
    pass


async def test_io_async():
    pass


#######################
# 主函数
#######################
async def run():
    # GET诗词文件列表
    poet_file_list = get_poet_list()
    print(poet_file_list)
    # GET诗词文件内容  todo 遍历文件--得到内容列表
    for poet_file in poet_file_list:
        # poet_file = poet_file_list[0]
        poet_content_list = await get_content_async(poet_file)
        print(poet_content_list)
        # GET单首诗词内容 todo 遍历内容列表--得到一首诗词
        for poet_content in poet_content_list:
            # poet_content = poet_content_list[0]
            # print(poet_content)
            title = poet_content["title"].strip()
            author = poet_content["author"].strip()
            content = "".join(poet_content["paragraphs"])
            print("题目：{},类型：{}".format(title, type(title)))
            print("作者：{},类型：{}".format(author, type(author)))
            print("内容：{},类型：{}".format(content, type(content)))
            # SAVE到数据库
            obj = Poet.create_obj(title, author, content)
            if obj:
                print("诗词：{}，成功存储".format(obj.title))
            else:
                print("失败")


def count():
    obj = Poet.query_obj()
    print("目前已存储诗词：{}".format(len(obj)))


def query():
    objs = Poet.query_obj()
    obj = random.choice(objs)
    print("题目：{}".format(obj.title))
    print("作者：{}".format(obj.author))

    for i in obj.content.split('。'):
        print(i)


if __name__ == "__main__":
    run()
    count()
