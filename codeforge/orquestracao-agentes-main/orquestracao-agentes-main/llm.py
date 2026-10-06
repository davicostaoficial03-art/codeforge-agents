import logging
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# A partir da versão 2.18 do google-genai, o SDK loga um aviso sempre que
# generate_content é chamado diretamente (ele "recomenda" usar Chat.send_message).
# Como não usamos function calling automático aqui, o aviso é apenas ruído no
# console — silenciamos só esse logger, sem alterar nenhum comportamento.
logging.getLogger("google_genai.models").setLevel(logging.ERROR)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash-lite"
)


def call_llm(system_prompt, user_prompt):
    response = client.models.generate_content(
        model=MODEL,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt
        )
    )
    return response.text