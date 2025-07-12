from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

INIT_PROMPT = (
"You are a translator/dictionary. You'll recieve JSON: {'word':'xyz', 'native':'pl', 'foreign':'en'} (ISO codes). "
"Translate the word from the 'native' language to the 'foreign' language. Return the respnse in the 'native' language in the following JSON format:"
  "{meaning: 'short and simple explanation of the word',"
  "type: 'noun/verb/adjective',"
  "translation: 'translation into foreign',"
  "examples: 'three short sentences using this word in the foreign language',"
  "synonyms: ['synonym1', 'synonym2', 'synonym3']}"
"Your response should be only this JSON, nothing else."
)

@app.get("/word/{word}")
async def read_word(word: str):
    final_prompt = (
    f"{INIT_PROMPT}\n"
    f"{{'word': '{word}', 'native': 'en', 'foreign': 'es'}}")

    print(final_prompt)

    async with httpx.AsyncClient(timeout=120.0) as client:
        #  to zajmuje długo, więc zanim sie wykona to api call do prostego dictionary api

        print("test")

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

        print("res: " + result)
        print(response_json)

    return JSONResponse(content=response_json)
