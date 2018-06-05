# coding=utf8
import random
import itchatmp
from itchatmp.content import (
    TEXT, MUSIC, IMAGE, VOICE,
    VIDEO, THUMB, NEWS, CARD,
    SAFE)
from mp_base import get_response, text_list
from poet_base import query_luck, query_page, query_luck_word

# **************************************************

# 一小瓶陶瓷订阅号
itchatmp.update_config(itchatmp.WechatConfig(
    token='xxx',
    appId='xxx',
    appSecret='xxx'))


@itchatmp.msg_register(TEXT)
def text_reply(msg):
    if "1" in msg["Content"]:
        reply = random.choice(text_list)
    elif "2" in msg["Content"]:
        reply = query_luck()
    elif "3" in msg["Content"]:
        reply = query_luck_word()
    else:
        reply = get_response(msg['Content'])
    return reply


itchatmp.run(port=8899)
