# flake8: noqa: E501
from openai import AsyncOpenAI
from app.config import settings


class AIService:
    """Сервис, определяющий тональность текста с помощью AI"""

    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY

    async def analyze(self, comment: str):
        client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )
        prompt = f"Определи тональность текста. Ответь одним словом: положительная, отрицательная или нейтральная. Текст: {comment}."

        response = await client.chat.completions.create(
            model="openai/gpt-oss-120b:free",
            messages=[{"role": "user", "content": prompt}],
        )

        response = response.choices[0].message.content.strip().lower()
        return response
