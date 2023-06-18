import os

from dotenv import load_dotenv
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, AudioMessage, TextSendMessage
from ai.chatgpt import *
from config.configs import *

load_dotenv()

app = Flask(__name__)
environment = Environment[os.getenv("APP_ENVIRONMENT", Environment.VERCEL.value)]
if environment == Environment.DEVELOPMENT:
    app.config.from_object(DevelopmentConfig)
elif environment == Environment.PRODUCTION:
    app.config.from_object(ProductionConfig)
elif environment == Environment.VERCEL:
    app.config.from_object(ProductionForVercelConfig)

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

chatgpt = ChatGPT()

# region User related

user_prompt_key = "prompt"

user_dict = {}

# endregion


@app.route("/")
def home():
    return "OK"


@app.route("/webhook", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


@line_handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    user_id = event.source.user_id
    if not (user_exists(user_id)):
        init_user(user_id)
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=chat(user_id, event.message.text))
    )


@line_handler.add(MessageEvent, message=AudioMessage)
def handle_audio_message(event):
    user_id = event.source.user_id
    if not (user_exists(user_id)):
        init_user(user_id)
    # Read voice message for whisper api input
    message_id = event.message.id
    user_audio_path = os.path.join(
        app.config.get("AUDIO_TEMP_PATH"), f"{message_id}.m4a"
    )
    with open(user_audio_path, "wb") as f:
        f.write(line_bot_api.get_message_content(message_id).content)
    whispered_text = chatgpt.whisper(user_audio_path)
    if os.path.exists(user_audio_path):
        os.remove(user_audio_path)
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=chat(user_id, whispered_text))
    )


def user_exists(user_id):
    return user_id in user_dict


def init_user(user_id):
    user_dict[user_id] = {user_prompt_key: Prompt()}


def chat(user_id, user_input):
    user_prompt = user_dict[user_id][user_prompt_key]
    user_prompt.write(Role.USER.value, user_input)
    response_text = chatgpt.chat(user_prompt.messages)
    user_prompt.write(Role.ASSISTANT.value, response_text)
    return response_text


if __name__ == "__main__":
    app.run()
