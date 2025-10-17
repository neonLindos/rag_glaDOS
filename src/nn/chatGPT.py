
import os

from openai import AsyncOpenAI

class ChatGPT():

    def __init__(self):
        openai_api_key = os.getenv("OPENAI_API_KEY")  # Correct key name
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        self.client = AsyncOpenAI(api_key=openai_api_key)



    async def gen_text(self):
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": "Hello world"}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}" 