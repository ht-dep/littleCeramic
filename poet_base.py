import os
import json
import random
from poet_db import Poet, Word, db_add

poet = '''
{}
{}
{}
       '''


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


###############
# 语录文件列表
###############
def get_word_list():
    face_path = os.path.join(get_current_dir(), "word")
    if os.path.exists(face_path):
        faces_list = os.listdir(face_path)
        return [os.path.join(face_path, i) for i in faces_list if "json" in i]
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
def get_content(file_path):
    if os.path.exists(file_path):
        with open(file_path, encoding='utf8') as f:
            result = json.loads(f.read())
        return result


#######################
# 主函数
#######################
def run():
    # GET诗词文件列表
    poet_file_list = get_poet_list()
    print(poet_file_list)
    # GET诗词文件内容  todo 遍历文件--得到内容列表
    for poet_file in poet_file_list:
        # poet_file = poet_file_list[0]
        poet_content_list = get_content(poet_file)
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


#######################
# 主函数
#######################
def run_word():
    # GET语录列表
    word_file_list = get_word_list()
    print(word_file_list)
    # GET诗词文件内容  todo 遍历文件--得到内容列表
    for word_file in word_file_list:
        word_content_list = get_content(word_file)
        print(word_content_list)
        # GET单首诗词内容 todo 遍历内容列表--得到一首诗词
        for word_content in word_content_list["words"]:
            author = word_content_list["author"]
            content = word_content
            print("作者：{},类型：{}".format(author, type(author)))
            print("内容：{},类型：{}".format(content, type(content)))
            # SAVE到数据库
            obj = Word.create_obj(author, content)
            if obj:
                print("诗词：{}，成功存储".format(obj.content))
            else:
                print("失败")


def count():
    obj = Poet.count_obj()
    print("目前已存储诗词：{}".format(obj))



def word_count():
    obj = Word.count_obj()
    print("目前已存储诗词：{}".format(obj))


def query_page():
    obj = Poet.get_page_obj()

    print("题目：{}".format(obj.title))
    print("作者：{}".format(obj.author))
    return {
        "题目": obj.title,
        "作者": obj.author,
        "内容": obj.content}


def query_luck():
    obj = Poet.get_luck_obj()[0]
    # print("题目：{}".format(obj.title))
    # print("作者：{}".format(obj.author))
    # for i in obj.content.split('。'):
    #     print(i)
    return poet.format(obj.title, obj.author, obj.content.replace("。", "。\n"))


def query_luck_word():
    obj = Word.get_luck_obj()[0]
    # print("题目：{}".format(obj.title))
    # print("作者：{}".format(obj.author))
    # for i in obj.content.split('。'):
    #     print(i)
    text = obj.content.replace("。", "。\n")
    # text = text.replace("\r", "\n")
    text = text.replace("-", "")
    text = text.replace("/", "，")
    return text


def test_query():
    import time
    while 1:
        cc = query_luck_word()
        print()
        print(cc)

        time.sleep(1)


if __name__ == "__main__":
    # run()
    # count()
    run_word()
    # test_query()
