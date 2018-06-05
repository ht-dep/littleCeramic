import random
import json
import requests
import time
from bs4 import BeautifulSoup as bs
# from word_base import headers

juzi_url = "http://www.juzimi.com/"
MARK_URL = {
    # "张小娴": "{}{}".format(juzi_url, "writer/601"),
    # "莎士比亚": "{}{}".format(juzi_url, "writer/莎士比亚"),
    # "三毛": "{}{}".format(juzi_url, "writer/三毛"),
    # "南派三叔": "{}{}".format(juzi_url, "writer/南派三叔"),
    # "顾漫": "{}{}".format(juzi_url, "writer/顾漫"),
    # "张爱玲": "{}{}".format(juzi_url, "writer/张爱玲"),
    # "顾城": "{}{}".format(juzi_url, "writer/顾城"),
    # "村上春树": "{}{}".format(juzi_url, "writer/村上春树"),
    # "席慕容": "{}{}".format(juzi_url, "writer/席慕容"),
    # "尼采": "{}{}".format(juzi_url, "writer/尼采"),
    # "纳兰容若": "{}{}".format(juzi_url, "writer/纳兰容若"),
    # "仓央嘉措": "{}{}".format(juzi_url, "writer/仓央嘉措"),
    # "树下野狐": "{}{}".format(juzi_url, "writer/树下野狐"),
    # "林夕": "{}{}".format(juzi_url, "writer/林夕"),
    # "几米": "{}{}".format(juzi_url, "writer/几米"),
    # "泰戈尔": "{}{}".format(juzi_url, "writer/泰戈尔"),
    # "孟子": "{}{}".format(juzi_url, "writer/孟子"),
    # "庄子": "{}{}".format(juzi_url, "writer/庄子"),
    # "老子": "{}{}".format(juzi_url, "writer/老子"),
    # "毛泽东": "{}{}".format(juzi_url, "writer/毛泽东"),
    # "希特勒": "{}{}".format(juzi_url, "writer/希特勒"),
    # "王小波": "{}{}".format(juzi_url, "writer/王小波"),
    # "龙应台": "{}{}".format(juzi_url, "writer/龙应台"),
    # "七堇年": "{}{}".format(juzi_url, "writer/七堇年"),
    # "林徽因": "{}{}".format(juzi_url, "writer/林徽因"),
    # "莫言": "{}{}".format(juzi_url, "writer/莫言"),
    # "三毛": "{}{}".format(juzi_url, "writer/三毛"),
    # "王尔德": "{}{}".format(juzi_url, "writer/王尔德"),
    # "河图": "{}{}".format(juzi_url, "writer/河图"),
    # "钱钟书": "{}{}".format(juzi_url, "writer/钱钟书"),
    # "月亮和六便士": "{}{}".format(juzi_url, "article/月亮和六便士"),
    # "撩妹": "{}{}".format(juzi_url, "album/1974568"),
    "纳兰": "{}{}".format(juzi_url, "article/25738"),
}

proxy_ip = ""


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").text


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


def getHtml(url):
    # ....
    print(url)
    retry_count = 5
    proxy_ip = get_proxy()
    print(proxy_ip)
    while retry_count > 0:
        try:
            req = requests.get(url, headers=random.choice(headers),
                               proxies={"http": "{}".format(proxy_ip)}, timeout=10)
            # 使用代理访问
            print("访问状态码：{}".format(req.status_code))
            return req
        except Exception:
            retry_count -= 1
    # 出错5次, 删除代理池中代理
    print("删除该代理ip")
    delete_proxy(proxy_ip)
    return None


def get_client(url):
    while 1:
        print("重新获取代理")
        client = getHtml(url)
        # print("结果：{}".format(client))
        if client:
            return client


####################
# SAVE语录本地
####################
def save_json(author, words):
    data = {
        "author": author,
        "words": words
    }
    file_path = '{}.json'.format(author)
    with open(file_path, mode="w", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False))
    return True


####################
# GET语录页数
####################
def get_num(author):
    print(author)
    url = MARK_URL[author]
    print(url)
    req = get_client(url)
    print(req)
    html = req.text
    soup = bs(html, "lxml")
    mark = soup.select_one(".block-inner .content .contentin .item-list .pager-last  a")
    pages = mark.text
    # pages = 5
    print("{}的语录共{}页".format(author, pages))
    return int(pages)


####################
# GET单页语录
####################
def get_content(author, page_num):
    if page_num < 2:
        url = MARK_URL[author]
    else:
        url = "{}?page={}".format(MARK_URL[author], page_num - 1)
    print("当前页面地址：{}".format(url))
    req = get_client(url)
    html = req.text
    soup = bs(html, "lxml")

    marks = soup.select(".block-inner .content .contentin .view-content .views-field-phpcode .xlistju")
    # marks = soup.select(".block-inner .content .contentin .view-content .views-field-phpcode a")
    # print(marks)
    # 获取语录 todo 便利循环
    words = [mark.text for mark in marks]
    # print(words)
    # for mark in marks:
    #     print(mark)
    # word = mark.text
    # print(word)
    # 组织结构
    # for word in words:
    #     print(word)
    return words


####################
# GET所有语录
####################
def get_all(author, num):
    page_words = []
    for page in range(1, num):
        print("第{}页".format(page))
        page_word = get_content(author, page)
        print("语录{}个,内容：{}".format(len(page_word), page_word))
        if not len(page_word):
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            print("死机")
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        page_words.extend(page_word)
        time.sleep(0.3)

    print("所有语录{}个,内容：{}".format(len(page_words), page_words))
    return page_words


####################
# GET作者的所有语录
####################
def get_author(author):
    # GET单作者的语录
    num = get_num(author)
    words = get_all(author, num)
    save_json(author, words)


####################
# RUN主逻辑
####################
def main():
    for author in MARK_URL.keys():
        # GET单作者的语录
        get_author(author)


if __name__ == "__main__":
    pass
    # get_content()
    main()
    # get_author("顾城")
