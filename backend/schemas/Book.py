import httpx
from fastapi.responses import JSONResponse

class Book:
    def __init__(self, title:str, cover: bytes = None, metadata: list[dict] = None):
        self.title = title
        self.cover = cover
        self.metadata = metadata or []
    
    def toString(self) -> str:
        return self.title

    def setCover(self, cover: bytes):
        self.cover = cover
    
    def setMetadata(self, metadata: list[dict]):
        self.metadata = metadata

    async def getMetadata(self) -> JSONResponse:
        url = f"https://openlibrary.org/search.json?q={self.title}&fields=key,title,cover_i,author_name,editions,editions.key,editions.title,editions.language"
        async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.get(
                    url=url
                )
                data = response.json()
                needed=[
                    {
                        "author_name":doc.get("author_name",[]),
                        "title":doc.get("title",[]),
                        "cover_i":doc.get("cover_i",[])
                    }
                    for doc in data.get('docs',[])
                    if isinstance(doc.get("cover_i"), int) # dont show book entries that dont have a cover image
                ]

                self.setMetadata(needed)
                return JSONResponse(needed)


