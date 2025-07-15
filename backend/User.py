import httpx
from fastapi.responses import JSONResponse

class Book:
    def __init__(self, name:str, native: str, foreign: str):
        self.name = name
        self.native = native
        self.foreign = foreign

    
    def toString(self) -> str:
        return self.title

    def setCover(self, cover: bytes):
        self.cover = cover
    
    def setMetadata(self, metadata: list[dict]):
        self.metadata = metadata

    # async def getMetadata(self) -> JSONResponse:
    #     url = f"https://openlibrary.org/search.json?q={self.title}&fields=key,title,cover_i,author_name,editions,editions.key,editions.title,editions.language"
    #     async with httpx.AsyncClient(timeout=120.0) as client:
    #             response = await client.get(
    #                 url=url
    #             )
    #             data = response.json()
    #             needed=[
    #                 {
    #                     "author_name":doc.get("author_name",[]),
    #                     "title":doc.get("title",[]),
    #                     "cover_i":doc.get("cover_i",[])
    #                 }
    #                 for doc in data.get('docs',[])
    #                 if isinstance(doc.get("cover_i"), int) # dont show book entries that dont have a cover image
    #             ]

    #             self.setMetadata(needed)
    #             return JSONResponse(needed)

