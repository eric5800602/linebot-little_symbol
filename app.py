import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["user", "fsm", "what","sendmeme","create_img","choose_template","confirm","add_template","get_image","get_image2","decide_format"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "fsm",
            "conditions": "is_going_to_fsm",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "what",
            "conditions": "is_going_to_what",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "sendmeme",
            "conditions": "is_going_to_sendmeme",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "create_img",
            "conditions": "is_going_to_create_img",
        },
        {
            "trigger": "advance",
            "source": "create_img",
            "dest": "user",
            "conditions": "is_going_to_initial",
        },
        {
            "trigger": "advance",
            "source": "create_img",
            "dest": "choose_template",
            "conditions": "is_going_to_choose_template",
        },
        {
            "trigger": "advance",
            "source": "choose_template",
            "dest": "create_img",
            "conditions": "is_going_to_cancel",
        },
        {"trigger": "advance","source": "user","dest": "add_template","conditions": "is_going_to_add_template",},
        {"trigger": "advance","source": "add_template","dest": "get_image","conditions": "is_going_to_get_image",},
        {"trigger": "advance","source": "get_image","dest": "get_image2","conditions": "is_going_to_get_image2",},
        {"trigger": "advance","source": "get_image2","dest": "decide_format","conditions": "is_going_to_decide_format",},
        {"trigger": "advance","source": "decide_format","dest": "user","conditions": "is_going_to_goback_from_decide_format",},
        {"trigger": "advance","source": "decide_format","dest": "add_template","conditions": "is_going_to_add_template_again",},
        {"trigger": "advance","source": "choose_template","dest": "confirm","conditions": "is_going_to_confirm",},
        {"trigger": "advance","source": "confirm","dest": "user","conditions": "is_going_to_return",},
        {"trigger": "advance","source": "confirm","dest": "choose_template","conditions": "is_going_to_again",},
        {"trigger": "go_back", "source": ["fsm", "what","sendmeme","create_img","choose_template"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body:"+ body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)
    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        print("\nFSM STATE: "+machine.state)
        print("REQUEST BODY: \n"+body)
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "Not Entering any State")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.jepg", prog="dot", format="jepg")
    return send_file("fsm.jepg", mimetype="image/jepg")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)
