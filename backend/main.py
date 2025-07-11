from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

INIT_PROMPT = (
"Jesteś tłumaczem. Otrzymujesz JSON: {'word':'xyz', 'native':'pl', 'foreign':'en'} (kody ISO). Przetłumacz słowo z języka 'native' na 'foreign'. Zwróć odpowiedź w języku 'native' w formacie JSON:"
  "{meaning: 'krótkie, proste wyjaśnienie słowa',"
  "type: 'rzeczownik/czasownik/przymiotnik',"
  "translation: 'tłumaczenie na foreign',"
  "synonyms: ['synonim1', 'synonim2', 'synonim3']}"
"Odpowiadaj tylko tym JSON, bez dodatkowego tekstu."
)

@app.get("/word/{word}")
async def read_word(word: str):
    final_prompt = (
    f"{INIT_PROMPT}\n"
    f"{{'word': '{word}', 'native': 'pl', 'foreign': 'es'}}")

    print(final_prompt)
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            url="http://ollama:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": final_prompt
            }
        )

        result = ""
        for line in response.text.splitlines():
            if line.strip():
                obj = json.loads(line)
                result += obj.get("response", "")
                if obj.get("done"):
                    break
        response_json = json.loads(result)


    return {
        "message": "success",
        "response": response_json,
    }
