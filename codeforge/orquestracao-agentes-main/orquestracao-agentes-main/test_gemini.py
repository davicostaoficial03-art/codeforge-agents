import logging
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

logging.getLogger("google_genai.models").setLevel(logging.ERROR)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="Explique em uma frase o que é um agente de IA."
)

print(response.text)