from fastapi import FastAPI,HTTPException
from sqlalchemy import create_engine, text
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from Book import Book
import httpx
import json
import re
import os

""" PORTS:
    - 5173 - FRONTEND
    - 5174 - BACKEND
    - 5000 - LibreTranslate
    - 11434 - OLLAMA
"""

DATABASE_URL = os.getenv("DATABASE_URL")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")

app = FastAPI()
db = create_engine(DATABASE_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

INIT_PROMPT = (
    "As a JSON translation API, return exactly this structure:\n"
    "{\n"
    "  \"translation\": \"accurate_translation\",\n"
    "  \"meaning\": \"clear_definition_in_native_language\",\n"
    "  \"type\": \"part_of_speech_in_native_terms\",\n"
    "  \"synonyms\": [\"syn1\", \"syn2\"],\n"
    "  \"examples\": [\"ex1\", \"ex2\", \"ex3\"]\n"
    "}\n"
    "Rules:\n"
    "- Always return ALL fields\n"
    "- Exactly 3 examples\n"
    "- 2-4 synonyms\n"
    "- Meaning/type/synonyms in {native}\n"
    "- Translation/examples in {foreign}\n"
    "Example for pl->es:\n"
    "{\"translation\":\"gato\",\"meaning\":\"Ssak domowy\",\"type\":\"rzeczownik\",\"synonyms\":[\"kotek\",\"mruczek\"],\"examples\":[\"El gato ma\",\"Los gatos son\",\"Mi gato es\"]}"
)


"""
        LibreTranslate - port 5000
        what can be achieved with `LibreTranslate`:
        use - https://github.com/LibreTranslate/LibreTranslate
"""

# Word--------------------------------------------------------------------------------------------------------
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
async def read_word(
    word: str,
    native: str = None,
    foreign: str = None
    ):

    print("request recieved")
    print("native:", native)
    print("foreign:", foreign)

    final_prompt = (
    f"{INIT_PROMPT}\n"
    f"{{'word': '{word}', 'native': '{native}', 'foreign': '{foreign}'}}")
    # print(final_prompt)



    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                url="http://ollama:11434/api/generate",
                json={
                    "model": "llama3",
                    "prompt": final_prompt,
                    "stream": False,
                    "options": {
                            "temperature": 0.3,
                            "num_ctx": 2048,
                            "num_thread": 4 
                        }
                }
            )
            # response_data - informacje o modelu, duration etc.
            response_data = response.json()
            print("RAW response_data:", response_data)
            # response_dict - we extract only what we want to serve to the frontend
            response_dict = extract_first_json(response_data.get('response',''))
            print("RAW response_data['response']:", response_data.get('response'))
            return JSONResponse(content=response_dict)

    except httpx.ReadTimeout:
        raise HTTPException(
            status_code=504,
            detail="Ollama response timeout. Try a simpler word or try again later.")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Translation error: {str(e)}")

# Book--------------------------------------------------------------------------------------------------------
@app.post("/book/newBook")
async def add_book(
    title: str
    ):

    b1 = Book(title=title)

    metadata = await b1.getMetadata()

    json_formatted= json.dumps(b1.metadata, indent=2)
    print(json_formatted)

    return metadata

@app.get("/book/{bookId}/cover")
async def get_cover(bookId:str):
    no_rules_cover_i = "10524294"
    cover_i = no_rules_cover_i

    print(DATABASE_URL)
    print(DB_USER)
    print(DB_PASSWORD)

    # async with httpx.AsyncClient(timeout=120.0) as client:
    #             response = await client.get(
    #                 url="https://covers.openlibrary.org/b/id/{cover_i}.jpg"
    #             )

    #             print(response)
    #             return(response)
# User--------------------------------------------------------------------------------------------------------
# @app.get("/util/listOfISOcodes")

@app.post("/user/new")
async def add_user(
    # name:str,
    # native:str,
    # foreign:str
    ):
    with db.connect() as conn:
        result = conn.execute(
            text("select * from users;")
        )
        for row in result:
            print(row)


    return {"status":"ok"}