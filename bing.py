import json
from config import config_instance


import asyncio
from EdgeGPT import Chatbot, ConversationStyle

cookies = json.loads(cookies_str)


class Bing:
    def __init__(self):
        self.bot = Chatbot(cookies=cookies)
        self._result = None

    async def close(self):
        return await self.bot.close()

    async def get(self, question: str):
        return (
            (
                await self.bot.ask(
                    prompt=question,
                    conversation_style=ConversationStyle.balanced
                )
            )["item"]["messages"][1]["adaptiveCards"][0]["body"][0]["text"],
        )
