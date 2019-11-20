import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"


def send_image_url(reply_token, img_url):
    line_bot_api = LineBotApi(channel_access_token)
    client.replyMessage(reply_token, 
    {
        type: 'image',
        originalContentUrl: 'https://developers.line.biz/media/messaging-api/messages/image-full-04fbba55.png',
        previewImageUrl: 'https://developers.line.biz/media/messaging-api/messages/image-167efb33.png'
    }
    )
    return "OK"
"""
def send_button_message(id, text, buttons):
    pass
"""
