from urllib import request
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from schemas.Book import Book
from schemas.User import User
from schemas.DBconnection import DBconnection

import httpx
import json
import re
from fastapi import status, HTTPException, Response, Body
from auth.security import hash_password, create_access_token, verify_password

"""
status.HTTP_200_OK
status.HTTP_201_CREATED
status.HTTP_204_NO_CONTENT
status.HTTP_400_BAD_REQUEST
status.HTTP_401_UNAUTHORIZED
status.HTTP_403_FORBIDDEN
status.HTTP_404_NOT_FOUND
status.HTTP_409_CONFLICT
status.HTTP_422_UNPROCESSABLE_ENTITY
status.HTTP_500_INTERNAL_SERVER_ERROR

PORTS:
    - 5173 - FRONTEND
    - 5174 - BACKEND
    - 5000 - LibreTranslate
    - 11434 - OLLAMA
"""
app = FastAPI()
# json.dumps(data, indent=2)

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
@app.post("/book/new")
async def add_book(title: str, response_class=JSONResponse) -> JSONResponse:
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")

    bk = Book(title=title)
    bk = DBconnection.insertBook(bk) # only now .insertBook can return None, so now we check if the operation was successfull
    if bk:
        print(bk.__repr__())
        return JSONResponse(
            status_code = 201, # 201 - created
            content={"msg":f"{bk.__repr__()} created"}
        )
    else:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Book with that title already exists"
        )
    # await bk.fetchMetadata() # this will fetch fields like cover and author_title and assign it to the bk object
@app.get("/book/{bookId}/cover")
async def get_cover(bookId:str):
    no_rules_cover_i = "10524294"
    cover_i = no_rules_cover_i

    # async with httpx.AsyncClient(timeout=120.0) as client:
    #             response = await client.get(
    #                 url="https://covers.openlibrary.org/b/id/{cover_i}.jpg"
    #             )

    #             print(response)
    #             return(response)

# Auth--------------------------------------------------------------------------------------------------------
@app.post("/auth/signup")
def signup(
    username: str = Body(...),
    password: str = Body(...),
    native: str = Body(...),
    foreign: str = Body(...)
) -> JSONResponse:

    if DBconnection.getUserByUsername(username):
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    hashed_pass = hash_password(password)

    user = User(username=username,native=native,foreign=foreign,hashed_password=hashed_pass)
    DBconnection.insertUser(user)

    # log in after successfull sign up
    access_token = create_access_token(data={"sub": user.username})

    return JSONResponse(
        status_code=201,
        content = {'msg':'User created successfully',
                 'access_token':access_token,
                 'token_type':'bearer'
                 }
    )
@app.post("/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    user = DBconnection.getUserByUsername(form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect username or password"
        )
    
    access_token = create_access_token(data={"sub": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# User--------------------------------------------------------------------------------------------------------
# @app.get("/util/listOfISOcodes")
@app.get("/user/")
def get_users():
    return DBconnection.getUsers()

@app.get("/user/{username}")
def get_specific_user(username: str):
    return DBconnection.getUserByUsername(username)

@app.get("/db-test")
def db_test():
    return DBconnection.test()
