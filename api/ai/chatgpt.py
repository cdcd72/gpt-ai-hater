import os
import openai

from dotenv import load_dotenv
from enum import Enum

load_dotenv()

prompt_max_messages = int(os.getenv("APP_MAX_PROMPT_MESSAGES", "12")) + 1
system_prompt = os.getenv(
    "APP_INIT_PROMPT", "請你在回覆的時候，帶有非常不屑且辱罵的語氣並表現得不是很想處理這件事，盡量以繁體中文回答。"
)

openai.api_key = os.getenv("OPENAI_API_KEY")
openai_completion_model = os.getenv("OPENAI_COMPLETION_MODEL", "gpt-3.5-turbo")
openai_completion_temperature = float(os.getenv("OPENAI_COMPLETION_TEMPERATURE", "0.5"))


class ChatGPT:
    def __init__(self):
        self.model = openai_completion_model
        self.temperature = openai_completion_temperature

    def whisper(self, audio_path):
        audio_file = open(audio_path, "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript["text"]

    def chat(self, messages):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
        )
        return response["choices"][0]["message"]["content"]


class Role(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class Prompt:
    def __init__(self):
        self.messages = [
            {
                "role": Role.SYSTEM.value,
                "content": system_prompt,
            }
        ]

    def write(self, role, content):
        if len(self.messages) >= prompt_max_messages:
            self.messages[1:2] = []
        self.messages.append({"role": role, "content": self.__add_mark(content)})

    def __add_mark(self, message):
        if not message:
            return message
        marks = ["？", "。", "！"]
        if not message[-1] in marks:
            return f"{message}。"
        return message
