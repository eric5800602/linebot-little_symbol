import tempfile,os
import random

from linebot import LineBotApi, WebhookParser
from linebot.models import *
from dotenv import load_dotenv
from imgurpython import ImgurClient
from PIL import Image

load_dotenv()
client_id = os.getenv("client_id", None)
client_secret = os.getenv("client_secret", None)
access_token = os.getenv("access_token",None)
refresh_token = os.getenv("refresh_token",None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token,text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"
def send_button_template(reply_token,buttons_template):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, buttons_template)
    return "OK"
def send_yes_no_button(id,template):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.push_message(id, template)
    return "OK"
def send_image_url(reply_token, target):
    line_bot_api = LineBotApi(channel_access_token)
    if(target == ''):
        print('There is nothing funny.')
        text = 'There is nothing funny.'
        line_bot_api.reply_message(reply_token, TextSendMessage(text=text))
    else:
        line_bot_api.reply_message(reply_token,ImageSendMessage(original_content_url=target, preview_image_url=target))
    
    return "OK"
def send_img(id, target):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.push_message(id,ImageSendMessage(original_content_url=target, preview_image_url=target))
    return "OK"

def push_msg_img(id, target, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.push_message(id, TextSendMessage(text))
    line_bot_api.push_message(id,ImageSendMessage(original_content_url=target, preview_image_url=target))
    return "OK"
def push_msg(id,text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.push_message(id,TextSendMessage(text))
    return "ok"
def upload_img(event):
    line_bot_api = LineBotApi(channel_access_token)
    static_tmp_path = os.path.join(os.path.dirname(__file__), 'static')
    ext = 'png'
    message_content = line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name
        

    dist_path = tempfile_path + '.' + ext
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)
    im = Image.open(dist_path)
    width, height = im.size
    client = ImgurClient(client_id, client_secret, access_token, refresh_token)
    path = os.path.join('static', dist_name)
    upimg = client.upload_from_path(path, config=None, anon=False)
    os.remove(path)
    print(upimg['link'])
    push_msg(event.source.user_id,"上傳成功")
    return upimg ,width,height 