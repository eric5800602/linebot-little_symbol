import os
import random

from linebot import LineBotApi, WebhookParser
from linebot.models import *
from bs4 import BeautifulSoup
import requests

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"


def send_image_url(reply_token, img_url):
    line_bot_api = LineBotApi(channel_access_token)
    head_Html = 'https://memes.tw/image/'+str(random.randint(1,5000))
    res = requests.get(head_Html, timeout=30)
    soup = BeautifulSoup(res.text,'lxml')
    line_bot_api.reply_message(reply_token,ImageSendMessage(original_content_url='https://memes.tw'+str(soup.img['src']), preview_image_url='https://memes.tw'+str(soup.img['src'])))
    
    return "OK"
"""
def send_button_message(id, text, buttons):
    pass
"""
