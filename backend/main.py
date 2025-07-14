from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import json
import re 
""" PORTS:
    - 5173 - FRONTEND
    - 5174 - BACKEND
    - 5000 - LibreTranslate
    - 11434 - OLLAMA
"""
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

INIT_PROMPT = (
    "You are a translator/dictionary. You'll recieve JSON, e.g.: {'word':'xyz', 'native':'pl', 'foreign':'en'} (ISO codes). "
    "Translate the word from the 'native' language to the 'foreign' language. Return the respnse in the 'native' language in the following JSON format:"
    "{"
    "translation: 'translation into foreign',"
    "meaning: 'short and simple explanation of the word in the native language',"
    "type: 'noun/verb/adjective',"
    "synonyms: ['synonym1', 'synonym2', 'synonym3'],"
    "examples: ['example sentence 1', 'example sentence 2', 'example sentence 3']"
    "}"
    "Your response should be only this JSON, nothing else."
)

"""
        LibreTranslate - port 5000
        what can be achieved with `LibreTranslate`:
        use - https://github.com/LibreTranslate/LibreTranslate
"""

def extract_first_json(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        raw = match.group()
        raw = re.sub(r',\s*}', '}', raw)
        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            print("JSON decode error:", e)
            print("Problematic JSON:", raw)
            raise
    raise ValueError("No JSON found in response")


@app.get("/word/{word}")
async def read_word(word: str):
    print("request recieved")
    final_prompt = (
    f"{INIT_PROMPT}\n"
    f"{{'word': '{word}', 'native': 'en', 'foreign': 'es'}}")
    
    # print(final_prompt)

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            url="http://ollama:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": final_prompt,
                "stream": False
            }
        )
        # response_data - informacje o modelu, duration etc.
        response_data = response.json()
        print("RAW response_data:", response_data)
        # response_dict - we extract only what we want to serve to the frontend
        response_dict = extract_first_json(response_data.get('response',''))
        print("RAW response_data['response']:", response_data.get('response'))


        return JSONResponse(content=response_dict)
