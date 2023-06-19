# gpt-ai-hater

使用 Flask、OpenAI whisper API、GPT3.5 API 來開發**讓你不再依賴生成式 AI** 的 Line 機器人。

## 使用案例

![Image](data/img/demo.png)

#### 使用指令

| 指令 | 別名    | 說明             |
| ---- | ------- | ---------------- |
| 忘記 | /forget | 忘記當前對話內容 |

## 如何開始

#### 環境變數

| 名稱                          | 預設值                                                                                     | 說明                                                                                                                          |
| ----------------------------- | ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| APP_ENVIRONMENT               | VERCEL                                                                                     | 執行環境                                                                                                                      |
| APP_MAX_PROMPT_MESSAGES       | 12                                                                                         | 對話堆疊上限                                                                                                                  |
| APP_INIT_PROMPT               | 請你在回覆的時候，帶有非常不屑且辱罵的語氣並表現得不是很想處理這件事，盡量以繁體中文回答。 | 起始意圖（亦即你希望機器人怎麼回應你，可以調得更狠毒？）                                                                      |
| LINE_CHANNEL_ACCESS_TOKEN     | null                                                                                       | LINE 的 channel access token                                                                                                  |
| LINE_CHANNEL_SECRET           | null                                                                                       | LINE 的 channel secret                                                                                                        |
| OPENAI_API_KEY                | null                                                                                       | OpenAI 的 API key                                                                                                             |
| OPENAI_COMPLETION_MODEL       | gpt-3.5-turbo                                                                              | 詳見 [model](https://platform.openai.com/docs/api-reference/completions/create#completions/create-model) 參數說明             |
| OPENAI_COMPLETION_TEMPERATURE | 0.5                                                                                        | 詳見 [temperature](https://platform.openai.com/docs/api-reference/completions/create#completions/create-temperature) 參數說明 |

#### 部署至 Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fcdcd72%2Fgpt-ai-hater&env=LINE_CHANNEL_ACCESS_TOKEN,LINE_CHANNEL_SECRET,OPENAI_API_KEY)

## 如何偵錯

#### 調整 api/index.py 部分程式碼以可以在本機測試

```python
# from api.ai.chatgpt import *
# from api.config.configs import *
from ai.chatgpt import *
from config.configs import *
```

#### 依據 .env.example 格式並在根目錄新增 .env

    APP_ENVIRONMENT=DEVELOPMENT
    LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
    LINE_CHANNEL_SECRET=your_line_channel_secret
    OPENAI_API_KEY=your_openai_api_key

#### 安裝相依套件

    pip install -r requirements.txt

#### 執行 Flask

    py api/index.py

## 參考

- Line SDK : [https://github.com/line/line-bot-sdk-python](https://github.com/line/line-bot-sdk-python)
- OpenAI API Document : [https://platform.openai.com/docs/introduction](https://platform.openai.com/docs/introduction)
