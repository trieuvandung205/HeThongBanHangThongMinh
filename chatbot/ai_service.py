from django.conf import settings
from groq import Groq

from .formatter import PromptFormatter
from .prompts import SYSTEM_PROMPT


client = Groq(
    api_key=settings.GROQ_API_KEY
)


def ask_ai(state):
    """
    Gửi prompt đến Groq và trả về câu trả lời.
    """

    prompt = PromptFormatter.build(state)

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],

        temperature=0.4,
        max_tokens=700,

    )

    return response.choices[0].message.content